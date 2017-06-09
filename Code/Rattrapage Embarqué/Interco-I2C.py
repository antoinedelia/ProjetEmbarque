class IntercoI2C:

def _init_(self):
    self.bus = smbus.SMBus(1)
    self.address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number