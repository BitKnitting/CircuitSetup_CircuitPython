#############################################################################
# The intent of this script is to read in the Arduino register include file: 
# and convert into Python's syntax.
#############################################################################


arduino_reg_file = open('ATM90E32.h')
python_reg_file = open('atm90e32_registers.py', 'w+')
with arduino_reg_file as file:
    reader = arduino_reg_file.readlines()
    for line in reader:
        if ('SagTh' in line):
            print(line)
        if ('#define' in line):
            line = line.replace('#define', '')
            line = line.replace('\t', ' ')
            line = line.replace('//', '#')
            index = line.find('0x')
            line = line[:index-1] + '=' + line[index:]
            line = line.lstrip(' ')
            python_reg_file.write(line)
        else:
            line = line.replace('/', '#')
            python_reg_file.write(line)
