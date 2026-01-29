from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray
from hardware.button import Button
from motion.line import check_straight_line
from utime import sleep

def main(motors, LineSensors, button:Button):
    motors.off()

    #input("Press Enter to continue...")

    speed = 100
    offsetP = 0
    offsetS = 0

    while True:
        print(button.toggle)
        if (button.toggle)%2 == 1:
            offsetP, offsetS = check_straight_line(motors, LineSensors, offsetP, offsetS)
            sensor_data = LineSensors.read_all()
            print(
                 f"left: {sensor_data['p']}, center-left: {sensor_data['cp']}, center-right: {sensor_data['cs']}, right: {sensor_data['s']}")
            motors.p.forward(speed, offset=offsetP)
            motors.s.forward(speed, offset=offsetS)
        else:
            motors.off()

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

    print("Motors successfully initialized.")

    # initialize line sensor array (choose configuration based on config)
    # run checking function based on configuration
    LineSensors = LineSensorArray(
        p=config['lineSensor']['pinPort'],
        cp=config['lineSensor']['pinCenterPort'],
        cs=config['lineSensor']['pinCenterStarboard'],
        s=config['lineSensor']['pinStarboard']
    )

    print("Line successfully initialized in configuration 0.")

    button = Button(pin = config['buttonPin'], debounce_ms=500)

    try:
        main(motors, LineSensors, button)
    except KeyboardInterrupt:
        motors.off()
        raise KeyboardInterrupt

