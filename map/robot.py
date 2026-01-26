class Robot:
    def __init__(self, map,start_node_id,direction='n'):
        ''' Initializes the robot at a starting node in the map facing a given direction.'''

        self.last_node_id = start_node_id
        self.direction = direction
        self.next_node_id = map.nodes.get(start_node_id).connections.get(direction)

