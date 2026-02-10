from map.map import *
from map.route import *

class KeyNodes:
    def __init__(self, map):
        self.empty_bays = {"r1": [], "r2": [], "r3": [], "r4": []}
        self.coils = [6, 4, 8, 10]
        self.coil_reading = 0

        self.bays = {"r1": [22,21,20,19,18,17], "r2": [28,27,26,25,24,23], "r3": [36,37,38,39,40,41], "r4": [42,43,44,45,46,47]}
        self.bays_searched = {"r1": [], "r2": [], "r3": [], "r4": []}
        self.bay_reading = {"r1": [0]*6, "r2": [0]*6, "r3": [0]*6, "r4": [0]*6}


def next_node(map, status, pause_count, current_node_id, key_nodes):

    sequence = []

    if status == 101: #Initialising - locating empty bays
        
        #Scanning the bay
        if len(key_nodes.bays_searched["r1"])>0:
            pause_count = check_bay(["r1","r2"],key_nodes.bays_searched["r1"][-1],key_nodes.bays_searched["r2"][-1],pause_count,key_nodes)

        elif len(key_nodes.bays_searched["r3"])>0:
            pause_count = check_bay(["r3","r4"],key_nodes.bays_searched["r3"][-1],key_nodes.bays_searched["r4"][-1],pause_count,key_nodes)

        #Selects the next bay to go to
        if pause_count <=1:
            if len(key_nodes.bays_searched["r3"]) <6:

                i =len(key_nodes.bays_searched["r3"])
                next_node_id = key_nodes.bays["r3"][i]
                key_nodes.bays_searched["r3"].append(next_node_id)
                key_nodes.bays_searched["r4"].append(key_nodes.bays["r4"][i])

                sequence = route(map, current_node_id, next_node_id)[1][:-1]

            elif len(key_nodes.bays_searched["r1"]) <6:

                i =len(key_nodes.bays_searched["r1"])
                next_node_id = key_nodes.bays["r1"][i]
                key_nodes.bays_searched["r1"].append(next_node_id)
                key_nodes.bays_searched["r2"].append(key_nodes.bays["r2"][i])

                sequence = route(map, current_node_id, next_node_id)[1][:-1]

            else:
                status = 102

            


    elif status == 102: #Pick up coil
        
        if len(key_nodes.coils) !=0:

            #Some way to choose closest coil?
            sequence = route(map, current_node_id, key_nodes.coils[0])[1]
            for coil in key_nodes.coils:
                temp_seq = route(map, current_node_id, coil)[1]
                if len(temp_seq) < len(sequence):
                    sequence = temp_seq

            if len(sequence) == 0:
                #Reached coil, activate picking up mech
                pause_count = pick_up_coil(pause_count)
                if pause_count <=1:
                    #Pick-up complete
                    key_nodes.coils.remove(current_node_id)
                    status = 103

        else:
            status = 105




    elif status == 103: #Measure Coil, and deliver
        #Alogorithm to measure resistance and drop off coil
        pause_count,res = measure_coil()
        if res != None:
            next_node_id = key_nodes.empty_bays[res].sorted()[0] 
            sequence = route(map, current_node_id, next_node_id)[1]
            status = 104


    elif status == 104: #Drop Off Coil

        pause_count = drop_off_coil(pause_count)

        if pause_count <=1:
            #Drop off complete - updating empty bay list

            for key, values in key_nodes.empty_bays.items():
                if current_node_id in values:
                    key_nodes.empty_bays[key].remove(current_node_id)

                    
            status = 102

    elif status == 105: #Go Home
        sequence = route(map, current_node_id, 2)[1]

        #Note: externally if len(sequence) ==0:, and status = 105, activate parking algorithm


    return sequence,status

def check_bay(sector,bottom_bay,top_bay,pause_count,key_nodes):
    #Algorithm with sensors to check bays here
    if pause_count == 0:
        pause_count = 100

    if pause_count > 1:
        #Check with sensors top_reading, bottom_reading
        bottom_reading = 150
        top_reading= 50
        

        key_nodes.bay_reading[sector[0]][key_nodes.bays[sector[0]].index(bottom_bay)] += bottom_reading
        key_nodes.bay_reading[sector[1]][key_nodes.bays[sector[1]].index(top_bay)] += top_reading

    else: #pause_count == 1
        #multi-addtional checker - different threshold values for the two sensors
        threshold = [10000,10000]
        if key_nodes.bay_reading[sector[0]][key_nodes.bays[sector[0]].index(bottom_bay)] >= threshold[0]:
            key_nodes.empty_bays[sector[0]].append(bottom_bay)

        if key_nodes.bay_reading[sector[1]][key_nodes.bays[sector[1]].index(top_bay)] >= threshold[1]:
            key_nodes.empty_bays[sector[1]].append(top_bay)

    return pause_count



def pick_up_coil(pause_count):
    #Algorithm to operate servos and pick up coil
    if pause_count == 0:
        pause_count = 100

    return pause_count

def drop_off_coil(pause_count):
    #Algorithm to operate servos and drop off coil
    if pause_count == 0:
        pause_count = 100

    return pause_count



def measure_coil(key_nodes):
    #Measures and determines the resistoance of coils
    res = None
    if pause_count == 0:
        pause_count = 100

    if pause_count > 1:
        #Check with resistor circuit reading
        res_reading = 100

        key_nodes.coil_reading += res_reading

    else: #pause_count == 1
        #decide on which resistor is correct
        threshold = [1000,2000,3000,10000]

        for i in range(len(threshold)):
            if key_nodes.coil_reading<=threshold[i] and res == None:
                res = list(key_nodes.bays.keys())[i]

    return pause_count,res