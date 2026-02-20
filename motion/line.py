from hardware.line import LineSensorArray
from hardware.motor import Motors
from time import sleep
from machine import Pin

"""
Node states:
-2 : lost line, proceed with next action
-1 : reached node, calculate next action
0 : driving straight
1 : turning port
2 : finishing port turn
3 : turning starboard
4 : finishing starboard turn
5 : initial alignment at startup
6 : finishing initial alignment at startup
7 : parking maneuver - moving forward
8 : parking maneuver - turning into bay
9 : bay turning - detecting next line
10 : bay turning - executing turn
11 : Reversing out of dead end
"""

def straight_line(line_sensors: LineSensorArray, offsetP, offsetS, prev_reading, pause_count, saturation=50, offset_step_up=1, offset_step_down=5):
    """
    Drive straight while both outer line sensors detect the line.
    Returns the 2 offsets, node state, line sensor data and updated pause count.
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    offsetP : int
        Controls the operation of the port motor
    offsetS : int
        Controls the operation of the starboard motor
    prev_reading : dict
        The previous 4 saved readings from the line sensor
    pause_count : int
        Pads out other count variables to make them take longer
    saturation : int, optional
        Maximum offset for the specific straight line being followed (Default = 50)
    offset_step_up : int, optional
        The value to step up the offset whenever the robot needs to turn (Default = 1)
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    prev_p = prev_reading.get('p')
    prev_s = prev_reading.get('s')
    prev_cp = prev_reading.get('cp')
    prev_cs = prev_reading.get('cs')

    node_state = 0

    if (p, cp, cs, s) == (0, 1, 1, 0):
        #print('Continuing straight line')

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

    elif (cp == 0 and cs == 0) and (prev_cp == 1 or prev_cs == 1):
        #print('Lost line')
        #motors.off()

        pause_count += 1

        if offsetP > 0:
            offsetP = 300
            offsetS = 0

        elif offsetS > 0:
            offsetS = 300
            offsetP = 0


        return  offsetP,offsetS ,-2, line_data, 100

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

    return offsetP, offsetS, node_state, line_data, pause_count

def turn(line_sensors: LineSensorArray, speed, node_state, pause_count, sf:float=0.83333, turn_count=0):
    """
    Turn at a node. Returns the 2 offsets, node state, and the updated turn count and pause count.
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    speed : int
        The current speed of the robot
    node_state : int
        The "action regime" that the robot is in 
    pause_count : int
        Pads out other count variables to make them take longer
    sf : int, optional
        Speed factor, the fraction of speed that should be the new offset (Default = 0.83333)
    turn_count : int, optional
        The value to step up the offset whenever the robot needs to turn (Default = 0)
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    if turn_count > 0 and pause_count==0:
        turn_count -= 1
    elif turn_count==0:
        #Pin(11, Pin.OUT).value(0)
        pass

    #print(turn_count)

    if (cs == 0 or cp == 0) and (node_state == 1 or node_state == 3):
        offset = sf*speed
        node_state += 1
    elif (cs == 1 or cp == 1) and (node_state == 2 or node_state == 4) and (s == 0 and p == 0) and turn_count == 0:
        return 0,0,0,0,0
    else:
        offset = sf*speed

    if node_state == 1 or node_state == 2:
        return offset,0, node_state, turn_count, pause_count
    elif node_state == 3 or node_state == 4:
        return 0, offset, node_state, turn_count, pause_count

def startup(line_sensors: LineSensorArray, node_state, prev_reading):
    """
    Initial alignment at startup. Returns the new node state and the line sensor data.
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    node_state : int
        The "action regime" that the robot is in
    prev_reading : dict
        The previous 4 saved readings from the line sensor
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    prev_p = prev_reading.get('p')
    prev_s = prev_reading.get('s')
    prev_cp = prev_reading.get('cp')
    prev_cs = prev_reading.get('cs')

    if ((cs == 1 and p == 1) and (prev_cs ==0 or prev_p == 0)):
        if node_state == 5:
            node_state += 1
        elif node_state == 6:
            node_state = -1

    return node_state, line_data

def parking(line_sensors: LineSensorArray, speed, node_state, direction,count,sf:float=0.83333):
    """
    Parking maneuver at the end of the course. Returns the 2 offsets, node state and count
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    speed : int
        The current speed of the robot
    node_state : int
        The "action regime" that the robot is in 
    direction : str
        Cardinal direction that the robot needs to move in
    count : int
        count
    sf : int, optional
        Speed factor, the fraction of speed that should be the new offset (Default = 0.83333)
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    count += 1

    if node_state == 7:
        offset = sf*speed

        if s ==0 and p ==0 and cp ==0 and cs ==0 and count>=800:
            node_state += 1
            count = 0

    elif node_state == 8:
        offset = 0 #(1 - sf) * speed

    if count >= 200 and node_state == 8:
        return 0,0,0,count
    else:
        if direction == 'e':
            return 0,offset, node_state, count
        elif direction == 'w':
            return offset, 0, node_state, count
        else:
            return 0,0,0,count

