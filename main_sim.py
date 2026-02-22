from simulator.draw import *
from map.robot import *
from map.build_map import build_map
import turtle as ttl
from map.route import route

key_nodes = [1,35,15,1]
s = ['n']

map = build_map()

# Ensure the map is consistent
map.assert_consistent()

robot = Robot(map, start_node_id=key_nodes.pop(0), direction=s.pop(0))

# Initialize the simulator
map, robot = initialize_simulator(map, robot, LENGTH=40, start_pos=(0,-283))

while True:

    if sim_check_node(robot, map):
        if len(s) == 0 and len(key_nodes) > 0:

            s += route(map, robot.next_node_id, key_nodes.pop(0))[1]
            print("New route:", s)
        elif len(s) == 0 and len(key_nodes) == 0:
            print("Route complete")
            break
        next_direction = s.pop(0)
        robot.direction = next_direction
        robot.last_node_id = robot.next_node_id
        robot.next_node_id = map.nodes.get(robot.next_node_id).connections.get(next_direction)
        sim_turn(robot)
        print(f"Direction: {robot.direction}, {robot.last_node_id} --> {robot.next_node_id}")
    else:
        sim_move(robot)

# Finalize the simulator
finalize_simulator()