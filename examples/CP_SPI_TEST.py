import time
import digitalio
import board
import busio
from adafruit_bus_device.spi_device import SPIDevice
from atm90e32_registers import *
import struct
READ = 1
WRITE = 0


def usleep(x): return time.sleep(x/(1e7))


def _do_spi(rw, address, val):
    global device
    two_byte_buf = bytearray(2)
    four_byte_buf = bytearray(4)
    results_buf = bytearray(2)
    print('the address is {:#04x} '.format(address))
    address |= rw << 15

    if(rw):  # read
        # pack the address into a the bytearray.  It is an unsigned short(H) that needs to be in MSB(>)
        struct.pack_into('>H', two_byte_buf, 0, address)
        # wait for data to become valid (4uS) - see http://bit.ly/2Zh6VI9
        usleep(4)
        with device as spi:
            # send address w/ read request to the atm90e32
            spi.write(two_byte_buf)
            # Get the unsigned short register values sent from the atm90e32
            spi.readinto(results_buf)
            result = struct.unpack('>H', results_buf)
            # unpack returns a tuple.  We're interested in result's first byte
            print('The bytes returned after a read request to address {:#04x} is {:#04x}'.format(
                address, result[0]))
    else:
        # pack the address into a the bytearray.  It is an unsigned short(H) that needs to be in MSB(>)
        struct.pack_into('>H', four_byte_buf, 0, address)
        struct.pack_into('>H', four_byte_buf, 2, val)
        usleep(4)
        with device as spi:
            spi.write(four_byte_buf)


spi_bus = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D10)
device = SPIDevice(spi_bus, cs, baudrate=200000, polarity=1, phase=1)
# Test: Read meter status 0 (address 0x71)
_do_spi(WRITE, SoftReset, 0x789A)
_do_spi(READ, EMMState0, 0xFFFF)
_do_spi(READ, 0x78, 0xFFF)
