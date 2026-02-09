from map.map import *
from map.route import *

class KeyNodes:
    def __init__(self, map):
        self.empty_bays = {"r1": [], "r2": [], "r3": [], "r4": []}
        self.coils = [6, 4, 8, 10]

        self.bays = {"r1": [22,21,20,19,18,17], "r2": [28,27,26,25,24,23], "r3": [36,37,38,39,40,41], "r4": [42,43,44,45,46,47]}
        self.bays_searched = {"r1": [], "r2": [], "r3": [], "r4": []}


def next_node(map, status, pause_count, current_node_id, key_nodes):



    if status == 101:
        if len(key_nodes.bays_searched["r3"]) <6:
            i =len(key_nodes.bays_searched["r3"])
            next_node_id = key_nodes.bays["r3"][i]


    sequence = route(map, current_node_id, next_node_id)[1]
    return sequence