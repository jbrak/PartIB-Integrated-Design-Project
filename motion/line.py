from hardware.line import LineSensorArray, LineSensorArrayAlt
from hardware.motor import Motors
from time import sleep

def check_straight_line(motors:Motors, line_sensors: LineSensorArray, offsetP:int=0, offsetS:int=0):
    """Drive straight while both outer line sensors detect the line."""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if (p, cp, cs, s) == (0, 1, 1, 0):
        print(f'Continuing straight line')
        motors.forward(speed=100)
        if offsetP > 0:
            offsetP -= 2
        elif offsetP < 0:
            offsetP = 0

        if offsetS > 0:
            offsetS -= 2
        elif offsetS < 0:
            offsetS = 0

    elif ((cp == 1 or cs == 1) and (p == 1 or s == 1)):
        print(f'Reached node, stopping')
        motors.off()

    elif (cp == 0 and cs == 0):
        print(f'Lost line, stopping')
        motors.off()

    elif (p, cp, cs, s) == (0, 0, 1, 0):
        print(f'Port side lost line, attempting to correct')
        offsetP = 0
        offsetS += 1


    elif (p, cp, cs, s) == (0, 1, 0, 0):
        print(f'Starboard side lost line, attempting to correct')
        motors.off()
        offsetS += 1
        offsetP = 0

    if offsetP > 10:
        offsetP = 10

    if offsetS > 10:
        offsetS = 10

    return offsetP, offsetS

