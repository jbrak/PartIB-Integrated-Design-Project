from utime import sleep
from machine import Pin, SoftI2C, I2C
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from libs.VL53L0X.VL53L0X import VL53L0X

# Depreciated
class Upper_old:
    def __init__(self, sda = 16, scl = 17):
        i2c_bus = SoftI2C(sda=Pin(sda), scl=Pin(scl), freq=100000)

        assert len(i2c_bus.scan()) == 1

        self.tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

        while (self.tof.begin() != 0):
            sleep(0.5)

        self.tof.start_measurement(calib_m=self.tof.eMODE_NO_CALIB, mode=self.tof.eDISTANCE)

    def get_distance(self):
        x = None
        while x is None:
            if (self.tof.is_data_ready() == True):
                x = self.tof.get_distance_mm()

        if x != 0:
            return x
        else:
            return 1000


    def start(self):
        self.tof.start_measurement(calib_m=self.tof.eMODE_NO_CALIB, mode=self.tof.eDISTANCE)

class DistanceSensor:
    """
    Class for the Distance Sensors that we had in our big box tower.

    Attributes
    ----------
    vl5310 : VL53L0X
        Holds the VL53L0X object for the distance sensor

    Methods
    -------
    get_distance -> int
    start()
    stop() 
    """
    def __init__(self, sda, scl, id):
        """
        Initialises a Distance Sensor

        Parameters
        ----------
        sda : int
            I2C data GPIO pin
        scl : int
            I2C clock GPIO pin
        id : int
            The I2C peripheral used for the distance sensor
        """

        i2c_bus = I2C(id=id,sda=Pin(sda), scl=Pin(scl))

        self.vl53l0 = VL53L0X(i2c_bus)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[0], 18)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[1], 14)
        self.vl53l0.start()

    def get_distance(self):
        """Returns the distance that the sensor reads"""
        self.start()
        x = self.vl53l0.read()
        self.stop()
        return x

    def start(self):
        """Starts the sensor"""
        self.vl53l0.start()

    def stop(self):
        """Stops the sensor"""
        self.vl53l0.stop()