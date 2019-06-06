import board
import busio
import digitalio

cs = digitalio.DigitalInOut(board.D10)
cs.direction = digitalio.Direction.OUTPUT

spi = busio.SPI(board.SCK, MISO=board.MISO,MOSI=board.MOSI)
while not spi.try_lock():
    pass
spi.configure(baudrate=200000, polarity=1, phase=1)
SoftReset = 0x70
EMMIntState0 = 0x73
result = bytearray(2)
address = EMMIntState0
spi.write(bytearray([address]))


spi.readinto(result)
value = int.from_bytes(result, 'big', True)

print(hex(value))