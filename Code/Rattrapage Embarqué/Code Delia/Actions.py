"""Import Enum"""
from enum import Enum

class Actions(Enum):
    """Enum for the actions of the robot"""
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    ENABLEMAGNET = 6
    DISABLEMAGNET = 7
