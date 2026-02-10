from utime import sleep
from machine import Pin, SoftI2C, I2C
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from libs.VL53L0X.VL53L0X import VL53L0X

class Upper:
    def __init__(self, sda = 8, scl = 9):
        i2c_bus = SoftI2C(sda=Pin(sda), scl=Pin(scl), freq=100000)

        assert len(i2c_bus.scan()) == 1

        self.tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

        while (self.tof.begin() != 0):
            sleep(0.5)

        self.tof.start_measurement(calib_m=self.tof.eMODE_NO_CALIB, mode=self.tof.eDISTANCE)

    def get_distance(self):
        return self.tof.get_distance_mm()

    def start(self):
        self.tof.start_measurement(calib_m=self.tof.eMODE_NO_CALIB, mode=self.tof.eDISTANCE)

class Lower:
    def __init__(self, sda = 16, scl = 17):
        i2c_bus = I2C(id=0, sda=Pin(sda), scl=Pin(scl))

        self.vl53l0 = VL53L0X(i2c_bus)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[0], 18)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[1], 14)
        self.vl53l0.start()

    def get_distance(self):
        return self.vl53l0.read()

    def start(self):
        self.vl53l0.start()

    def stop(self):
        self.vl53l0.stop()