from machine import Pin, PWM
from utime import sleep

class Servo:

    # Lets you control the servos easily
    def __init__(self, pin, freq, offset=0, maximum=20000):
        self.pwm = PWM(Pin(pin), freq)
        self.multiplier = 47.8 # multiplier for angle -> u16 conversion. Tested angle, accurate enough
        self.offset = int(offset)
        self.maximum = int(maximum)
        self.zero_degrees()
        self.duty_u16 = self.pwm.duty_u16()
        
    def zero_degrees(self): # Sets the Servo to its 0 state
        self.pwm.duty_u16(self.offset)

    def turn_angle(self, angle, t_ms=1): 
        # Turns (around) the angle in degrees you ask
        # +ve is anticlockwise looking towards the servo's rotator
        # Can also specify the time in which you want the servo to rotate the angle
        #  just in case you don't want to fling something
        for _ in range(t_ms):
            self.duty_u16 += (angle * self.multiplier / t_ms)
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
    
    def turn_duty(self, cycle):
        self.duty_u16 += int(cycle)
        self.pwm.duty_u16(self.duty_u16)

grabber = Servo(15, 100, 2400, 15000) # Servo 1, limits are the absolute limits of the servo
lifter = Servo(13, 100, 2500, 6000) # Servo 2, limits around correct

def grab():
    grabber.turn_angle(30)
    sleep(3)
    grabber.turn_angle(-30)

def lift(time_ms=500):
    lifter.turn_angle(20, time_ms)
    
def calibrate(servo):
    print("Make sure that nothing can break")
    print("Press to make sure that nothing can break")
    input()
    print("Zeroing servo...")
    servo.zero_degrees()
    sleep(1)
    print("The servo will increment its pwm")
    print("Type \"y\" in the input when you can see it move")
    
    x = ""
    while x == "":
        servo.turn_duty(200)
        x = input()
    servo.turn_duty(-200)
    
    print("The servo will now turn in smaller increments")
    print("Keep typing \"y\" in the input when you can see it move")
    sleep(1)
    
    x = ""
    while x == "":
        servo.turn_duty(20)
        x = input()
    servo.turn_duty(-20)
    sleep(1)
    
    x = ""
    while x == "":
        servo.turn_duty(1)
        x = input()
    sleep(1)
    
    print("Your zero is: ", servo.duty_u16)
    print("Set this as your offset for this servo")
    
def turn(servo):
    x = ""
    while x == "":
        servo.turn_duty(20)
        print(servo.duty_u16)
        sleep(0.1)
    

if __name__ == "__main__":
    turn(lifter)
    