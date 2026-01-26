from simulator.draw import *
from map.robot import *
from map.map import Map
import turtle as ttl

# Create a map instance
map = Map()

# Define a sequence of movements for the robot
s = ['n','n', 'e', 'n', 'n']

# Add nodes to the map
map.add(
    StartNode(1, n=2),
    TJunction(2, missing='w', n=3, e=4, s=1),
    Corner(3, ('s', 'e'), s=2, e=5),
    DeadEnd(4, w=2),
    Corner(5, ('w', 'n'), w=3, n=7),
    DeadEnd(6, s=7),
    Marker(7, {'s': 5, 'n': 6})
)

# Ensure the map is consistent
map.assert_consistent()

robot = Robot(map, start_node_id=1, direction=s.pop(0))

# Initialize the simulator
map, robot = initialize_simulator(map, robot)

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