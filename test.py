import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)             # o (1,0) si estás usando SPI1: depende de tu cableado
spi.max_speed_hz = 500000
spi.mode = 0

while True:
    rx = spi.xfer2([0x00] * 16)
    print(rx)
    time.sleep(0.5)
