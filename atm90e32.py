# from atm90e32_registers import *
from adafruit_bus_device.spi_device import SPIDevice
import math
import time



#* STATUS REGISTERS *#
MeterEn = 0x00   # Metering Enable
ChannelMapI = 0x01  # Current Channel Mapping Configuration
ChannelMapU = 0x02  # Voltage Channel Mapping Configuration
SagPeakDetCfg = 0x05  # Sag and Peak Detector Period Configuration
OVth = 0x06    # Over Voltage Threshold
ZXConfig = 0x07   # Zero-Crossing Config
SagTh = 0x08    # Voltage Sag Th
PhaseLossTh = 0x09  # Voltage Phase Losing Th
INWarnTh = 0x0A   # Neutral Current (Calculated) Warning Threshold
OIth = 0x0B    # Over Current Threshold
FreqLoTh = 0x0C  # Low Threshold for Frequency Detection
FreqHiTh = 0x0D  # High Threshold for Frequency Detection
PMPwrCtrl = 0x0E  # Partial Measurement Mode Power Control
IRQ0MergeCfg = 0x0F  # IRQ0 Merge Configuration

#* EMM STATUS REGISTERS *#
SoftReset = 0x70  # Software Reset
EMMState0 = 0x71  # EMM State 0
EMMState1 = 0x72  # EMM State 1
EMMIntState0 = 0x73   # EMM Interrupt Status 0
EMMIntState1 = 0x74   # EMM Interrupt Status 1
EMMIntEn0 = 0x75  # EMM Interrupt Enable 0
EMMIntEn1 = 0x76  # EMM Interrupt Enable 1
LastSPIData = 0x78  # Last Read/Write SPI Value
CRCErrStatus = 0x79  # CRC Error Status
CRCDigest = 0x7A  # CRC Digest
CfgRegAccEn = 0x7F  # Configure Register Access Enable

#* LOW POWER MODE REGISTERS - NOT USED *#
DetectCtrl = 0x10
DetectTh1 = 0x11
DetectTh2 = 0x12
DetectTh3 = 0x13
PMOffsetA = 0x14
PMOffsetB = 0x15
PMOffsetC = 0x16
PMPGA = 0x17
PMIrmsA = 0x18
PMIrmsB = 0x19
PMIrmsC = 0x1A
PMConfig = 0x10B
PMAvgSamples = 0x1C
PMIrmsLSB = 0x1D

#* CONFIGURATION REGISTERS *#
PLconstH = 0x31   # High Word of PL_Constant
PLconstL = 0x32   # Low Word of PL_Constant
MMode0 = 0x33   # Metering Mode Config
MMode1 = 0x34   # PGA Gain Configuration for Current Channels
PStartTh = 0x35   # Startup Power Th (P)
QStartTh = 0x36   # Startup Power Th (Q)
SStartTh = 0x37  # Startup Power Th (S)
PPhaseTh = 0x38   # Startup Power Accum Th (P)
QPhaseTh = 0x39  # Startup Power Accum Th (Q)
SPhaseTh = 0x3A  # Startup Power Accum Th (S)

#* CALIBRATION REGISTERS *#
PoffsetA = 0x41   # A Line Power Offset (P)
QoffsetA = 0x42   # A Line Power Offset (Q)
PoffsetB = 0x43   # B Line Power Offset (P)
QoffsetB = 0x44   # B Line Power Offset (Q)
PoffsetC = 0x45   # C Line Power Offset (P)
QoffsetC = 0x46   # C Line Power Offset (Q)
PQGainA = 0x47   # A Line Calibration Gain
PhiA = 0x48     # A Line Calibration Angle
PQGainB = 0x49   # B Line Calibration Gain
PhiB = 0x4A     # B Line Calibration Angle
PQGainC = 0x4B   # C Line Calibration Gain
PhiC = 0x4C     # C Line Calibration Angle

#* FUNDAMENTAL#HARMONIC ENERGY CALIBRATION REGISTERS *#
POffsetAF = 0x51  # A Fund Power Offset (P)
POffsetBF = 0x52  # B Fund Power Offset (P)
POffsetCF = 0x53  # C Fund Power Offset (P)
PGainAF = 0x54  # A Fund Power Gain (P)
PGainBF = 0x55  # B Fund Power Gain (P)
PGainCF = 0x56  # C Fund Power Gain (P)

