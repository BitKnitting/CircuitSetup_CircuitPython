import digitalio
import board
import busio
from atm90e32 import ATM90e32

spi_bus = busio.SPI(board.SCK, MISO=board.MISO,MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D10)


# address = 0x70
# address1 = (address >> 8) | (address << 8)
# address = address1
# value = 0x789A
# value1 = int((value >> 8) | (value << 8))
# value = value1

energy_sensor  = ATM90e32(spi_bus,cs)