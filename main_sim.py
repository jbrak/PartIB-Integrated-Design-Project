from simulator.draw import *
from map.robot import *
from map.map import Map
import turtle as ttl

# Create a map instance
map = Map()

# # Define a sequence of movements for the robot
# s = ['n','n', 'e', 'n', 'n']
#
# # Add nodes to the map
# map.add(
#     StartNode(1, n=2),
#     TJunction(2, missing='w', n=3, e=4, s=1),
#     Corner(3, ('s', 'e'), s=2, e=5),
#     DeadEnd(4, w=2),
#     Corner(5, ('w', 'n'), w=3, n=7),
#     DeadEnd(6, s=7),
#     Marker(7, {'s': 5, 'n': 6})
# )

s = ['n']

map.add(
    StartNode(1, n=2), # Start Node
    TJunction(2, missing = 'n', s=1, w=3,e=7),
    TJunction(3,missing='n', s=4,e=2,w=5),
    DeadEnd(4,n=3), # Loading Bay 2
    TJunction(5,missing='w', e=3,s=6,n=11),
    DeadEnd(6,n=5), # Loading Bay 1
    TJunction(7, missing = 'n', w=2,s=8,e=9),
    DeadEnd(8,n=7), # Loading Bay 3
    TJunction(9,missing='e', w=7,s=10,n=30),
    DeadEnd(10,n=9), # Loading Bay 4
    TJunction(11,missing='w', n=12, s=5,e=17),
    TJunction(12,missing='w', s=11, n=13,e=18),
    TJunction(13,missing='w', n=14, s=12,e=19),
    TJunction(14,missing='w', n=15, s=13,e=20),
    TJunction(15,missing='w', n=16, s=14,e=21),
    TJunction(16,missing='w', n=49, s=15,e=22),
    DeadEnd(17, w=11), # Lower Rack A, Bay 6
    DeadEnd(18, w=12), # Lower Rack A, Bay 5
    DeadEnd(19, w=13), # Lower Rack A, Bay 4
    DeadEnd(20, w=14), # Lower Rack A, Bay 3
    DeadEnd(21, w=15), # Lower Rack A, Bay 2
    DeadEnd(22, w=16), # Lower Rack A, Bay 1

    TJunction(30, missing='e', n=31, s=9, w=36),
    TJunction(31, missing='e', n=32, s=30, w=37),
    TJunction(32, missing='e', n=33, s=31, w=38),
    TJunction(33, missing='e', n=34, s=32, w=39),
    TJunction(34, missing='e', n=35, s=33, w=40),
    TJunction(35, missing='e', n=50, s=34, w=41),
    DeadEnd(36, e=30),  # Lower Rack B, Bay 6
    DeadEnd(37, e=31),  # Lower Rack B, Bay 5
    DeadEnd(38, e=32),  # Lower Rack B, Bay 4
    DeadEnd(39, e=33),  # Lower Rack B, Bay 3
    DeadEnd(40, e=34),  # Lower Rack B, Bay 2
    DeadEnd(41, e=35),  # Lower Rack B, Bay 1

    DeadEnd(49, s=16),
    DeadEnd(50, s=35),
)

# Ensure the map is consistent
map.assert_consistent()

robot = Robot(map, start_node_id=1, direction=s.pop(0))

# Initialize the simulator
map, robot = initialize_simulator(map, robot, LENGTH=60, start_pos=(0,-200))

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