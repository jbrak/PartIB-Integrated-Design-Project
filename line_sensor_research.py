from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray, LineSensorArrayAlt
from motion.line import check_straight_line, check_straight_line_alt

def main():
    # read configuration file
    config = load_config()

    # initialize motors
    motors = Motors(pDIR = config['motors']['port']['pinDIR'],
                    pPWM = config['motors']['port']['pinPWM'],
                    sDIR = config['motors']['starboard']['pinDIR'],
                    sPWM = config['motors']['starboard']['pinPWM'])

    print("Motors successfully initialized.")



    # initialize line sensor array (choose configuration based on config)
    # run checking function based on configuration
    if config['altArray'] == 0:
        LineSensors = LineSensorArray(
            p=config['lineSensor']['pinPort'],
            cp=config['lineSensor']['pinCenterPort'],
            cs=config['lineSensor']['pinCenterStarboard'],
            s=config['lineSensor']['pinStarboard']
        )

        print("Line successfully initialized in configuration 0.")

        input("Press Enter to continue...")

        motors.forward()

        while True:
            check_straight_line(motors, LineSensors, t="Test 0")

    elif config['altArray'] == 1:
        LineSensors = LineSensorArrayAlt(
            p=config['lineSensor']['pinPort'],
            f=config['lineSensor']['pinFront'],
            b=config['lineSensor']['pinBack'],
            s=config['lineSensor']['pinStarboard']
        )
        print("Line successfully initialized in configuration 1. (alternative)")

        input("Press Enter to continue...")

        motors.forward()

        while True:
            check_straight_line_alt(motors, LineSensors, t="Test 0")

    else:
        raise ValueError("Invalid altArray configuration value. Must be 0 or 1.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