#* MEASUREMENT CALIBRATION REGISTERS *#
UgainA = 0x61   # A Voltage RMS Gain
IgainA = 0x62   # A Current RMS Gain
UoffsetA = 0x63   # A Voltage Offset
IoffsetA = 0x64   # A Current Offset
UgainB = 0x65   # B Voltage RMS Gain
IgainB = 0x66   # B Current RMS Gain
UoffsetB = 0x67   # B Voltage Offset
IoffsetB = 0x68   # B Current Offset
UgainC = 0x69   # C Voltage RMS Gain
IgainC = 0x6A   # C Current RMS Gain
UoffsetC = 0x6B   # C Voltage Offset
IoffsetC = 0x6C   # C Current Offset
IoffsetN = 0x6E   # N Current Offset

#* ENERGY REGISTERS *#
APenergyT = 0x80   # Total Forward Active
APenergyA = 0x81   # A Forward Active
APenergyB = 0x82   # B Forward Active
APenergyC = 0x83   # C Forward Active
ANenergyT = 0x84   # Total Reverse Active
ANenergyA = 0x85   # A Reverse Active
ANenergyB = 0x86   # B Reverse Active
ANenergyC = 0x87   # C Reverse Active
RPenergyT = 0x88   # Total Forward Reactive
RPenergyA = 0x89   # A Forward Reactive
RPenergyB = 0x8A   # B Forward Reactive
RPenergyC = 0x8B   # C Forward Reactive
RNenergyT = 0x8C   # Total Reverse Reactive
RNenergyA = 0x8D   # A Reverse Reactive
RNenergyB = 0x8E   # B Reverse Reactive
RNenergyC = 0x8F   # C Reverse Reactive

SAenergyT = 0x90   # Total Apparent Energy
SenergyA = 0x91    # A Apparent Energy
SenergyB = 0x92   # B Apparent Energy
SenergyC = 0x93   # C Apparent Energy


#* FUNDAMENTAL # HARMONIC ENERGY REGISTERS *#
APenergyTF = 0xA0  # Total Forward Fund. Energy
APenergyAF = 0xA1  # A Forward Fund. Energy
APenergyBF = 0xA2  # B Forward Fund. Energy
APenergyCF = 0xA3  # C Forward Fund. Energy
ANenergyTF = 0xA4   # Total Reverse Fund Energy
ANenergyAF = 0xA5  # A Reverse Fund. Energy
ANenergyBF = 0xA6  # B Reverse Fund. Energy
ANenergyCF = 0xA7  # C Reverse Fund. Energy
APenergyTH = 0xA8  # Total Forward Harm. Energy
APenergyAH = 0xA9  # A Forward Harm. Energy
APenergyBH = 0xAA  # B Forward Harm. Energy
APenergyCH = 0xAB  # C Forward Harm. Energy
ANenergyTH = 0xAC  # Total Reverse Harm. Energy
ANenergyAH = 0xAD   # A Reverse Harm. Energy
ANenergyBH = 0xAE   # B Reverse Harm. Energy
ANenergyCH = 0xAF   # C Reverse Harm. Energy

#* POWER & P.F. REGISTERS *#
PmeanT = 0xB0   # Total Mean Power (P)
PmeanA = 0xB1   # A Mean Power (P)
PmeanB = 0xB2   # B Mean Power (P)
PmeanC = 0xB3   # C Mean Power (P)
QmeanT = 0xB4   # Total Mean Power (Q)
QmeanA = 0xB5   # A Mean Power (Q)
QmeanB = 0xB6   # B Mean Power (Q)
QmeanC = 0xB7   # C Mean Power (Q)
SmeanT = 0xB8   # Total Mean Power (S)
SmeanA = 0xB9   # A Mean Power (S)
SmeanB = 0xBA   # B Mean Power (S)
SmeanC = 0xBB   # C Mean Power (S)
PFmeanT = 0xBC   # Mean Power Factor
PFmeanA = 0xBD   # A Power Factor
PFmeanB = 0xBE   # B Power Factor
PFmeanC = 0xBF   # C Power Factor

PmeanTLSB = 0xC0   # Lower Word (Tot. Act. Power)
PmeanALSB = 0xC1   # Lower Word (A Act. Power)
PmeanBLSB = 0xC2   # Lower Word (B Act. Power)
PmeanCLSB = 0xC3   # Lower Word (C Act. Power)
QmeanTLSB = 0xC4   # Lower Word (Tot. React. Power)
QmeanALSB = 0xC5   # Lower Word (A React. Power)
QmeanBLSB = 0xC6   # Lower Word (B React. Power)
QmeanCLSB = 0xC7   # Lower Word (C React. Power)
SAmeanTLSB = 0xC8  # Lower Word (Tot. App. Power)
SmeanALSB = 0xC9   # Lower Word (A App. Power)
SmeanBLSB = 0xCA   # Lower Word (B App. Power)
SmeanCLSB = 0xCB   # Lower Word (C App. Power)