def bay_turning(line_sensors: LineSensorArray, node_state, prev_reading, direction, count,pause_count, turn_count, speed, saturation, offset_step_up, offset_step_down):
    """
    Bay turning maneuver at dead-end nodes
    Returns the 2 offsets, the node states, line sensor data, and the 3 counts that were passed in
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    node_state : int
        The "action regime" that the robot is in 
    prev_reading : dict
        The previous 4 saved readings from the line sensor
    direction : str
        Cardinal direction that the robot needs to move in
    count : int
        count
    pause_count : int
        Pads out other count variables to make them take longer
    turn_count : int
        The value to step up the offset whenever the robot needs to turn
    speed : int
        The current speed of the robot
    saturation : int
        Maximum offset for the specific straight line being followed
    offset_step_up : int
        The value to step up the offset whenever the robot needs to turn
    offset_step_down : int
        The value to step down the offset whenever the robot needs to turn
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    prev_cp = prev_reading.get('cp')
    prev_cs = prev_reading.get('cs')
    prev_p = prev_reading.get('p')
    prev_s = prev_reading.get('s')

    offsetP = 0
    offsetS = 0

    if p == 1 and prev_p == 0 and direction == 'w':
        count += 1

    if s == 1 and prev_s == 0 and direction == 'e':
        count += 1

    if node_state == 9:
        offsetP, offsetS, node_state_temp, line_data, pause_count = straight_line(line_sensors, offsetP, offsetS, prev_reading,pause_count, saturation, offset_step_up, offset_step_down)

        if node_state_temp == -1:
            node_state += 1
            pause_count = 25 #102

    elif node_state == 10:

        if turn_count > 0:
            turn_count -= 1

        if (cs == 1 and cp == 1) and (prev_cp == 0 or prev_cs == 0) and count >= 2 and turn_count == 0:
            node_state = 0

        if direction == 'w':
            if node_state == 0:
                offsetP = 0
                offsetS = 3*speed
            else:
                offsetP = speed*2
                offsetS = 0


        elif direction == 'e':
            if node_state == 0:
                offsetP = 3*speed
                offsetS = 0
            else:
                offsetP = 0
                offsetS = speed*2


    return offsetP, offsetS, node_state, line_data, count, pause_count, turn_count

def reverse(line_sensors: LineSensorArray, offsetP, offsetS, prev_reading,speed, pause_count, saturation=50, offset_step_up=1, offset_step_down=5):
    """
    Reverses the robot
    
    Parameters
    ----------
    line_sensors : LineSensorArray
        All 4 line sensors and their states
    offsetP : int
        Controls the operation of the port motor
    offsetS : int
        Controls the operation of the starboard motor
    prev_reading : dict
        The previous 4 saved readings from the line sensor
    speed : int
        The current speed of the robot
    pause_count : int
        Pads out other count variables to make them take longer
    saturation : int
        Maximum offset for the specific straight line being followed (Default = 50)
    offset_step_up : int
        The value to step up the offset whenever the robot needs to turn (Default = 1)
    offset_step_down : int
        The value to step down the offset whenever the robot needs to turn (Default = 5)
    """

    line_data = line_sensors.read_all()
    p = line_data.get('p')
    cp = line_data.get('cp')
    cs = line_data.get('cs')
    s = line_data.get('s')

    offsetP, offsetS, node_state, line_data, pause_count = straight_line(line_sensors, offsetP, offsetS, prev_reading,pause_count, saturation, offset_step_up, offset_step_down)

    if node_state == 0:
        node_state = 11
    elif node_state == -1:
        pause_count = 100 # 1000

    if (p, cp, cs, s) == (1, 1, 1, 1) or (p, cp, cs, s) == (0, 0, 0, 0):
        offsetP = 0
        offsetS = 0

    # if offsetP != 0 :
    #     offsetP = saturation
    #
    # if offsetS != 0 :
    #     offsetS = saturation

    return (2*speed-offsetS), (2*speed-offsetP), node_state, line_data, pause_count
