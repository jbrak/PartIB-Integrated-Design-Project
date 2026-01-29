from machine import Pin
from utime import sleep

class LineSensor:
    def __init__(self, pin):
        self.sensor = Pin(pin, Pin.IN)  # set line sensor pin

    def read(self):
        return self.sensor.value()  # return sensor value (0 or 1)


class LineSensorArray:
    """Line sensor array with four colinear sensors: port, center port, center starboard, starboard."""
    def __init__(self, p, cp, cs, s):
        """Initialize line sensor array with four sensors."""
        self.p = LineSensor(p)   #port sensor
        self.cp = LineSensor(cp)  #center port sensor
        self.cs = LineSensor(cs) #center starboard sensor
        self.s = LineSensor(s)  #starboard sensor

    def read_all(self):
        return {
            'p' : self.p.read(),
            'cp': self.cp.read(),
            'cs': self.cs.read(),
            's' : self.s.read()
        }


