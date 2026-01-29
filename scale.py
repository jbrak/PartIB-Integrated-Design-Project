from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray, LineSensorArrayAlt
from motion.line import check_straight_line, check_straight_line_alt
from time import sleep

config = load_config()
motors = Motors(pDIR=config['motor']['port']['pinDIR'],
                pPWM=config['motor']['port']['pinPWM'],
                sDIR=config['motor']['starboard']['pinDIR'],
                sPWM=config['motor']['starboard']['pinPWM'])

# motors.forward(speed = speed)
sleep(5)
motors.off()

sScale = 1.05
pScale = 0.95
speed = 50

speedS = int(speed * sScale)
speedP = int(speed * pScale)

print('Initialized')
print('waiting 10 seconds')

# sleep(3)

motors.s.forward(speed=speedS)
motors.p.forward(speed=speedP)
print('running 10 seconds')
# motors.forward(speed = speed)
sleep(5)
print('turning off motors')
motors.off()

