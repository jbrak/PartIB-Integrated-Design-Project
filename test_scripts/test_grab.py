from hardware.grabber import Servo
from motion.grabber import grab, drop, home
from hardware.motor import Motors
from config.config import load_config
from utime import sleep
from motion.pathfinding import measure_coil, KeyNodes
from machine import Pin

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

    key_nodes = KeyNodes()

    pause_count = 0

    home(grabber, lifter)
    try:
        grab(motors, grabber, lifter)
        res = None
        while res is None:
            pause_count, res = measure_coil(key_nodes, pause_count = pause_count)
            pause_count = pause_count - 1

        print(res)

        drop(grabber)

        sleep(1)

        home(grabber, lifter)

        for i in key_nodes.led_pin_lookup.values():
            Pin(i, Pin.OUT).value(0)

    except KeyboardInterrupt:
        drop(grabber)

        sleep(1)

        home(grabber, lifter)

        for i in key_nodes.led_pin_lookup.values():
            Pin(i, Pin.OUT).value(0)


