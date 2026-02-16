from hardware.grabber import Servo
from motion.grabber import grab, drop, home
from hardware.motor import Motors
from config.config import load_config
from utime import sleep

if __name__ == '__main__':
    # read configuration file
    config = load_config()

    # initialize motors
    motors = Motors(pDIR = config['motor']['port']['pinDIR'],
                    pPWM = config['motor']['port']['pinPWM'],
                    sDIR = config['motor']['starboard']['pinDIR'],
                    sPWM = config['motor']['starboard']['pinPWM'],
                    sdrift_compensation=config['motor']['starboard']['driftCompensation'],
                    pdrift_compensation=config['motor']['port']['driftCompensation'])

    grabber = Servo(15, 100, 2400, 4500)

    lifter = Servo(13, 100, 3700, 5000, 4000)

    grab(motors, grabber, lifter)

    sleep(1)

    drop(grabber)

    sleep(1)

    home(grabber, lifter)


