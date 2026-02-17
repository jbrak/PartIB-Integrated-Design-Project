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

def drop(motors,grabber):
    motors.forward(speed=80)
    sleep(0.15)
    motors.off()
    sleep(0.1)
    grabber.set_duty(3800, 100)
    sleep(0.1)
    motors.reverse(speed=80)
    sleep(0.5)
    motors.off()

def home(grabber, lifter):
    grabber.zero_degrees()
    lifter.zero_degrees()
