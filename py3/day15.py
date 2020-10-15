from computer import Computer
import itertools
from typing import List
import enum


DEBUG = False

"""
Movement commands:
north (1), south (2), west (3), and east (4).

Status codes:
0: The repair droid hit a wall. Its position has not changed.
1: The repair droid has moved one step in the requested direction.
2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
"""


class Direction(enum.Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


# class Status(enum.Enum):
STATUS = {
    "WALL": 0,
    "MOVED": 1,
    "OXYGEN": 2
}


_INVERT_DIRECTION = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
    Direction.EAST: Direction.WEST,
}

_WORLD_MAPPING = {
    'WALL': '#',
    'VISITED': '.',
    'OXYGEN': 'O',
    'UNEXPLORED': ' '
}

GRAPH = {(0, 0): '.'}
OXYGEN_POSITION = None

def print_graph(graph):
    x_pos = [p[0] for p in graph.keys()]
    y_pos = [p[1] for p in graph.keys()]
    max_x = max(x_pos)
    max_y = max(y_pos)
    min_x = min(x_pos)
    min_y = min(y_pos)
    for y in range(max_y, min_y - 1, -1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) in graph:
                row.append(graph[(x, y)])
            else:
                row.append(' ')
        print(''.join(row))


def calc_pos(position, direction):
    if direction == Direction.NORTH:
        return (position[0], position[1]+1)
    elif direction == Direction.SOUTH:
        return (position[0], position[1]-1)
    elif direction == Direction.EAST:
        return (position[0]+1, position[1])
    elif direction == Direction.WEST:
        return (position[0]-1, position[1])
    else:
        print("WTF MATE")


def make_graph(c):
    position = (0, 0)
    reached_oxygen = False
    explore_queue = [position]
    # position tuple -> (position, direction)
    came_from = {position: (position, Direction.NORTH)}
    walls = {}

    while len(explore_queue) > 0:
        to_explore = explore_queue.pop()

        assert to_explore in came_from, f"Visiting {to_explore} and its not in came_from"

        if to_explore != position:
            to_explore_parent, to_explore_dir = came_from[to_explore]
            # Are we where we want to go
            while to_explore_parent != position:
                # -> If not -> backtrack till we get there
                assert position in came_from, f"Trying to backtrack to {to_explore} at {position} which is not in came from"
                pos, dirc = came_from[position]

                # Move the inverse direction
                inv_output = c.run_program(_INVERT_DIRECTION[dirc].value)
                assert (inv_output.output[0] == STATUS['MOVED'])
                position = calc_pos(position, _INVERT_DIRECTION[dirc])

            # Move one step to get to to_explore
            move_to_explore = c.run_program(to_explore_dir.value)
            assert (move_to_explore.output[0] == STATUS["MOVED"])
            position = calc_pos(position, to_explore_dir)
        assert position == to_explore, f"Should be at {to_explore} but at {position}"
        # We sense the neighbors to see what is possible
        #       Making sure to backtrack
        # Then we enqueue the neighbors to explore

        for direction in Direction:
            next_input = direction
            tmp_position = calc_pos(position, direction)

            # if visited this node before, or it is a wall, skip.
            if (tmp_position in came_from) or (tmp_position in walls):
                continue

            p_output = c.run_program(next_input.value)
            output = p_output.output[0]
            output_op = p_output.opcode
            if output == STATUS['OXYGEN']:
                reached_oxygen = True
                GRAPH[tmp_position] = _WORLD_MAPPING['OXYGEN']
                global OXYGEN_POSITION
                OXYGEN_POSITION = tmp_position

                # Update the came_from dict
                came_from[tmp_position] = (position, direction)

                # Move the inverse direction
                inv_output = c.run_program(_INVERT_DIRECTION[direction].value)
                assert (inv_output.output[0] == STATUS['MOVED'])
                #break
            elif output == STATUS['WALL']:
                GRAPH[tmp_position] = _WORLD_MAPPING['WALL']
                # Update the came_from dict
                walls[tmp_position] = position
                continue
            elif output == STATUS['MOVED']:
                # Add this node to the explore queue
                explore_queue.append(tmp_position)
                GRAPH[tmp_position] = _WORLD_MAPPING['UNEXPLORED']

                # Update the came_from dict
                came_from[tmp_position] = (position, direction)

                # Move the inverse direction
                inv_output = c.run_program(_INVERT_DIRECTION[direction].value)
                assert (inv_output.output[0] == STATUS['MOVED'])
            else:
                assert True == False, f'Im sad: {output}'

        if reached_oxygen:
            #break
            pass


