from map.robot import Robot
from simulator.map import DrawableMap
import turtle as ttl

class DrawableRobot(Robot):
    ''' A drawable robot that extends the basic Robot class.'''
    def __init__(self, map:DrawableMap,start_node_id, direction='n'):
        ''' Initializes the drawable robot at a starting node in the map facing a given direction.'''
        super().__init__(map,start_node_id, direction)
        self.position = map.nodes[start_node_id].position
        self.next_node_position = map.nodes[self.next_node_id].position

class DrawableRobot2(Robot):
    ''' A drawable robot that extends the basic Robot class.'''
    def __init__(self, map:DrawableMap,robot,t:ttl.Turtle):
        ''' Initializes the drawable robot at a starting node in the map facing a given direction.'''
        super().__init__(map,robot.last_node_id, robot.direction)
        self.t = t