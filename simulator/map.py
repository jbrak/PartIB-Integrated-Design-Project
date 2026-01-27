from map.map import *

class DrawableNode():
    def __init__(self, node: Node, DOTSIZE=10):
        ''' Initializes a DrawableNode from a given Node and position.'''
        colors = {
            'start': 'green',
            'dead_end': 'red',
            'corner': 'blue',
            't_junction': 'orange',
            '+_junction': 'purple',
            'marker' : 'yellow',
            'generic': 'gray'
        }
        self.id = node.id
        self.type = node.type
        self.connections = node.connections
        self.position = None
        self.DOTSIZE = DOTSIZE
        self.COLOR = colors.get(self.type, 'gray')




class DrawableMap():
    def __init__(self, map: Map, start_pos=(0,0), DOTSIZE=10, LENGTH=50):
        ''' Initializes a DrawableMap from a given Map.'''
        self.nodes = {}
        self.to_define = []

        for id, node in map.nodes.items():
            node = DrawableNode(node, DOTSIZE)
            self.nodes[id] = node
            if node.type == 'start':
                start = node

        start.position = start_pos
        self.nodes[start.id] = start
        self.start_id = start.id

        self.generate_positions(start.id, LENGTH=LENGTH)




    @staticmethod
    def direction_to_offset(direction):
        ''' Converts a direction to an (x, y) offset.'''
        offsets = {
            'n': (0, 1),
            's': (0, -1),
            'e': (1, 0),
            'w': (-1, 0)
        }
        if direction not in offsets:
            raise ValueError(f"Invalid direction '{direction}'")
        return offsets[direction]

    def generate_positions(self, node_id, LENGTH=50):
        ''' Generates positions for nodes based on their connections.'''
        node = self.nodes.get(node_id)
        if not node.position:
            raise ValueError(f"Node {node.id} has no position defined.")

        for direction, connected_id in node.connections.items():
            connected_node = self.nodes.get(connected_id)
            if not connected_node.position:

                if connected_node.type == 'dead_end':
                    L = LENGTH/3
                else:
                    L = LENGTH

                offset = self.direction_to_offset(direction)
                connected_node.position = (
                    node.position[0] + L*offset[0],
                    node.position[1] + L*offset[1]
                )
                self.nodes[connected_id] = connected_node
                self.to_define.append(connected_id)

        if len(self.to_define)>0:
            self.generate_positions(self.to_define.pop(0), LENGTH=LENGTH)

    def get_positions(self):
        ''' Returns a dictionary of node ids to their positions.'''
        positions = {}
        for id, node in self.nodes.items():
            positions[id] = node.position
        return positions


if __name__ == '__main__':
    m = Map()
    m = Map()

    m.add(
        StartNode(1, n=2),
    TJunction(2, missing='w', n=3, e=4, s=1),
    DeadEnd(3, s=2),
    DeadEnd(4, w=2)
    )

    m.assert_consistent()

    dm = DrawableMap(m, start_pos=(0,0))
    print(dm.get_positions())
