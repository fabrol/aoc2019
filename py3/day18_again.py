
# Optimization: Represent input graph as:
#   key|gate -> {key|gate: dist}
#   

# prev seen: abc, curr=c
# graph["c"], see if "A" and "B" and "C" are in that dict, then expand
# graph["A"]
# graph["B"]
# graph["C"]
# create a set of 


# Find @
# Find available keys to move to and distance to each
# 
# Memoize (key, allkeys) -> path length
#    (key describes your position)

def read_input(filename='day18.in'):
    with open(filename, 'r') as f:
        contents = f.read().strip()
        return contents

N = 3

_DELTAS = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]

_KEY_NAMES = set(list("abcdefghijklmnopqrstuvwxyz"))

def print_graph(graph, seen_keys):
    for row in graph:
        output = []
        for val in row:
            if val in seen_keys or val.lower() in seen_keys:
                output.append('-')
            else:
                output.append(val)
        print(''.join(output))
            

def find_keys(position, seen_keys, graph):
    dist_by_keys = {}  # {available_key_to_visit: (pos, dist)}
    # if you hit a key or a locked door
    queue = [position + (0,)]
    max_row = len(graph) - 1
    max_col = len(graph[0]) - 1
    visited = set()
    while queue:
        curr = queue.pop(0)
        row, col, dist = curr
        visited.add((row, col))
        for r, c in _DELTAS:
            nr = row + r
            nc = col + c
            if 0 <= nr <= max_row and 0 <= nc <= max_col and (nr, nc) not in visited:
                next_val = graph[row+r][col+c]
                # is it a key?
                # is it a gate?
                # is it a '.'
                if ord('a') <= ord(next_val) <= ord('z'):
                    if next_val not in seen_keys:
                        dist_by_keys[next_val] = ((nr, nc), dist + 1)
                    else:
                        queue.append((nr, nc, dist + 1))
                elif ord('A') <= ord(next_val) <= ord('Z'):
                    if next_val.lower() in seen_keys:
                        queue.append((nr, nc, dist + 1))
                elif next_val in ('.', '@'):
                    queue.append((nr, nc, dist + 1))
                elif next_val == '#':
                    pass
                else:
                    raise ValueError(f'halp idk what {next_val} at {nr},{nc} is')

    return dist_by_keys


# cache: (position, hashable_seen_keys): shortest_to_end

def seen_keys_to_hash(seen_keys):
    return ''.join(sorted(seen_keys))

def min_total_path_length(position, seen_keys, graph, cache):
    val = cache.get((position, seen_keys_to_hash(seen_keys)), None)
    if val:
        print(f'Hit cache {val} Seen keys {len(seen_keys)} {position}')
        return val

    dist_by_keys = find_keys(position, seen_keys, graph)
    if not dist_by_keys:
        cache[(position, seen_keys_to_hash(seen_keys))] = 0
        return 0
    #print_graph(graph, seen_keys)
    #print(f'Seen keys {seen_keys}')
    min_path_len = float('inf')
    #print(f'Seen keys {len(seen_keys)} {len(dist_by_keys)} {position}')
    for key, (pos, dist) in dist_by_keys.items():
        #print(f'From {position}->{pos}, Exploring {key} ({dist})')
        remain_dist = min_total_path_length(
                        position=pos,
                        seen_keys=(seen_keys + [key]),
                        graph=graph,
                        cache = cache)
        #print(f'{min_path_len} {curr_path_len} {dist} {remain_dist}')
        min_path_len = min(min_path_len, remain_dist + dist)
    cache[(position, seen_keys_to_hash(seen_keys))] = min_path_len
    return min_path_len 

def run_parta(graph_str):
    graph = []
    for line in graph_str.split('\n'):
        graph.append(list(line))

    start_pos = (-1, -1)  # (row, col)
    for i in range(len(graph)):
        try:
            start_index = graph[i].index('@')
            start_pos = (i, start_index)
            break
        except ValueError:
            pass

    print(f'Starting position {start_pos}')
        
    cache = {}
    print(min_total_path_length(start_pos, [], graph, cache))


run_parta(read_input('day18_test1.in'))

#
# 
# def MinTotalPathLength(position, graph):
# Find available keys k to move to p and distance d to each
# selection = Min(MinTotalPathLength( p, graph w/ p unlocked) + d)
#   
#


# 
# From (27, 29)->(23, 23), Exploring v (14)
#Seen keys 23 1 (23, 23)
#From (23, 23)->(77, 51), Exploring o (806)
#Seen keys 24 1 (77, 51)
#From (77, 51)->(75, 53), Exploring b (16)
#Seen keys 25 1 (75, 53)
#From (75, 53)->(69, 61), Exploring k (14)
#From (29, 63)->(27, 11), Exploring f (666)
#
