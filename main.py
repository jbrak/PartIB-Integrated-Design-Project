from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray
from hardware.button import Button
from motion.line import straight_line, turn, startup, parking, bay_turning, reverse
from utime import sleep
from map.build_map import build_map
from map.robot import Robot
from map.map import *
from map.route import route

def main(motors, LineSensors, button:Button, map : Map, robot : Robot, key_nodes:[int]):
    motors.off()

    #input("Press Enter to continue...")

    # set speed from config
    speed = config["straights"]['speed']

    # initialize offsets
    offsetP = 0
    offsetS = 0
    node_state = 5 # 0: straight, 1: turning, 2: finishing turn
    prev_reading = {'p':0, 's':0}
    copy_key_nodes = key_nodes.copy()
    sequence = []
    pause_count = 0

    while True:
        if (button.toggle)%2 == 1:
            sensor_data = LineSensors.read_all()
            #print(f"left: {sensor_data['p']}, center-left: {sensor_data['cp']}, center-right: {sensor_data['cs']}, right: {sensor_data['s']}")

            if node_state == 0:
                offsetP, offsetS, node_state, prev_reading, pause_count = straight_line(LineSensors, offsetP, offsetS, prev_reading,pause_count,
                                                             saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'])
            elif node_state == -1:
                # reached node, calculate next action
                # if len(sequence) == 0:
                #     sequence = copy_sequence.copy()

                if len(sequence) > 0:
                    print("Normal Operation")
                    next_direction = sequence.pop(0)
                    turn_direction = robot.update_direction(next_direction)
                    robot.last_node_id = robot.next_node_id
                    robot.next_node_id = map.nodes.get(robot.next_node_id).connections.get(next_direction)

                    if type(map.nodes.get(robot.last_node_id)) == Bay and turn_direction in ['s','p']:
                        node_state = 9
                        count = 0
                    elif turn_direction == 's':
                        node_state = 3
                    elif turn_direction == 'p':
                        node_state = 1
                    else:
                        node_state = 0

                elif len(sequence) == 0 and len(key_nodes) > 0:
                    sequence += route(map, robot.next_node_id, key_nodes.pop(0))[1]
                elif len(sequence) == 0 and len(key_nodes) == 0:
                    #print("Sequence complete. Stopping robot.")
                    node_state = 7
                    count = 0

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
                offsetP, offsetS, node_state, prev_reading, count, pause_count = bay_turning(line_sensors=LineSensors, prev_reading=prev_reading, node_state = node_state, direction= robot.direction, speed = speed,
                                                            saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'], count = count, pause_count=pause_count)
                print(count)
            elif node_state in [1,2,3,4]:
                offsetP, offsetS, node_state = turn(LineSensors, speed, node_state, sf = config["turns"]["scale_factor"])
            elif node_state == 11 and type(map.nodes.get(robot.next_node_id)) == DeadEnd:
                offsetP, offsetS, node_state, prev_reading = reverse(LineSensors, offsetP, offsetS, prev_reading, speed=speed,
                                                             saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'])

                if node_state == -1:
                    robot.next_node_id = robot.last_node_id

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
                if type(map.nodes.get(robot.next_node_id)) == DeadEnd:
                    node_state = 11


            print(offsetP, offsetS, node_state)

        else:
            motors.off()
            robot = Robot(map, start_node_id=1, direction='n')
            sequence = []
            key_nodes = copy_key_nodes.copy()
            offsetP = 0
            offsetS = 0
            node_state = 5  # 0: straight, 1: turning, 2: finishing turn
            prev_reading = {'p': 0, 's': 0}

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

    print("Motors successfully initialized.")

    # initialize line sensor array (choose configuration based on config)
    # run checking function based on configuration
    LineSensors = LineSensorArray(
        p=config['lineSensor']['pinPort'],
        cp=config['lineSensor']['pinCenterPort'],
        cs=config['lineSensor']['pinCenterStarboard'],
        s=config['lineSensor']['pinStarboard']
    )

    map = build_map()

    key_nodes = [2,36,2]

    robot = Robot(map, start_node_id=1, direction='n')

    print("Line successfully initialized in configuration 0.")

    button = Button(pin = config['buttonPin'], debounce_ms=500)

    try:
        main(motors, LineSensors, button, map, robot, key_nodes)
    except KeyboardInterrupt:
        motors.off()
        raise KeyboardInterrupt

