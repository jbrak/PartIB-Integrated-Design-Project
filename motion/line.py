from hardware.line import LineSensorArray
from hardware.motor import Motors
from time import sleep

def straight_line(line_sensors: LineSensorArray, offsetP, offsetS, saturation=50, offset_step_up=1, offset_step_down=5):
    """Drive straight while both outer line sensors detect the line."""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    node_state = 0

    if (p, cp, cs, s) == (0, 1, 1, 0):
        print('Continuing straight line')
        if offsetP > 0:
            offsetP -= offset_step_down
        elif offsetP < 0:
            offsetP = 0

        if offsetS > 0:
            offsetS -= offset_step_down
        elif offsetS < 0:
            offsetS = 0

    elif ((cp == 1 or cs == 1) and (p == 1 or s == 1)):
        print('Reached node')
        node_state = 1

    elif (cp == 0 and cs == 0):
        print('Lost line')
        #motors.off()

    elif (p, cp, cs, s) == (0, 0, 1, 0):
        print('Port side lost line, attempting to correct')
        offsetP = 0
        offsetS += offset_step_up


    elif (p, cp, cs, s) == (0, 1, 0, 0):
        print('Starboard side lost line, attempting to correct')
        offsetP += offset_step_up
        offsetS = 0

    if offsetP > saturation:
        offsetP = saturation

    if offsetS > saturation:
        offsetS = saturation

    return offsetP, offsetS, node_state

def turn(line_sensors: LineSensorArray, speed):
    """turn at a node"""

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if cs == 1 and cs == 0:
        offsetP = 0
        offsetS = 0
        node_state = 0
    else:
        offsetP = speed / 2
        offsetS = 0
        node_state = 1

    return offsetP, offsetS, node_state