def find_shortest_path():
    position = (0, 0)
    came_from = {}  # position -> position
    explore_queue = [position]
    found_pos = None

    while (len(explore_queue) > 0):
        to_explore = explore_queue.pop(0)
        if to_explore not in GRAPH:
            assert True == False, f'node {to_explore} not in GRAPH'
        val_at = GRAPH[to_explore]

        if val_at == _WORLD_MAPPING['OXYGEN']:
            found_pos = to_explore
            break

        # Find all neighbors, enqueue ones that you haven't visited yet.
        for direction in Direction:
            nbr_pos = calc_pos(to_explore, direction)
            if nbr_pos not in GRAPH:
                continue
            if GRAPH[nbr_pos] == _WORLD_MAPPING['WALL']:
                continue
            if nbr_pos not in came_from:
                came_from[nbr_pos] = to_explore
                explore_queue.append(nbr_pos)

    if not found_pos:
        print(f'Uh Oh')
        return

    path_len = 0
    while found_pos != (0, 0):
        GRAPH[found_pos] = _WORLD_MAPPING['VISITED']
        found_pos = came_from[found_pos]
        path_len += 1

    return path_len


def find_filling_time():
    position = OXYGEN_POSITION
    explore_queue1 = [position]
    explore_queue2 = []
    visited = set()

    explore_queue = explore_queue1
    next_queue = explore_queue2
    rounds = 0

    while (len(explore_queue1)>0 or len(explore_queue2)>0):
        while (len(explore_queue) > 0):
            to_explore = explore_queue.pop(0)

            if to_explore not in GRAPH:
                assert True == False, f'node {to_explore} not in GRAPH'
            val_at = GRAPH[to_explore]
            GRAPH[to_explore] = 'O'

            # Find all neighbors, enqueue ones that you haven't visited yet.
            for direction in Direction:
                nbr_pos = calc_pos(to_explore, direction)
                if nbr_pos not in GRAPH:
                    continue
                if GRAPH[nbr_pos] == _WORLD_MAPPING['WALL']:
                    continue
                if nbr_pos not in visited:
                    visited.add(to_explore)
                    next_queue.append(nbr_pos)
        rounds += 1
        explore_queue, next_queue = next_queue, explore_queue
        print_graph(GRAPH)

    return rounds

def run_parta():
    program = read_input()
    c = Computer(program=program, debug=DEBUG)
    make_graph(c)
    print('DONE making graph')
    print_graph(GRAPH)
    #print(find_shortest_path())
    #print_graph(GRAPH)
    print(f"Filling time: {find_filling_time()}")

    # Find a path

    # N N N N E N E N E -> problem: backtracking sucks with the turtle

    # BFS
    # For each d:
    #   d if suceed: d_inv, go to next iteration
    #   d if wall: ok go to next iteration
    #   d if goal: end
    # Explore N E S W
    # Then of availble neighbors, move and repeat
    # Store in queue the set of nodes/positions to explore
    # Store in dict where you came from / direction you took to get there. Only updated once on way in
    #

    ############
    # 2  #oxxxx#
    #      xxxD#
    ############

    ############
    # 2  #XOX   #
    #     NAX   #
    ############

    # Find the thing via some search
    # Find the shortest path


def read_input(filename='day15.in'):
    with open(filename, 'r') as f:
        program = [int(x) for x in f.readline().strip().split(',')]
        return program


run_parta()
