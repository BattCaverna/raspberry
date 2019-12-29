import spidev
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000
spi.cshigh = True

data = [0x00, 0x00]
while True:
    inp = spi.xfer(data)
    data = [~inp[0], ~inp[1]]
