class Node:
    ''' Represents a node in the map with connections to other nodes. '''
    def __init__(self, id, connections: dict):
        ''' Initializes a Node with an ID and its connections.'''

        keys = set(connections.keys())
        valid_keys = {'n', 's', 'e', 'w'}
        if not keys.issubset(valid_keys):
            raise ValueError(f"Invalid connection keys: {keys - valid_keys}. Valid keys are {valid_keys}.")

        self.id = id
        self.connections = connections
        self.type = 'generic'

    def __repr__(self):
        connections = {'n':'','s':'','e':'','w':''}
        for key, value in self.connections.items():
            connections[key] = value

        return \
f'''Node ID: {self.id}
{str(connections['n']) + "\n|" if connections['n'] != '' else ''}
{str(connections['w'])+"–" if connections['w'] != '' else ''}{self.id}{"–"+str(connections['e']) if connections['e'] != '' else ''}
{"|\n" + str(connections['s']) if connections['s'] != '' else ''}
'''

class StartNode(Node):
    ''' Represents the starting node in the map. Assumes a single northerly connection.'''
    def __init__(self, id, n:int):
        connections = {'n': n}
        super().__init__(id, connections)
        self.type = 'start'

class TJunction(Node):
    ''' Represents a T-junction node in the map.'''
    def __init__(self, id,missing: str, *, n=None, s=None, e=None, w=None):
        ''' Initializes a T-junction with one missing connection.'''

        # Requres one direction to be missing
        if missing not in {'n', 's', 'e', 'w'}:
            raise ValueError("missing must be one of 'n','s','e','w'")

        # Require the missing direction to be None
        conns = {'n': n, 's': s, 'e': e, 'w': w}
        if conns[missing] is not None:
            raise ValueError(f"T-junction missing '{missing}' must be None")

        # Require the other three to be provided (not None)
        for d, v in conns.items():
            if d != missing and v is None:
                raise ValueError(f"Missing neighbor id for '{d}'")

        # Create the connections dictionary without the missing direction
        connections = {d: v for d, v in conns.items() if v is not None}

        super().__init__(id, connections)
        self.type = 't_junction'
        self.missing = missing

class PlusJunction(Node):
    ''' Represents a junction node in the map with all four connections.'''
    def __init__(self, id, *, n:int, s:int, e:int, w:int):
        connections = {'n': n, 's': s, 'e': e, 'w': w}
        super().__init__(id, connections)
        self.type = '+_junction'

class Corner(Node):
    ''' Represents a corner node in the map.'''
    def __init__(self,id, connected: tuple, *, n=None, s=None, e=None, w=None):
        ''' Initializes a corner with two connected directions.'''

        # Require connected to be a tuple of two directions
        if len(connected) != 2 or not all(d in {'n', 's', 'e', 'w'} for d in connected):
            raise ValueError("connected must be a tuple of two directions from 'n','s','e','w'")

        # Require the connected directions to be provided (not None)
        conns = {'n': n, 's': s, 'e': e, 'w': w}
        for d in connected:
            if conns[d] is None:
                raise ValueError(f"Missing neighbor id for connected direction '{d}'")

        # Require the other two directions to be None
        for d in conns:
            if d not in connected and conns[d] is not None:
                raise ValueError(f"Corner unconnected direction '{d}' must be None")

        # Create the connections dictionary with only the connected directions
        connections = {d: conns[d] for d in connected}

        super().__init__(id, connections)
        self.type = 'corner'
        self.connected = connected

class Marker(Node):
    """A marker node that lies on a straight line (NS or EW) with no branching."""
    def __init__(self, id, connections: dict):
        ''' Initializes a Marker with two colinear connections.'''
        # Require exactly two co-linear connections
        dirs = set(connections.keys())
        if dirs not in ({'n', 's'}, {'e', 'w'}):
            raise ValueError(
                "MarkerNode must have exactly two colinear connections: "
                "{'n','s'} or {'e','w'}"
            )

        super().__init__(id, connections)
        self.type = 'marker'
        self.direction = dirs

class DeadEnd(Node):
    """Represents a dead-end node in the map (exactly one connection)."""
    def __init__(self, id, *, n=None, s=None, e=None, w=None):
        # Collect provided directions
        conns = {'n': n, 's': s, 'e': e, 'w': w}
        connections = {d: v for d, v in conns.items() if v is not None}

        if len(connections) != 1:
            raise ValueError("DeadEnd must have exactly one connection")

        super().__init__(id, connections)
        self.type = 'dead_end'

class Map:
    ''' Represents a map of nodes with connections. '''
    def __init__(self):
        ''' Initializes an empty Map. '''
        self.nodes = {}

    @staticmethod # Just means its not dependent on self
    def _opposite_dir(d: str) -> str:
        ''' Returns the opposite direction for a given direction. '''
        opp = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        if d not in opp:
            raise ValueError(f"Invalid direction '{d}'")
        return opp[d]

    def add_node(self, node):
        ''' Adds a node to the map after validation. '''

        # Prevent duplicate node ids
        if node.id in self.nodes:
            raise ValueError(f"Node id {node.id} already exists in map")

        # Prevent self connections
        for d, connected_id in node.connections.items():
            if connected_id == node.id:
                raise ValueError(f"Node {node.id} has a self-connection on '{d}'")

        # Add the node
        self.nodes[node.id] = node

        # Return the node for chaining
        return node

    def add(self, *nodes):
        ''' Adds multiple nodes to the map. '''
        for n in nodes:
            self.add_node(n)
        return self

    # --- validation ---
    def consistency_errors(self):
        ''' Returns a list of consistency errors in the map. '''

        # Initialize error list
        errors = []

        # Check each node's connections
        for node in self.nodes.values():
            for d, connection_id in node.connections.items():

                # Check if the connected node exists
                if connection_id not in self.nodes:
                    errors.append(
                        f"Node {node.id} has '{d}' -> {connection_id}, "
                        f"but node {connection_id} is missing"
                    )
                    continue


                # Get the connected node
                connected_node = self.nodes[connection_id]

                # Get the desired opposite direction
                back = self._opposite_dir(d)

                #Get the actual back connection
                actual = connected_node.connections.get(back)

                # Check if the back connection exists
                if actual != node.id:
                    errors.append(
                        f"Inconsistent link: {node.id} '{d}' -> {connection_id}, "
                        f"but {connection_id} '{back}' -> {actual}"
                    )

        # Return the list of errors
        return errors

    def assert_consistent(self):
        ''' Raises an error if the map is inconsistent. '''
        # Get consistency errors
        errors = self.consistency_errors()

        # Raise error if any found
        if errors:
            raise ValueError(
                "Map consistency check failed:\n" +
                "\n".join(f"- {e}" for e in errors)
            )

    def __repr__(self):
        lines = [f"Map({len(self.nodes)} nodes):"]
        for node_id in sorted(self.nodes):
            lines.append(repr(self.nodes[node_id]))
        return "\n".join(lines)



if __name__ == '__main__':
    # Example Usage

    m = Map()

    m.add(
        StartNode(1, n=2),
    TJunction(2, missing='w', n=3, e=4, s=1),
    DeadEnd(3, s=2),
    DeadEnd(4, w=2)
    )

    m.assert_consistent()
    print(m)
