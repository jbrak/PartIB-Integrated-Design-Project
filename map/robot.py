class Robot:
    """
    Holds the methods for updating the AGV's internal map
    
    Attributes
    ----------
    last_node_id : int
        Holds the ID of the previous node 
    direction : str
        Holds the direction that the robot is going to
    next_node_id : int
        Holds the ID of the next node

    Methods
    -------
    update_direction(next_direction : str) -> str
    """
    
    def __init__(self, map,start_node_id,direction='n'):
        '''
        Initializes the robot at a starting node in the map facing a given direction.
        
        Parameters
        ----------
        map : Map
            The map that the robot is traversing
        start_node_id : int
            The ID of the start node
        direction : str
            The direction that the robot is facing at first
        '''

        self.last_node_id = start_node_id
        self.direction = direction
        self.next_node_id = map.nodes.get(start_node_id).connections.get(direction)

    def update_direction(self, next_direction):
        '''
        Returns the way that the robot needs to move to get to the next node.
        
        Parameters
        ----------
        next_direction : str
            The next direction the robot needs to go to
        
        '''

        direction_map = {'n' : {'n': 'f', 'e': 's', 's': 'b', 'w': 'p'},
                         'e' : {'n': 'p', 'e': 'f', 's': 's', 'w': 'b'},
                         's' : {'n': 'b', 'e': 'p', 's': 'f', 'w': 's'},
                         'w' : {'n': 's', 'e': 'b', 's': 'p', 'w': 'f'}}

        turn = direction_map[self.direction][next_direction]

        if turn != 'b':
            self.direction = next_direction

        return turn

