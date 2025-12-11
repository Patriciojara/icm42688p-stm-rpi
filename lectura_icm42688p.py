import spidev

spi = spidev.SpiDev()
spi.open(0, 0)      # bus, device -> deberás ajustarlo a tu configuración
spi.max_speed_hz = 1000000
spi.mode = 0

frame = spi.xfer2([0]*16)
# frame[0:2] -> 0xAA, 0x55
# frame[2:4] temp, etc.
