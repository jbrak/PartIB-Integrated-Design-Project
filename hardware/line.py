from machine import Pin
from utime import sleep

class LineSensor:
    """
    Class for one line sensor
    
    Attributes
    ----------
    sensor : Pin
        Holds the line sensor's pin
    
    Methods
    -------
    read() -> int
    """
    def __init__(self, pin):
        """
        Sets the line sensor pin
        
        Parameters
        ----------
        pin : int
            The GPIO pin that the sensor is connected to
        """
        self.sensor = Pin(pin, Pin.IN)

    def read(self):
        """Returns the sensor's value (0 or 1)"""
        return self.sensor.value()


class LineSensorArray:
    """
    Line sensor array with four colinear sensors: port, center port, center starboard, starboard.
    
    Attributes
    ----------
    p : LineSensor
        Holds the port line sensor
    cp : LineSensor
        Holds the centre port line sensor
    cs : LineSensor
        Holds the centre starboard line sensor
    s : LineSensor
        Holds the starboard line sensor

    Methods
    -------
    read_all() -> dict["str", "int"]
    """

    def __init__(self, p, cp, cs, s):
        """
        Initialize line sensor array with four sensors.
        
        Parameters
        ----------
        p : int
            The port line sensor's pin
        cp : int
            The centre port line sensor's pin
        cs : int
            The centre starboard line sensor's pin
        s : int
            The starboard line sensor's pin
        """

        self.p = LineSensor(p)   
        self.cp = LineSensor(cp)  
        self.cs = LineSensor(cs) 
        self.s = LineSensor(s)  

    def read_all(self):
        """Returns a dictionary holding the readings of all the line sensors"""
        return {
            'p' : self.p.read(),
            'cp': self.cp.read(),
            'cs': self.cs.read(),
            's' : self.s.read()
        }


