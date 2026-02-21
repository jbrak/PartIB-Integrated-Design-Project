from map.robot import Robot
from simulator.map import DrawableMap
import turtle as ttl

class DrawableRobot(Robot):
    """
    A drawable robot that extends the basic Robot class.

    Attributes
    ----------
    last_node_id : int
        Holds the ID of the previous node 
    direction : str
        Holds the direction that the robot is going to
    next_node_id : int
        Holds the ID of the next node the robot needs to go to
    position : tuple
        Holds an (x,y) position of the robot
    next_node_position
        Holds the (x,y) position of the next node the robot needs to go to
    """
    
    def __init__(self, map:DrawableMap,start_node_id, direction='n'):
        """
        Initializes the drawable robot at a starting node in the map facing a given direction.
        
        map : DrawableMap
            The drawn map that the drawn robot will be traversing
        start_node_id : int
            The ID of the starting node
        direction : str
            The direction that the robot starts facing 
        """

        super().__init__(map,start_node_id, direction)
        self.position = map.nodes[start_node_id].position
        self.next_node_position = map.nodes[self.next_node_id].position

class DrawableRobot2(Robot):
    """
    A drawable robot that extends the basic Robot class.

    Attributes
    ----------
    last_node_id : int
        Holds the ID of the previous node    
    direction : str
        Holds the direction that the robot is going to
    next_node_id : int
        Holds the ID of the next node
    t : Turtle
        Holds the turtle used to draw the map and robot
    """

    def __init__(self, map:DrawableMap,robot,t:ttl.Turtle):
        """
        Initializes the drawable robot at a starting node in the map facing a given direction.
        
        map : DrawableMap
            The drawn map that the drawn robot will be traversing
        robot : Robot
            The AGV's class 
        t : Turtle
            The turtle used to draw the map and robot 
        """

        super().__init__(map,robot.last_node_id, robot.direction)
        self.t = t