import turtle as ttl
from turtle import Turtle

from simulator.map import *
from map.map import *
'''python -m simulator.draw'''
def draw_nodes(t:Turtle,start_node, end_node):
    ''' Draws a connection between two nodes on the map.'''

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

if __name__ == '__main__':
    m = Map()

    m.add(
        StartNode(1, n=2),
    TJunction(2, missing='w', n=3, e=4, s=1),
    Corner(3, ('s', 'e'), s=2, e=5),
    DeadEnd(4, w=2),
    Corner(5, ('w', 'n'), w=3, n=7),
    DeadEnd(6, s=7),
    Marker(7, {'s':5, 'n':6})
    )

    m.assert_consistent()

    dm = DrawableMap(m, start_pos=(0,0))

    print(type(dm.nodes[1]))
    print(type(dm))

    screen = ttl.Screen()
    screen.title("Map Simulation")
    screen.setup(width=800, height=600)
    screen.bgcolor("palegreen")
    t = ttl.Turtle()
    screen.tracer(False)
    t.hideturtle()

    for node_id, node in dm.nodes.items():
        for connection_id in node.connections.values():
            connected_node = dm.nodes.get(connection_id)
            if connected_node:
                draw_nodes(t, node, connected_node)

    screen.update()
    ttl.done()