#* FUND#HARM POWER & V#I RMS REGISTERS *#
PmeanTF = 0xD0   # Total Active Fund. Power
PmeanAF = 0xD1   # A Active Fund. Power
PmeanBF = 0xD2   # B Active Fund. Power
PmeanCF = 0xD3   # C Active Fund. Power
PmeanTH = 0xD4   # Total Active Harm. Power
PmeanAH = 0xD5   # A Active Harm. Power
PmeanBH = 0xD6   # B Active Harm. Power
PmeanCH = 0xD7   # C Active Harm. Power
UrmsA = 0xD9    # A RMS Voltage
UrmsB = 0xDA    # B RMS Voltage
UrmsC = 0xDB    # C RMS Voltage
IrmsA = 0xDD    # A RMS Current
IrmsB = 0xDE    # B RMS Current
IrmsC = 0xDF    # C RMS Current
IrmsN = 0xD8    # Calculated N RMS Current

PmeanTFLSB = 0xE0  # Lower Word (Tot. Act. Fund. Power)
PmeanAFLSB = 0xE1  # Lower Word (A Act. Fund. Power)
PmeanBFLSB = 0xE2  # Lower Word (B Act. Fund. Power)
PmeanCFLSB = 0xE3  # Lower Word (C Act. Fund. Power)
PmeanTHLSB = 0xE4  # Lower Word (Tot. Act. Harm. Power)
PmeanAHLSB = 0xE5  # Lower Word (A Act. Harm. Power)
PmeanBHLSB = 0xE6  # Lower Word (B Act. Harm. Power)
PmeanCHLSB = 0xE7  # Lower Word (C Act. Harm. Power)
# 0xE8	    ## Reserved Register
UrmsALSB = 0xE9  # Lower Word (A RMS Voltage)
UrmsBLSB = 0xEA  # Lower Word (B RMS Voltage)
UrmsCLSB = 0xEB  # Lower Word (C RMS Voltage)
# 0xEC	    ## Reserved Register
IrmsALSB = 0xED  # Lower Word (A RMS Current)
IrmsBLSB = 0xEE  # Lower Word (B RMS Current)
IrmsCLSB = 0xEF  # Lower Word (C RMS Current)

#* THD, FREQUENCY, ANGLE & TEMPTEMP REGISTERS*#
THDNUA = 0xF1   # A Voltage THD+N
THDNUB = 0xF2   # B Voltage THD+N
THDNUC = 0xF3   # C Voltage THD+N
# 0xF4	    ## Reserved Register
THDNIA = 0xF5   # A Current THD+N
THDNIB = 0xF6   # B Current THD+N
THDNIC = 0xF7   # C Current THD+N
Freq = 0xF8    # Frequency
PAngleA = 0xF9   # A Mean Phase Angle
PAngleB = 0xFA   # B Mean Phase Angle
PAngleC = 0xFB   # C Mean Phase Angle
Temp = 0xFC   # Measured Temperature
UangleA = 0xFD  # A Voltage Phase Angle
UangleB = 0xFE  # B Voltage Phase Angle
UangleC = 0xFF  # C Voltage Phase Angle


SPI_WRITE = 0
SPI_READ = 1

