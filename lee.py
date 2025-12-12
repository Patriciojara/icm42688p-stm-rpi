import struct
import math

ACCEL_LSB_PER_G = 2048.0   # si estás en ±16g
GYRO_LSB_PER_DPS = 16.4    # si estás en ±2000 dps

def parse_frame(rx):
    if len(rx) != 16 or rx[0] != 0xAA or rx[1] != 0x55:
        return None

    temp_raw, ax, ay, az, gx, gy, gz = struct.unpack(">7h", bytes(rx[2:16]))

    temp_c = temp_raw / 132.48 + 25.0

    ax_g = ax / ACCEL_LSB_PER_G
    ay_g = ay / ACCEL_LSB_PER_G
    az_g = az / ACCEL_LSB_PER_G
    a_mag = math.sqrt(ax_g*ax_g + ay_g*ay_g + az_g*az_g)

    gx_dps = gx / GYRO_LSB_PER_DPS
    gy_dps = gy / GYRO_LSB_PER_DPS
    gz_dps = gz / GYRO_LSB_PER_DPS

    return {
        "temp_raw": temp_raw,
        "temp_c": temp_c,
        "ax": ax, "ay": ay, "az": az,
        "ax_g": ax_g, "ay_g": ay_g, "az_g": az_g,
        "a_mag_g": a_mag,
        "gx": gx, "gy": gy, "gz": gz,
        "gx_dps": gx_dps, "gy_dps": gy_dps, "gz_dps": gz_dps,
    }

while True:
    print(parse_frame)