from machine import Pin, PWM
from utime import sleep


class Servo:
    """
    Lets you control the servos easily

    Attributes
    ----------
    pwm : PWM
        Holds pwm object for the servo
    multiplier : float
        Holds the multiplicative factor for converting between duty_u16 values and angles
    offset : int
        Holds the minimum duty_u16 value that the servo can turn to
    maximum : int
        Holds the maximum duty_u16 value that the servo can turn to
    duty_u16 : int
        Holds the current duty_u16 value for the servo

    Methods
    -------
    zero_degrees()
        Sets the duty_u16 value of the servo to its "zero state" (the offset)
    turn_angle(angle, time_ms=1)
        Turns the servo by the specified angle in the specified time
    turn_duty(cycle, time_ms=1)
        Turns the servo by the specified cycle in the specified time
    set_angle(angle, time_ms=1)
        Turns the servo to the specified angle in the specified time
    set_duty(cycle, time_ms=1)
        Sets the duty_u16 value to the specified cycle in the specified time

    """

    # offset = 2400 and maximum = 15000 are averaged from tested values. Refer to duty_u16 values
    def __init__(self, pin, freq, offset=2400, maximum=15000, zero=2400):
        """
        Parameters
        ----------
        pin : int
            The GPIO pin that the servo is connected to
        freq : int
            The frequency at which the servo is working at
        offset : int, optional
            The minimum duty_u16 value that the servo can turn to
        maximum : int, optional
            The maximum duty_u16 value that the servo can turn to
        """
        self.pwm = PWM(Pin(pin), freq)
        self.multiplier = 47.8  # multiplier for angle -> u16 conversion. Tested angle, accurate enough
        self.offset = int(offset)  # u16 value setting the servo's minimum
        self.zero = int(zero)
        self.maximum = int(maximum)  # u16 value setting the servo's maximum rotation
        self.zero_degrees()
        self.duty_u16 = self.pwm.duty_u16()

    def zero_degrees(self):  # Sets the Servo to its zero state
        self.pwm.duty_u16(self.zero)

    def turn_angle(self, angle, time_ms=1):
        # Turns (around) the angle in degrees you ask
        # +ve is anticlockwise looking towards the servo's rotator
        # Can also specify the time in which you want the servo to rotate the angle
        #   just in case you don't want to fling something
        for _ in range(time_ms):
            self.duty_u16 += (angle * self.multiplier / time_ms)
            # The servo should only be within the offset (minimum) and maximum
            if self.duty_u16 < self.offset:
                self.duty_u16 = self.offset
                print("Cannot turn anymore, preceeding offset")
                break
            if self.duty_u16 > self.maximum:
                self.duty_u16 = self.maximum
                print("Cannot turn anymore, exceeding maximum")
                break
            self.pwm.duty_u16(int(self.duty_u16))
            sleep(0.001)

        self.duty_u16 = int(self.duty_u16)

    def turn_duty(self, cycle, time_ms=1):
        for _ in range(time_ms):
            self.duty_u16 += cycle * 1.0 / time_ms
            if self.duty_u16 < self.offset:
                self.duty_u16 = self.offset
                print("Cannot turn anymore, preceeding offset")
            elif self.duty_u16 > self.maximum:
                self.duty_u16 = self.maximum
                print("Cannot turn anymore, exceeding maximum")
            else:
                self.pwm.duty_u16(int(self.duty_u16))

    def set_angle(self, angle, time_ms=1):
        Delta = (self.offset + angle * self.multiplier) - self.duty_u16

        for _ in range(time_ms):
            self.duty_u16 += (Delta / time_ms)
            # The servo should only be within the offset (minimum) and maximum
            if self.duty_u16 < self.offset:
                self.duty_u16 = self.offset
                print("Cannot turn anymore, preceeding offset")
                break
            if self.duty_u16 > self.maximum:
                self.duty_u16 = self.maximum
                print("Cannot turn anymore, exceeding maximum")
                break
            self.pwm.duty_u16(int(self.duty_u16))
            sleep(0.001)

        self.duty_u16 = int(self.duty_u16)

    def set_duty(self, cycle, time_ms=1):
        Delta = cycle - self.duty_u16

        for _ in range(time_ms):
            self.duty_u16 += (Delta / time_ms)
            # The servo should only be within the offset (minimum) and maximum
            if self.duty_u16 < self.offset:
                self.duty_u16 = self.offset
                print("Cannot turn anymore, preceeding offset")
                break
            if self.duty_u16 > self.maximum:
                self.duty_u16 = self.maximum
                print("Cannot turn anymore, exceeding maximum")
                break
            self.pwm.duty_u16(int(self.duty_u16))
            sleep(0.001)

        self.duty_u16 = int(self.duty_u16)


if __name__ == "__main__":

    grabber = Servo(15, 100, 2400, 4500)  # Servo 1, limits are the maximum we want it to turn
    # Open: Grabber at 2.4k
    # Closed: Grabber at 4.5k
    # Halfway: Grabber at 3.8k

    lifter = Servo(13, 100, 3700, 5000, 4000)  # Servo 2, limits around correct
    # Grabbing: Lifter at 3.7k
    # Driving: Lifter at 4k
    # Lifting: Lifter at 4.7k

    reset = 0
    if reset == 1:
        print("Reset all servos!")
    else:
        sleep(3)
        lifter.set_duty(3700, 100)
        sleep(0.1)
        grabber.set_duty(4500, 100)
        sleep(0.1)
        lifter.set_duty(5000, 100)
        sleep(1)
        # test_turn2(grabber)
        grabber.set_duty(3800, 100)
