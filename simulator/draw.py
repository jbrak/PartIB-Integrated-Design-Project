import turtle as ttl
from turtle import Turtle
from time import sleep
from simulator.map import *
from map.map import Map
from simulator.robot import *

'''python -m simulator.draw'''
def draw_nodes(t:Turtle,start_node, end_node):
    """
    Draws a connection between two nodes on the map
    
    Parameters
    ----------
    t : Turtle
        The turtle that will draw the map connections
    start_node : int
        Node ID of te 
    """

    # Get the positions of the start and end nodes
    start_pos = start_node.position
    end_pos = end_node.position


    # Move to the start position
    t.penup()
    t.goto(start_pos)
    t.dot(start_node.DOTSIZE,start_node.COLOR)
    t.pendown()

    # Draw a line to the end position
    t.goto(end_pos)
    t.penup()

def draw_map(t:Turtle, dm:DrawableMap):
    ''' Draws the entire drawable map using the provided turtle.'''
    # Hide the turtle while drawing
    t.hideturtle()

    # Draw all connections between nodes
    for node_id, node in dm.nodes.items():
        for connection_id in node.connections.values():
            connected_node = dm.nodes.get(connection_id)
            if connected_node:
                draw_nodes(t, node, connected_node)
    # Show the turtle after drawing
    t.showturtle()


def move_robot(t:Turtle, drawable_robot:DrawableRobot, dm:DrawableMap, next_direction=None):
    ''' Moves the drawable robot to a new position.'''

    # Define heading map and offsets
    heading_map = {"n":90, "e":0, "s":270, "w":180}
    offsets = {
        'n': (0, 1),
        's': (0, -1),
        'e': (1, 0),
        'w': (-1, 0)
    }

    # Get the step offset based on the current direction
    step = offsets[drawable_robot.direction]

    # Set the turtle heading
    t.setheading(heading_map[drawable_robot.direction])

    # Move the turtle step by step to the next node position
    while drawable_robot.position != drawable_robot.next_node_position:
        t.forward(1)
        drawable_robot.position = (drawable_robot.position[0] + step[0], drawable_robot.position[1] + step[1])
        sleep(0.01)

    # Update the robot's state if a next direction is provided
    if next_direction is not None:
        drawable_robot.last_node_id = drawable_robot.next_node_id
        drawable_robot.direction = next_direction
        drawable_robot.next_node_id = dm.nodes[drawable_robot.last_node_id].connections.get(next_direction)
        drawable_robot.next_node_position = dm.nodes[drawable_robot.next_node_id].position

def sim_move(robot:DrawableRobot2):
    ''' Simulates a simple forward movement of the turtle.'''
    robot.t.forward(1)

def sim_check_node(r:DrawableRobot2, dm: DrawableMap,):
    '''Checks if the Next Node Has been Reached'''
    pos = (int(r.t.xcor()), int(r.t.ycor()))

    if pos == dm.nodes[r.next_node_id].position:
        return True
    return False

def sim_turn(r:DrawableRobot2):
    heading_map = {"n": 90, "e": 0, "s": 270, "w": 180}

    r.t.setheading(heading_map[r.direction])

def initialize_simulator(m:Map, robot:Robot, LENGTH=60, start_pos=(0,-100)):
    '''Initializes the simulator environment.'''
    # Create a drawable map with starting position
    dm = DrawableMap(m, start_pos=start_pos, LENGTH=LENGTH)

    # Set up the turtle graphics screen
    screen = ttl.Screen()
    screen.title("Map Simulation")
    screen.setup(width=800, height=600)
    screen.bgcolor("palegreen")
    t = ttl.Turtle()
    screen.tracer(False)

    #  Draw the map
    draw_map(t, dm)

    # Update the screen
    screen.update()

    # Move the turtle to the robot's starting position
    t.goto(dm.nodes[dm.start_id].position)

    # Animate the robot movement
    screen.tracer(True)

    # Create a drawable robot
    robot = DrawableRobot2(dm, robot, t)
    sim_turn(robot)

    return dm, robot

def finalize_simulator():
    '''Finalizes the simulator environment.'''
    ttl.done()

if __name__ == '__main__':
    # Create a map instance
    m = Map()

    # Define a sequence of movements for the robot
    s = ['n','e','n','n']

    # Add nodes to the map
    m.add(
        StartNode(1, n=2),
    TJunction(2, missing='w', n=3, e=4, s=1),
    Corner(3, ('s', 'e'), s=2, e=5),
    DeadEnd(4, w=2),
    Corner(5, ('w', 'n'), w=3, n=7),
    DeadEnd(6, s=7),
    Marker(7, {'s':5, 'n':6})
    )

    # Ensure the map is consistent
    m.assert_consistent()

    # Create a drawable map with starting position
    dm = DrawableMap(m, start_pos=(0,-100))

    # Set up the turtle graphics screen
    screen = ttl.Screen()
    screen.title("Map Simulation")
    screen.setup(width=800, height=600)
    screen.bgcolor("palegreen")
    t = ttl.Turtle()
    screen.tracer(False)

    #  Draw the map
    draw_map(t, dm)

    # Update the screen
    screen.update()

    # Animate the robot movement
    screen.tracer(True)

    # Create a drawable robot
    drawable_robot = DrawableRobot(dm, start_node_id=1, direction='n')

    # Move the turtle to the robot's starting position
    t.goto(drawable_robot.position)

    # Move the robot according to the defined sequence
    for i in s:
        move_robot(t, drawable_robot, dm, next_direction=i)

    # Final move to complete the last segment
    move_robot(t, drawable_robot, dm)

    # Finish the turtle graphics
    ttl.done()