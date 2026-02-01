class Robot:
    def __init__(self, map,start_node_id,direction='n'):
        ''' Initializes the robot at a starting node in the map facing a given direction.'''

        self.last_node_id = start_node_id
        self.direction = direction
        self.next_node_id = map.nodes.get(start_node_id).connections.get(direction)

    def update_direction(self, next_direction):

        direction_map = {'n' : {'n': 'f', 'e': 's', 's': 'b', 'w': 'p'},
                         'e' : {'n': 'p', 'e': 'f', 's': 's', 'w': 'b'},
                         's' : {'n': 'b', 'e': 'p', 's': 'f', 'w': 's'},
                         'w' : {'n': 's', 'e': 'b', 's': 'p', 'w': 'f'}}

        turn = direction_map[self.direction][next_direction]

        self.direction = next_direction
        return turn

