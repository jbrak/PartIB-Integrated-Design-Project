from machine import Pin, PWM
from utime import sleep

class Servo:

    # Lets you control the servos easily
    
    def __init__(self, pin, freq, offset=2621, multiplier=50, calibrated=False):
        self.pwm = PWM(Pin(pin), freq)
        self.offset = int(offset) # offset for the PWM's 0 state
        self.duty_u16 = int(offset) # holds the PWM's duty cycle (starts at offset or 0 state)
        self.multiplier = multiplier # multiplier for angle -> u16 conversion
        if calibrated:
            self.duty_u16 = self.pwm.duty_u16()
        else:
            self.duty_u16 = int(offset)
        self.zero_degrees()
            
    
    def zero_degrees(self): # Sets the Servo to its 0 state
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

grabber = Servo(15, 100, calibrated=True)
lifter = Servo(13, 100)

def do_pwm():
    pwm1.duty_ns(int(2500))
    
    while True:
        # PWM the specified pin
        u16_level = int(65535 * level / 100)
        pwm_pin.duty_u16(u16_level)
    
        # update level and sleep
        print(f"Level={level}, u16_level={u16_level}, direction={direction}")
        level += direction
        if u16_level > 32000:
            direction = -1
        elif u16_level < 30000:
            direction = 1
        sleep(0.05)

def grab_old():
    level = 5  # 0-100
    direction = 1  # 1=up, -1=down
    
    counter = 0
    
    # PWM the specified pin
    u16_level = int(65535 * level / 100)
    grabber.duty_u16(u16_level)

    # update level and sleep
    print(f"Level={level}, u16_level={u16_level}, direction={direction}")
    
    if u16_level > 4000:
        sleep(3)
        direction = -1
    elif u16_level < 2000:
        sleep(3)
        direction = 1
    sleep(0.5)
    counter = counter + 1
    
    level += direction
    # PWM the specified pin
    u16_level = int(65535 * level / 100)
    pwm1.duty_u16(u16_level)

def grab():
    grabber.turn(30)
    sleep(3)
    grabber.turn(-30)

def lift():
    lifter.turn(20, 500)

if __name__ == "__main__":
    #grab()
    #sleep(3)
    #lift()
    pass