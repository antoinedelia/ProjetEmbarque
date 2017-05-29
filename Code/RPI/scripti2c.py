import smbus
import time
from enum import Enum

class Actions(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    ENABLEMAGNET = 6
    DISABLEMAGNET = 7

bus = smbus.SMBus(1)

address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number

while True:
    var = input("Enter 1-9:")
    if not var:
        continue
    writeNumber(var)
    print "RPI: hi Arduino, I sent you ", var
    time.sleep(1)
    number = readNumber()
    print "Arduino: Hey RPI, I received a digit ", number
    print
