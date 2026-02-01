from simulator.draw import *
from map.robot import *
from map.build_map import build_map
import turtle as ttl

s = ['n','e','e','n','n','n','n','n','n','n','n', 'w', 'w', 's','s','s','s','s','s','s','s','e','e','s']

map = build_map()

# Ensure the map is consistent
map.assert_consistent()

robot = Robot(map, start_node_id=1, direction=s.pop(0))

# Initialize the simulator
map, robot = initialize_simulator(map, robot, LENGTH=50, start_pos=(0,-400))

while True:

    if sim_check_node(robot, map):
        if len(s) == 0:
            break
        next_direction = s.pop(0)
        robot.direction = next_direction
        robot.last_node_id = robot.next_node_id
        robot.next_node_id = map.nodes.get(robot.next_node_id).connections.get(next_direction)
        sim_turn(robot)
    else:
        sim_move(robot)

# Finalize the simulator
finalize_simulator()