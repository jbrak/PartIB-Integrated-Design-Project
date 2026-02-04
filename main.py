from config.config import load_config
from hardware.motor import Motors
from hardware.line import LineSensorArray
from hardware.button import Button
from motion.line import straight_line, turn, startup, parking
from utime import sleep
from map.build_map import build_map
from map.robot import Robot
from map.map import Map
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

    while True:
        if (button.toggle)%2 == 1:
            sensor_data = LineSensors.read_all()
            #print(f"left: {sensor_data['p']}, center-left: {sensor_data['cp']}, center-right: {sensor_data['cs']}, right: {sensor_data['s']}")

            if node_state == 0:
                offsetP, offsetS, node_state, prev_reading = straight_line(LineSensors, offsetP, offsetS, prev_reading,
                                                             saturation=config["straights"]['saturation'],
                                                             offset_step_up=config["straights"]['offset_step_up'],
                                                             offset_step_down=config["straights"]['offset_step_down'])
            elif node_state == -1:
                # reached node, calculate next action
                # if len(sequence) == 0:
                #     sequence = copy_sequence.copy()

                if len(sequence) > 0:
                    next_direction = sequence.pop(0)
                    turn_direction = robot.update_direction(next_direction)
                    robot.last_node_id = robot.next_node_id
                    robot.next_node_id = map.nodes.get(robot.next_node_id).connections.get(next_direction)

                    if turn_direction == 's':
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
                offsetP, offsetS, node_state, count = parking(LineSensors, speed, node_state, robot.direction, count)

                if node_state == 0:
                    #print("Toggle Button")
                    button.toggle += 1
            else:
                offsetP, offsetS, node_state = turn(LineSensors, speed, node_state)

            motors.p.forward(speed, offset=offsetP)
            motors.s.forward(speed, offset=offsetS)



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

    key_nodes = [2,35,15,2]

    robot = Robot(map, start_node_id=1, direction='n')

    print("Line successfully initialized in configuration 0.")

    button = Button(pin = config['buttonPin'], debounce_ms=500)

    try:
        main(motors, LineSensors, button, map, robot, sequence)
    except KeyboardInterrupt:
        motors.off()
        raise KeyboardInterrupt

