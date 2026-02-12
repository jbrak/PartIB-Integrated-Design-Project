from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray
from hardware.button import Button
from hardware.grabber import *
from hardware.box import DistanceSensor
from motion.line import straight_line, turn, startup, parking, bay_turning, reverse
from motion.pathfinding import *
import utime
from map.build_map import build_map
from map.robot import Robot
from map.map import *
from machine import Pin

"""
status:
101: Initializing, detecting empty spaces
102: picking up coil, measure resistance
103: dropping off coil in relevent bay
104: going home
"""


def main(motors, LineSensors, button:Button, map : Map, robot : Robot, upper : Upper, lower : Lower):
    motors.off()

    #input("Press Enter to continue...")

    # set speed from config
    speed = config["straights"]['speed']

    # initialize offsets
    offsetP = 0
    offsetS = 0
    node_state = 5 # 0: straight, 1: turning, 2: finishing turn
    prev_reading = {'p':0, 's':0}
    sequence = []
    pause_count = 0
    status = 101
    key_nodes = KeyNodes()
    turn_count = 0
    missed_count = 0

    TARGET_HZ = 2000
    PERIOD_US = 1_000_000 // TARGET_HZ

    next_tick = utime.ticks_add(utime.ticks_us(), PERIOD_US)

    for i in key_nodes.led_pin_lookup.values():
        Pin(i, Pin.OUT).value(1)
        utime.sleep(0.5)
        Pin(i, Pin.OUT).value(0)

    while True:
        if (button.toggle)%2 == 1:

            now = utime.ticks_us()
            remaining = utime.ticks_diff(next_tick, now)
            if remaining > 0:
                utime.sleep_us(remaining)

            next_tick = utime.ticks_add(next_tick, PERIOD_US)

            sensor_data = LineSensors.read_all()
            #print(f"left: {sensor_data['p']}, center-left: {sensor_data['cp']}, center-right: {sensor_data['cs']}, right: {sensor_data['s']}")

            if node_state == 0:
                offsetP, offsetS, node_state, prev_reading, pause_count = straight_line(LineSensors, offsetP, offsetS, prev_reading,pause_count,
                                                             saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'])
                if missed_count > 0:
                    node_state = 0

            elif node_state == -1 and not (missed_count > 0 and robot.direction == "s"):
                # reached node, calculate next action
                # if len(sequence) == 0:
                #     sequence = copy_sequence.copy()

                if len(sequence) > 0:
                    turn_count = 0
                    if len(sequence) > 0:
                        if sequence[0] == "s":
                            for bays in key_nodes.bays.values():
                                #print(bays)
                                # for node in bays:
                                #     print(node, list(map.nodes.get(node).connections.values())[0], robot.last_node_id)
                                #     if list(map.nodes.get(node).connections.values())[0] == robot.last_node_id:
                                if robot.last_node_id in bays:
                                    Pin(11, Pin.OUT).value(1)
                                    turn_count = 1750

                    next_direction = sequence.pop(0)
                    turn_direction = robot.update_direction(next_direction)
                    robot.last_node_id = robot.next_node_id
                    robot.next_node_id = map.nodes.get(robot.next_node_id).connections.get(next_direction)

                    if type(map.nodes.get(robot.last_node_id)) == Bay and turn_direction in ['s','p'] and robot.direction in ['w', 'e']:
                        node_state = 9
                        count = 1
                        turn_count = 500
                    elif turn_direction == 's':
                        node_state = 3
                    elif turn_direction == 'p':
                        node_state = 1
                    elif turn_direction == 'b':
                        node_state = 11
                        count = 1
                    else:
                        node_state = 0

                    print("--------------------------------")
                    print(turn_direction)
                    print("NODE STATE",node_state)
                    print(robot.direction)
                    print("prev:", robot.last_node_id)
                    print("next:", robot.next_node_id)
                    print(sequence)

                elif len(sequence) == 0 and status == 105:
                    node_state = 7
                    count = 0

                elif len(sequence) == 0:
                    #print("Sequence complete. Stopping robot.")
                    sequence, status, pause_count = next_node(map, status, pause_count, robot.next_node_id, key_nodes, upper, lower)

                    print(status, sequence)

                    if status == 102 and len(sequence) > 0:
                        souths = 0
                        for bays in key_nodes.bays.values():
                            if robot.next_node_id in bays:
                                bays = sorted(bays)
                                souths = bays.index(robot.next_node_id)
                                robot.next_node_id = bays[0]
                                #robot.next_node_id = list(map.nodes.get(bays[0]).connections.values())[0]
                                break

                        for j in range(souths):
                            sequence.pop(1)

                        missed_count = 1300*souths
                        print(missed_count)




            elif node_state == 5 or node_state == 6:
                node_state, prev_reading = startup(LineSensors, node_state, prev_reading)
            elif node_state == 7 or node_state == 8:
                #print("node_state:", node_state)
                #print("count:", count)
                offsetP, offsetS, node_state, count = parking(LineSensors, speed, node_state, robot.direction, count, sf=config["turns"]["scale_factor"])

                if node_state == 0:
                    #print("Toggle Button")
                    button.toggle += 1
            elif node_state == 9 or node_state==10:
                offsetP, offsetS, node_state, prev_reading, count, pause_count, turn_count = bay_turning(line_sensors=LineSensors, prev_reading=prev_reading, node_state = node_state, direction= robot.direction, speed = speed,
                                                            saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'], count = count, pause_count=pause_count, turn_count=turn_count)
                #print(count)
            elif node_state in [1,2,3,4]:
                offsetP, offsetS, node_state, turn_count, pause_count = turn(LineSensors, speed, node_state, pause_count =pause_count, sf = config["turns"]["scale_factor"], turn_count = turn_count)

            elif (node_state == 11):
                if type(map.nodes.get(robot.last_node_id)) == DeadEnd:
                    offsetP, offsetS, node_state, prev_reading, pause_count = reverse(LineSensors, offsetP, offsetS, prev_reading, speed=speed,
                                                             saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'], pause_count=pause_count)

                else:

                    current_node = map.nodes.get(robot.last_node_id)

                    for i in current_node.connections.keys():
                        if i not in ['n', 's']:
                            direction_temp = i

                    turn_count = 0

                    offsetP, offsetS, node_state, prev_reading, count, pause_count, turn_count = bay_turning(
                        line_sensors=LineSensors, prev_reading=prev_reading, node_state=10,
                        direction=direction_temp, speed=speed,
                        saturation=config["straights"]['saturation'],
                        offset_step_up=config["straights"]['offset_step_up'],
                        offset_step_down=config["straights"]['offset_step_down'], count = count, pause_count=pause_count, turn_count=turn_count)

                    if node_state == 10:
                        node_state = 11
                    else:
                        if robot.direction == 's':
                            robot.direction = 'n'
                        else:
                            robot.direction = 's'

                    offsetS, offsetP = offsetP, offsetS

            if pause_count == 0:
                if offsetP <= speed:
                    motors.p.forward(speed, offset=offsetP)
                elif offsetP == 3*speed:
                    motors.s.off()
                elif offsetP > speed:
                    motors.p.reverse(speed, offset=(speed*2-offsetP))


                if offsetS <= speed:
                    motors.s.forward(speed, offset=offsetS)
                elif offsetS == 3*speed:
                    motors.s.off()
                elif offsetS > speed:
                    motors.s.reverse(speed, offset=(speed*2-offsetS))

            else:
                motors.p.off()
                motors.s.off()
                pause_count -= 1

                if status == 102:
                    ## Code for picking up coil
                    pause_count = pick_up_coil(pause_count)
                elif status == 104 and len(sequence) == 0:
                    ## Code for releasing coil
                    pause_count = drop_off_coil(pause_count)

                ### This should be within a separate reverse function - the robot detects in neds to travel backwards and does so
                if type(map.nodes.get(robot.next_node_id)) == DeadEnd and node_state == -2:
                    node_state = -1

            #print(offsetP, offsetS, node_state)

            if missed_count > 0 and robot.direction == "s" and pause_count == 0:
                missed_count -= 1
                Pin(14, Pin.OUT).value(1)
            elif missed_count == 0:
                Pin(14, Pin.OUT).value(0)

        else:
            motors.off()
            robot = Robot(map, start_node_id=1, direction='n')
            offsetP = 0
            offsetS = 0
            node_state = 5  # 0: straight, 1: turning, 2: finishing turn
            prev_reading = {'p': 0, 's': 0}
            sequence = []
            pause_count = 0
            status = 101
            key_nodes = KeyNodes()
            turn_count = 0
            missed_count = 0

        #print(f"p: {offsetP},s:{offsetS}, node-state: {node_state}, toggle: {button.toggle}")

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

    grabber = Servo(15, 100)
    lifter = Servo(13, 100)

    # initialize line sensor array (choose configuration based on config)
    # run checking function based on configuration
    LineSensors = LineSensorArray(
        p=config['lineSensor']['pinPort'],
        cp=config['lineSensor']['pinCenterPort'],
        cs=config['lineSensor']['pinCenterStarboard'],
        s=config['lineSensor']['pinStarboard']
    )

    upper = DistanceSensor(sda = config['box']['upper']['sda'], scl = config['box']['upper']['scl'])
    lower = DistanceSensor(sda = config['box']['lower']['sda'], scl = config['box']['lower']['scl'])

    map = build_map()

    robot = Robot(map, start_node_id=1, direction='n')

    #print("Line successfully initialized in configuration 0.")

    button = Button(pin = config['buttonPin'], debounce_ms=500)

    try:
        main(motors, LineSensors, button, map, robot, upper, lower)
    except KeyboardInterrupt:
        motors.off()
        raise KeyboardInterrupt

