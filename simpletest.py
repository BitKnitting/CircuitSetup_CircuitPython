import digitalio
import board
import busio
from atm90e32 import ATM90e32

spi_bus = busio.SPI(board.SCK, MISO=board.MISO,MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D10)
energy_sensor  = ATM90e32(spi_bus,cs)