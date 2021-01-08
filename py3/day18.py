
class Node(object):
    def __init__(self, key_name, location, last_location, keys, curr_path_length):
        self.keys = keys 
        self.location = location
        self.curr_path_length = curr_path_length
        self.last_location = last_location
        self.key_name = key_name

    def __str__(self):
        return (f'Key {self.key_name} at {self.location}'
                f'{self.curr_path_length} ({self.keys}, {self.last_location})')
    


def find_new_nodes(vault_map, location, keys, initial_path_len):
    # Identify all reachable keys from the current position
    q = [(location[0], location[1], initial_path_len)]
    #print (f'Starting to find from: {location}, {keys}')
    reachable_keys = []  # list of (row, col, path_len, key_name)
    col_max = len(vault_map[0]) - 2
    row_max = len(vault_map) - 2
    visited = set()
    while q:
        row, col, path_len = q.pop(0)
        if (row, col) in visited:
            continue
        visited.add((row, col))
        val = vault_map[row][col]
        # If the gate is not unlocked, continue.
        if ord('A') <= ord(val) <= ord('Z') and val.lower() not in keys:
            continue
        # If it's a key, yay! Stop exploring this direction.
        if ord('a') <= ord(val) <= ord('z') and (row, col) != location:
            reachable_keys.append((row, col, path_len, vault_map[row][col]))
            continue

        if row > 0 and vault_map[row-1][col] != '#':
            q.append((row-1, col, path_len+1))
        if col > 0 and vault_map[row][col-1] != '#':
            q.append((row, col-1, path_len+1))
        if col < col_max and vault_map[row][col+1] != '#':
            q.append((row, col+1, path_len+1))
        if row < row_max and vault_map[row+1][col] != '#':
            q.append((row+1, col, path_len+1))

    nodes = []
    for row, col, path_len, key_name in reachable_keys:
        n = Node(key_name=key_name,
                 location=(row, col),
                 last_location=location,
                 keys=keys.union(set([key_name])),
                 curr_path_length=path_len)
        nodes.append(n)
    return nodes

# Find start location

# BFS with tracking of cumulative path length

def run_part_a():
    graph = read_input()
    vault_map = []
    for line in graph.split('\n'):
        vault_map.append(list(line))
        
    # TODO: find @ in array
    print(vault_map[40][40])
    keys = set()
    location = (40, 40)
    start_node = Node(key_name='@', location=location, last_location=None,
                      keys=keys, curr_path_length=0)

    visited_map = {} # map from (keys, location) -> shortest_known_path_len

    def to_dict_key(keys, l):
        return (''.join(sorted(keys)), l)

    q = [start_node]
    known_endpoints = []

    while q:
        cur_node = q.pop(0)
        #print(f'cur_node: {cur_node}')
        print(f'Current Q: {len(q)}')
        #for n in q:
        #    print(f'\t  {n}')

        visited_key = to_dict_key(cur_node.keys, cur_node.location)

        # Stop exploring when there are shorter ways to get to this path.
        if (visited_key in visited_map and
                visited_map[visited_key] <= cur_node.curr_path_length):
            #print(f'  Stopping: {cur_node}')
            continue

        #print(f'  Searching: {cur_node} \t {visited_key} \t {visited_map.keys()}')
        shortest_known_val = visited_map.get(visited_key, cur_node.curr_path_length)
        if cur_node.curr_path_length <= shortest_known_val:
            visited_map[visited_key] = cur_node.curr_path_length

        # Stop exploring when we've reached our end condition.
        if len(cur_node.keys) == 26:
            known_endpoints.append(cur_node)
            continue

        new_nodes = find_new_nodes(vault_map=vault_map,
                                   location=cur_node.location,
                                   keys=cur_node.keys,
                                   initial_path_len=cur_node.curr_path_length)
        for n in new_nodes:
            q.append(n)

    print (known_endpoints)

def read_input(filename='day18.in'):
    with open(filename, 'r') as f:
        contents = f.read().strip()
        return contents

run_part_a()