class ATM90e32:
    ##############################################################################

    def __init__(self, spi_bus, cs):
        self._device = SPIDevice(spi_bus, cs, baudrate=200000, polarity=1, phase=1)
        self._init_config()


    def _init_config(self):
        # Initialize registers
        #***** CALIBRATION SETTINGS *****/
        _lineFreq = 4485        #4485 for 60 Hz (North America)
                                #389 for 50 hz (rest of the world)
        _pgagain = 21           #21 for 100A (2x), 42 for >100A (4x)

        _ugain = 42080          #42080 - 9v AC transformer.
                                #32428 - 12v AC Transformer                                        
        _igainA = 25498         #38695 - SCT-016 120A/40mA
        _igainB = 0
        _igainC = 25498
        #CurrentGainCT2 = 25498  #25498 - SCT-013-000 100A/50mA
        if (_lineFreq == 4485 or _lineFreq == 5231):
            #North America power frequency
            FreqHiThresh = 61 * 100
            FreqLoThresh = 59 * 100
            sagV = 90
        else:
            FreqHiThresh = 51 * 100
            FreqLoThresh = 49 * 100
            sagV = 190

        #calculation for voltage sag threshold - assumes we do not want to go under 90v for split phase and 190v otherwise
        # sqrt(2) = 1.41421356
        fvSagTh = (sagV * 100 * 1.41421356) / (2 * _ugain / 32768)
        # convert to int for sending to the atm90e32.
        vSagTh = self._round_number(fvSagTh)

        self._spi_rw(SPI_WRITE, SoftReset, 0x789A)   # Perform soft reset
        self._spi_rw(SPI_WRITE, CfgRegAccEn, 0x55AA) # enable register config access
        self._spi_rw(SPI_WRITE, MeterEn, 0x0001)   # Enable Metering


        self._spi_rw(SPI_WRITE, SagTh, vSagTh)         # Voltage sag threshold
        self._spi_rw(SPI_WRITE, FreqHiTh, FreqHiThresh)  # High frequency threshold - 61.00Hz
        self._spi_rw(SPI_WRITE, FreqLoTh, FreqLoThresh)  # Lo frequency threshold - 59.00Hz
        self._spi_rw(SPI_WRITE, EMMIntEn0, 0xB76F)   # Enable interrupts
        self._spi_rw(SPI_WRITE, EMMIntEn1, 0xDDFD)   # Enable interrupts
        self._spi_rw(SPI_WRITE, EMMIntState0, 0x0001)  # Clear interrupt flags
        self._spi_rw(SPI_WRITE, EMMIntState1, 0x0001)  # Clear interrupt flags
        self._spi_rw(SPI_WRITE, ZXConfig, 0x0A55)      # ZX2, ZX1, ZX0 pin config

        #Set metering config values (CONFIG)
        self._spi_rw(SPI_WRITE, PLconstH, 0x0861)    # PL Constant MSB (default) - Meter Constant = 3200 - PL Constant = 140625000
        self._spi_rw(SPI_WRITE, PLconstL, 0xC468)    # PL Constant LSB (default) - this is 4C68 in the application note, which is incorrect
        self._spi_rw(SPI_WRITE, MMode0, _lineFreq)   # Mode Config (frequency set in main program)
        self._spi_rw(SPI_WRITE, MMode1, _pgagain)    # PGA Gain Configuration for Current Channels - 0x002A (x4) # 0x0015 (x2) # 0x0000 (1x)
        self._spi_rw(SPI_WRITE, PStartTh, 0x0AFC)    # Active Startup Power Threshold - 50% of startup current = 0.9/0.00032 = 2812.5
        self._spi_rw(SPI_WRITE, QStartTh, 0x0AEC)    # Reactive Startup Power Threshold
        self._spi_rw(SPI_WRITE, SStartTh, 0x0000)    # Apparent Startup Power Threshold
        self._spi_rw(SPI_WRITE, PPhaseTh, 0x00BC)    # Active Phase Threshold = 10% of startup current = 0.06/0.00032 = 187.5
        self._spi_rw(SPI_WRITE, QPhaseTh, 0x0000)    # Reactive Phase Threshold
        self._spi_rw(SPI_WRITE, SPhaseTh, 0x0000)    # Apparent  Phase Threshold

        #Set metering calibration values (CALIBRATION)
        self._spi_rw(SPI_WRITE, PQGainA, 0x0000)     # Line calibration gain
        self._spi_rw(SPI_WRITE, PhiA, 0x0000)        # Line calibration angle
        self._spi_rw(SPI_WRITE, PQGainB, 0x0000)     # Line calibration gain
        self._spi_rw(SPI_WRITE, PhiB, 0x0000)        # Line calibration angle
        self._spi_rw(SPI_WRITE, PQGainC, 0x0000)     # Line calibration gain
        self._spi_rw(SPI_WRITE, PhiC, 0x0000)        # Line calibration angle
        self._spi_rw(SPI_WRITE, PoffsetA, 0x0000)    # A line active power offset
        self._spi_rw(SPI_WRITE, QoffsetA, 0x0000)    # A line reactive power offset
        self._spi_rw(SPI_WRITE, PoffsetB, 0x0000)    # B line active power offset
        self._spi_rw(SPI_WRITE, QoffsetB, 0x0000)    # B line reactive power offset
        self._spi_rw(SPI_WRITE, PoffsetC, 0x0000)    # C line active power offset
        self._spi_rw(SPI_WRITE, QoffsetC, 0x0000)    # C line reactive power offset

        #Set metering calibration values (HARMONIC)
        self._spi_rw(SPI_WRITE, POffsetAF, 0x0000)   # A Fund. active power offset
        self._spi_rw(SPI_WRITE, POffsetBF, 0x0000)   # B Fund. active power offset
        self._spi_rw(SPI_WRITE, POffsetCF, 0x0000)   # C Fund. active power offset
        self._spi_rw(SPI_WRITE, PGainAF, 0x0000)     # A Fund. active power gain
        self._spi_rw(SPI_WRITE, PGainBF, 0x0000)     # B Fund. active power gain
        self._spi_rw(SPI_WRITE, PGainCF, 0x0000)     # C Fund. active power gain

        #Set measurement calibration values (ADJUST)
        self._spi_rw(SPI_WRITE, UgainA, _ugain)      # A Voltage rms gain
        self._spi_rw(SPI_WRITE, IgainA, _igainA)      # A line current gain
        self._spi_rw(SPI_WRITE, UoffsetA, 0x0000)    # A Voltage offset
        self._spi_rw(SPI_WRITE, IoffsetA, 0x0000)    # A line current offset
        self._spi_rw(SPI_WRITE, UgainB, _ugain)      # B Voltage rms gain
        self._spi_rw(SPI_WRITE, IgainB, _igainB)      # B line current gain
        self._spi_rw(SPI_WRITE, UoffsetB, 0x0000)    # B Voltage offset
        self._spi_rw(SPI_WRITE, IoffsetB, 0x0000)    # B line current offset
        self._spi_rw(SPI_WRITE, UgainC, _ugain)      # C Voltage rms gain
        self._spi_rw(SPI_WRITE, IgainC, _igainC)      # C line current gain
        self._spi_rw(SPI_WRITE, UoffsetC, 0x0000)    # C Voltage offset
        self._spi_rw(SPI_WRITE, IoffsetC, 0x0000)    # C line current offset

        self._spi_rw(SPI_WRITE, CfgRegAccEn, 0x0000) # end configuration
    ##################################################################################### 
    @property
    def sys_status0(self):
        reading = self._spi_rw(SPI_READ, EMMIntState0, 0xFFFF)
        return reading
    #####################################################################################    
    @property
    def sys_status1(self):
        reading = self._spi_rw(SPI_READ, EMMIntState1, 0xFFFF)
        return reading  
     #####################################################################################     
    @property
    def meter_status0(self):
        reading = self._spi_rw(SPI_READ, EMMState0, 0xFFFF)
        return reading
    #####################################################################################    
    @property
    def meter_status1(self):
        reading = self._spi_rw(SPI_READ, EMMState1, 0xFFFF)
        return reading   
    #####################################################################################    
    @property
    def line_voltageA(self):
        reading = self._spi_rw(SPI_READ, UrmsA, 0xFFFF)
        return reading  
            #####################################################################################    
    @property
    def line_voltageB(self):
        reading = self._spi_rw(SPI_READ, UrmsB, 0xFFFF)
        return reading  
            #####################################################################################    
    @property
    def line_voltageC(self):
        reading = self._spi_rw(SPI_READ, UrmsC, 0xFFFF)
        return reading  

    #####################################################################################
    def _spi_rw(self, rw, address, value):
        # Get address ready for SPI #########################
        # set read/write flag 
        address |= rw << 15
        # swap bytes and put into byte array
        bytes_address = address.to_bytes(2,'big')
        ######################################################       
        # The Arduino library put us sleeps in...
        usleep = lambda x: time.sleep(x/1000000.0)
        # Write address to SPI
        with self._device as spi:
            print('before spi address write.')
            spi.write(bytes_address)
            print('after spi address write.')
        if rw:  # if True, reading from a register
            read_buf = bytearray(2)
            with self._device as spi:
                # from Arduino lib: "Must wait 4 us for data to become valid"
                usleep(4)
                spi.readinto(read_buf)
                value = int.from_bytes(read_buf, 'big')
                return value
        else:  # Write the two bytes of the value.
            bytes_value = value.to_bytes(2,'big')
            with self._device as spi:
                usleep(4)
                print('before spi write.')
                spi.write(bytes_value)
                print('after spi write.')
    
    def _round_number(self,f_num):
        if f_num - math.floor(f_num) < 0.5:
            return math.floor(f_num)
        return math.ceil(f_num)    

