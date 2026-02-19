from utime import sleep

def grab(motors, grabber, lifter):
    motors.s.forward(speed=80)
    motors.p.forward(speed=85)
    sleep(0.5)
    motors.off()
    lifter.set_duty(3700, 100)
    sleep(0.1)
    grabber.set_duty(4500, 100)
    sleep(0.1)
    lifter.set_duty(5000, 100)
    sleep(0.1)
    motors.s.reverse(speed = 80)
    motors.p.reverse(speed= 90)
    sleep(1)
    motors.off()

def drop(motors,grabber):
    motors.forward(speed=80)
    sleep(0.15)
    motors.off()
    sleep(0.1)
    grabber.set_duty(3800, 100)
    sleep(0.1)
    motors.s.reverse(speed=80)
    motors.p.reverse(speed=90)
    sleep(0.5)
    motors.off()

def home(grabber, lifter):
    grabber.zero_degrees()
    lifter.zero_degrees()
