from hardware.line import LineSensorArray
from hardware.motor import Motors
from time import sleep
"""
Node states:
-1 : reached node, calcualte next action
0 : driving straight
1 : turning port
2 : finishing port turn
3 : turning starboard
4 : finishing starboard turn
5 : initial alignment at startup
6: finishing initial alignment at startup
"""
def straight_line(line_sensors: LineSensorArray, offsetP, offsetS, prev_reading, saturation=50, offset_step_up=1, offset_step_down=5):
    """Drive straight while both outer line sensors detect the line."""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    prev_p = prev_reading.get('p')
    prev_s = prev_reading.get('s')

    node_state = 0

    if (p, cp, cs, s) == (0, 1, 1, 0):
        print('Continuing straight line')

        offsetP =0
        offsetS = 0

        # if offsetP > 0:
        #     offsetP -= offset_step_down
        # elif offsetP < 0:
        #     offsetP = 0
        #
        # if offsetS > 0:
        #     offsetS -= offset_step_down
        # elif offsetS < 0:
        #     offsetS = 0

    # elif ((cp == 1 or cs == 1) and (p == 1)):
    #     print('Reached node')
    #     node_state = 1
    #
    # elif ((cp == 1 or cs == 1) and (s == 1)):
    #     print('Reached node')
    #     node_state = 3

    elif ((cp == 1 or cs == 1) and (p == 1 or s == 1)) and (prev_p == 0 and prev_s == 0):
        #print('Reached node')
        node_state = -1

    elif (cp == 0 and cs == 0):
        #print('Lost line')
        #motors.off()
        pass

    elif (p, cp, cs, s) == (0, 0, 1, 0):
        #print('Port side lost line, attempting to correct')
        offsetP = 0
        offsetS += offset_step_up


    elif (p, cp, cs, s) == (0, 1, 0, 0):
        #print('Starboard side lost line, attempting to correct')
        offsetP += offset_step_up
        offsetS = 0

    if offsetP > saturation:
        offsetP = saturation

    if offsetS > saturation:
        offsetS = saturation

    return offsetP, offsetS, node_state, line_data

def turn(line_sensors: LineSensorArray, speed, node_state, sf:float=0.83333):
    """turn at a node"""

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if cs == 0 and cp == 0 and (node_state == 1 or node_state == 3):
        offset = sf*speed
        node_state += 1
    elif cs == 1 and cp == 1 and (node_state == 2 or node_state == 4):
        return 0,0,0
    else:
        offset = sf*speed

    if node_state == 1 or node_state == 2:
        return offset,0, node_state
    elif node_state == 3 or node_state == 4:
        return 0, offset, node_state

def startup(line_sensors: LineSensorArray, node_state, prev_reading):
    """Initial alignment at startup"""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    prev_p = prev_reading.get('p')
    prev_s = prev_reading.get('s')

    if s == 1 and p == 1 and (prev_p == 0 or prev_s == 0):
        if node_state == 5:
            node_state += 1
        elif node_state == 6:
            node_state = -1

    return node_state, line_data

def parking(line_sensors: LineSensorArray, speed, node_state, direction,count,sf:float=0.83333):
    """Parking maneuver at the end of the course"""
    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if node_state == 7:
        offset = sf*speed

        if s ==0 and p ==0 and cp ==0 and cs ==0:
            node_state += 1

    elif node_state == 8:
        count += 1
        offset = (1 - sf) * speed

    if count >= 2000:
        return 0,0,0,count
    else:
        if direction == 'e':
            return 0,offset, node_state, count
        elif direction == 'w':
            return offset, 0, node_state, count
        else:
            return 0,0,0,count
