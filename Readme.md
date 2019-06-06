
# CircuitPython for the Single Phase Energy Monitor

# Thanks to Those that went Before
There is _so much_ prior work that made it easier to write a CP library for the atm90e32.  Efforts include:  
* Tisham Dhar's [atm90e26 Arduino library](https://github.com/whatnick/ATM90E26_Arduino).    
* The [atm90e26 Circuit Python library I wrote](https://github.com/BitKnitting/HappyDay_ATM90e26_CircuitPython)  
* Circuit Setup's [atm90e32 Arduino library](https://github.com/CircuitSetup/Split-Single-Phase-Energy-Meter/tree/master/Software/libraries/ATM90E32)
# Sending and Receiving SPI
This is all about reading and writing over SPI to the atm90e32's registers.    
* Step 1: I "converted" the [ATM90E32.h include file](https://github.com/CircuitSetup/Split-Single-Phase-Energy-Meter/blob/master/Software/libraries/ATM90E32/ATM90E32.h) into an equivalent python file using [register_from_ard_to_py.py script](arduino_to_python/register_from_ard_to_py.py).  
* Step 2: Copy / munged a bit / pasted code from my [atm90e26 Circuit Python library](https://github.com/BitKnitting/HappyDay_ATM90e26_CircuitPython).