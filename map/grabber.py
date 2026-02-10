from machine import Pin, PWM
from utime import sleep


class Servo:

    # Lets you control the servos easily

    def __init__(self, pin, freq, offset=2621, multiplier=50):
        self.pwm = PWM(Pin(pin), freq)
        self.offset = int(offset)  # offset for the PWM's 0 state
        self.duty_u16 = int(offset)  # holds the PWM's duty cycle (starts at offset or 0 state)
        self.multiplier = multiplier  # multiplier for angle -> u16 conversion
        self.zero_degrees()

    def zero_degrees(self):  # Sets the Servo to its 0 state
        self.pwm.duty_u16(self.offset)

    def turn(self, angle, t_ms=1):
        # Turns (around) the angle in degrees you ask
        # +ve is anticlockwise looking towards the servo's rotator
        # Can also specify the time in which you want the servo to rotate the angle
        #  just in case you don't want to fling something
        for _ in range(t_ms):
            self.duty_u16 += (angle * self.multiplier / t_ms)
            self.pwm.duty_u16(int(self.duty_u16))
            sleep(0.001)

        self.duty_u16 = int(self.duty_u16)


def open_wide(grabber:Servo):
    grabber.turn(20)

def open_narrow(grabber:Servo):
    grabber.turn(10)

def close(grabber:Servo):
    grabber.turn(-30)

def lift(lifter:Servo):
    lifter.turn(20, 500)

def drop(lifter:Servo):
    lifter.turn(-20, 500)

def pick_up_coil(pause_count):
    #Algorithm to operate servos and pick up coil

    return pause_count

def drop_off_coil(pause_count):
    #Algorithm to operate servos and drop off coil

    return pause_count
