from utime import sleep

def grab(motors, grabber, lifter):
    motors.forward(speed=80)
    sleep(0.5)
    motors.off()
    lifter.set_duty(3700, 100)
    sleep(0.1)
    grabber.set_duty(4500, 100)
    sleep(0.1)
    lifter.set_duty(5000, 100)
    sleep(0.1)

def drop(grabber):
    grabber.set_duty(3800, 100)

def home(grabber, lifter):
    grabber.zero_degrees()
    lifter.zero_degrees()
