import spidev
import time
import struct
import math

# ===== Configuración SPI =====
spi = spidev.SpiDev()
spi.open(0, 0)             # SPI0, CE0
spi.max_speed_hz = 500000
spi.mode = 0
spi.bits_per_word = 8

# ===== Escalas IMU (ajústalas si cambias FS en el IMU) =====
ACCEL_LSB_PER_G = 2048.0   # ±16 g
GYRO_LSB_PER_DPS = 16.4    # ±2000 dps

FRAME_LEN = 24

def xor_checksum(data_bytes):
    c = 0
    for b in data_bytes:
        c ^= b
    return c

def read_frame():
    rx = spi.xfer2([0x00] * FRAME_LEN)

    # Verificar cabecera
    if rx[0] != 0xAA or rx[1] != 0x55:
        print("Frame inválido (header):", rx[:4], "...")
        return None

    # Verificar checksum (XOR de bytes 0..22 debe dar rx[23])
    calc = xor_checksum(rx[0:23])
    if calc != rx[23]:
        print(f"Frame inválido (checksum): calc=0x{calc:02X} rx=0x{rx[23]:02X}")
        return None

    # Status
    status = rx[22]
    imu_ok = bool(status & (1 << 0))
    mag_ok = bool(status & (1 << 1))

    # IMU: 7 int16 big-endian en rx[2:16]
    temp_raw, ax, ay, az, gx, gy, gz = struct.unpack(">7h", bytes(rx[2:16]))

    # MAG: 3 int16 big-endian en rx[16:22]
    mx, my, mz = struct.unpack(">3h", bytes(rx[16:22]))

    return {
        "imu_ok": imu_ok,
        "mag_ok": mag_ok,
        "temp_raw": temp_raw,
        "ax": ax, "ay": ay, "az": az,
        "gx": gx, "gy": gy, "gz": gz,
        "mx": mx, "my": my, "mz": mz
    }

def print_all(d):
    # Conversión IMU
    temp_c = d["temp_raw"] / 132.48 + 25.0

    ax_g = d["ax"] / ACCEL_LSB_PER_G
    ay_g = d["ay"] / ACCEL_LSB_PER_G
    az_g = d["az"] / ACCEL_LSB_PER_G
    a_mag = math.sqrt(ax_g**2 + ay_g**2 + az_g**2)

    gx_dps = d["gx"] / GYRO_LSB_PER_DPS
    gy_dps = d["gy"] / GYRO_LSB_PER_DPS
    gz_dps = d["gz"] / GYRO_LSB_PER_DPS

    # Magnetómetro: por ahora lo muestro RAW (LSB)
    mx = d["mx"]
    my = d["my"]
    mz = d["mz"]

    # Limpiar pantalla (opcional)
    print("\033[H\033[J", end="")   # ANSI clear screen

    print("===== FRAME =====")
    print(f"IMU OK: {d['imu_ok']} | MAG OK: {d['mag_ok']}")
    print()

    print("===== ICM42688P =====")
    print(f"Temperatura : {temp_c:6.2f} °C")
    print()
    print("Acelerómetro [g]")
    print(f"  X: {ax_g:7.3f}")
    print(f"  Y: {ay_g:7.3f}")
    print(f"  Z: {az_g:7.3f}")
    print(f"  |A|: {a_mag:7.3f}")
    print()
    print("Giroscopio [°/s]")
    print(f"  X: {gx_dps:7.2f}")
    print(f"  Y: {gy_dps:7.2f}")
    print(f"  Z: {gz_dps:7.2f}")
    print()

    print("===== AK09940A =====")
    print("Magnetómetro [RAW]")
    print(f"  X: {mx:7d}")
    print(f"  Y: {my:7d}")
    print(f"  Z: {mz:7d}")
    print("=====================")

# ===== Loop principal =====
while True:
    d = read_frame()
    if d:
        print_all(d)

    time.sleep(0.1)   # 10 Hz en pantalla
