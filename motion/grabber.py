from utime import sleep

def grab(motors, grabber, lifter):
    """
    Set of instructions that the robot goes through to grab a coil
    
    Parameters
    ----------
    motors : Motors
        The motors controlling how the robot moves 
    grabber : Servo
        The servo motor responsible for grabbing coils
    lifter : Servo
        The servo motor responsible for lifting coils
    """
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
    """
    Set of instructions that the robot goes through to drop a coil
    
    Parameters
    ----------
    motors : Motors
        The motors controlling how the robot moves 
    grabber : Servo
        The servo motor responsible for grabbing coils
    """
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
    """
    Set of instructions that the robot goes through to go into its "home" state.
    It will normally drive in this state
    
    Parameters
    ----------
    grabber : Servo
        The servo motor responsible for grabbing coils
    lifter : Servo
        The servo motor responsible for lifting coils
    """
    grabber.zero_degrees()
    lifter.zero_degrees()
