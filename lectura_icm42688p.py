import spidev
import time
import struct

# Configurar SPI
spi = spidev.SpiDev()
spi.open(0, 0)             # Bus 0, dispositivo CS0
spi.max_speed_hz = 1000000 # 1 MHz (puedes subirlo luego)
spi.mode = 0               # Modo SPI 0 (CPOL=0, CPHA=0)
spi.bits_per_word = 8

def read_frame():
    # Enviamos 16 bytes vacíos y recibimos 16 bytes del STM32 (full duplex)
    rx = spi.xfer2([0x00] * 16)

    # Verificar encabezado AA 55
    if rx[0] != 0xAA or rx[1] != 0x55:
        print("Frame inválido:", rx)
        return None

    # Empaquetar los datos: 7 valores enteros de 16 bits con signo
    temp, ax, ay, az, gx, gy, gz = struct.unpack(">7h", bytes(rx[2:16]))

    return {
        "temp_raw": temp,
        "ax": ax,
        "ay": ay,
        "az": az,
        "gx": gx,
        "gy": gy,
        "gz": gz
    }

# Loop principal
while True:
    data = read_frame()
    if data:
        print(data)
    time.sleep(0.05)  # 20 Hz lectura desde Raspberry
