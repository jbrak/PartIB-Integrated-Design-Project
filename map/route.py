from collections import deque

def route(map, start_id: int, goal_id: int):
    """
    Finds the shortest path between two nodes in a map using breadth-first search.
    """
    # handle trivial case
    if start_id == goal_id:
        return [start_id], []

    # queue holds nodes to explore, use a queue so that we can have O(1) pops from left
    q = [start_id]

    # parent[node] = previous node on shortest path
    parent = {start_id: None}

    # parent_dir[node] = direction used to ENTER 'node' from parent[node]
    parent_dir = {}

    while q:
        # get current node to explore
        current_id = q.pop(0)

        # get current node
        current_node = map.nodes[current_id]

        # assuming: current_node.connections is dict: direction -> neighbor_id
        for direction, next_id in current_node.connections.items():
            # skip if no connection in this direction
            if next_id is None:
                continue
            # skip if already seen
            if next_id in parent:
                continue

            # record parent and direction
            parent[next_id] = current_id
            parent_dir[next_id] = direction

            # check if goal reached
            if next_id == goal_id:
                # reconstruct path
                node_path = []
                dir_path = []
                node = goal_id

                # backtrack from goal to start
                while node is not None:
                    # append node
                    node_path.append(node)

                    # skip direction for start node
                    if node != start_id:
                        # append direction used to enter this node
                        dir_path.append(parent_dir[node])
                    # move to parent
                    node = parent[node]

                # reverse paths to get start to goal order
                node_path.reverse()
                dir_path.reverse()

                # return the paths
                return node_path, dir_path

            # add to queue for further exploration
            q.append(next_id)

    # if we exhaust the search without finding the goal
    return None, None
