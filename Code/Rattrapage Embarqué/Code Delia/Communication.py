import smbus

bus = smbus.SMBus(1)
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    return -1
@staticmethod
def readNumber():
    number = bus.read_byte(address)
    return number
