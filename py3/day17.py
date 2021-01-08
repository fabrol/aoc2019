from computer import Computer
import itertools
from typing import List
import enum


DEBUG_17 = True
DEBUG = False

def read_input(filename='day17.in'):
    with open(filename, 'r') as f:
        program = [int(x) for x in f.readline().strip().split(',')]
        return program

def parse_graph(program_output):
    width = program_output.index(10)

    grid = []
    row = []
    for c in program_output:
        if c == 10:
            grid.append(row)
            row = []
        else:
            row.append(chr(c))
    return grid

def print_graph(grid):
    for row in grid:
        print(''.join(row))

def find_intersections(grid):
    intersections = set()
    for i in range(1, len(grid) - 2):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] == '#':
                above = (grid[i-1][j] == '#')
                below = (grid[i+1][j] == '#')
                left = (grid[i][j-1] == '#')
                right = (grid[i][j+1] == '#')
                if above and below and left and right:
                    intersections.add((i, j))
    return intersections


_TURN_DIRECTION = {
    # (curr_dir, new_dir): R or L
    ('^', '>'): 'R',
    ('^', '<'): 'L',

    ('>', '^'): 'L',
    ('>', 'v'): 'R',

    ('<', '^'): 'R',
    ('<', 'v'): 'L',

    ('v', '>'): 'L',
    ('v', '<'): 'R',
}

def visit_scaffolds(grid):
    # Find robot
    # Path in the form of (DIR_TO_TURN, UNIT_TO_MOVE) pairs
    loc = ((0,2),'^')
    visited = set()
    instructions = []
    while True:
        to_visit = None

        for i, j, new_dir in [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]:
            neighbor = (loc[0][0]+i, loc[0][1]+j)
            if (neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= (len(grid) - 1)
                    or neighbor[1] >= len(grid[0])):
                continue
            if grid[neighbor[0]][neighbor[1]] != '#':
                continue

            # Have I visited before?
            if neighbor in visited:
                continue
            assert to_visit is None, f'to_visit is already set to {to_visit} ({neighbor})'

            turn_direction =  _TURN_DIRECTION[(loc[1], new_dir)]  
            to_visit = (neighbor, new_dir, turn_direction)
            break

        if to_visit is None:
            break

        if DEBUG_17:
            print (f'Attempting: {loc} -> {neighbor}, {new_dir}, {turn_direction}, ({i}, {j})')
        # 2. Calculate max units available to move
        moves = 1
        final_pos = None
        new_row, new_col = neighbor
        while True:
            new_row += i
            new_col += j
            if (new_row < 0 or new_col < 0 or new_row >= (len(grid) - 1)
                    or new_col >= len(grid[0])):
                break
            if grid[new_row][new_col] != '#':
                break
            visited.add((new_row, new_col))
            moves += 1
            final_pos = (new_row, new_col)


        if DEBUG_17:
            print(f'  Moved: {loc} -> {final_pos}, {new_dir} ({turn_direction},{moves})')

        # 3. Save direction turned and number of units moved and current direction
        instructions.extend([turn_direction, moves])
        # 4. Move there
        loc = (final_pos, new_dir)

    return visited, instructions

def run_parta():
    program = read_input()
    c = Computer(program=program, debug=DEBUG)
    output = c.run_program(None)
    grid = parse_graph(output.output)
    print_graph(grid)
    inters = find_intersections(grid)
    print(inters)
    print('Sum: %s' % sum([i*j for i, j in inters]))
     # 1D -> 2D via "10"
    #make_graph(c)
    # intersection: me, me+{above,left,right,below}



def get_steps():
    steps = ['R', 6, 'R', 6, 'R', 8, 'L', 10, 'L', 4, 'R', 6, 'L', 10, 'R', 8,
             'R', 6, 'L', 10, 'R', 8, 'R', 6, 'R', 6, 'R', 8, 'L', 10, 'L', 4,
             'L', 4, 'L', 12, 'R', 6, 'L', 10, 'R', 6, 'R', 6, 'R', 8, 'L', 10,
             'L', 4, 'L', 4, 'L', 12, 'R', 6, 'L', 10, 'R', 6, 'R', 6, 'R', 8,
             'L', 10, 'L', 4, 'L', 4, 'L', 12, 'R', 6, 'L', 10, 'R', 6, 'L', 10, 'R', 8]
    
    A = ['R', 6, 'R', 6, 'R', 8, 'L', 10, 'L', 4]
    B = ['R', 6, 'L', 10, 'R', 8]
    C = ['L', 4, 'L', 12, 'R', 6, 'L', 10]

    main_dict = {'A': A, 'B': B, 'C': C}
    main_routine = ['A', 'B', 'B', 'A', 'C', 'A', 'C', 'A', 'C','B']
    new_steps = []
    for x in main_routine:
        new_steps.extend(main_dict[x])

    assert steps == new_steps, f'Steps: {steps} New_steps: {new_steps}'

    steps = [str(x) for x in steps]
    
    def list_to_input_fn(arr):
        res = []
        for x in arr:
            res.extend([ord(a) for a in str(x)] + [ord(',')])
        res[-1] = 10
        return res

    input_to_run = [list_to_input_fn(main_routine), list_to_input_fn(A), list_to_input_fn(B), list_to_input_fn(C)]
    return input_to_run
    #steps_str = ''.join([str(x) for x in steps])
    # 3 substrings, full coverage (one-time combo of substrings reassembles to steps)
    # identify substrings that are repeated, ordered by length
    # 'R6', 'R6', 'R8', 'L10', 'L4', 'R6', 'L10',
    '''
    1 2 3 -> A,B,C
    1 2 3 1 2 3 -> A=1, B=2, C=3 or A=12, B=31, C=23. If length(str) > 20*3 => easy split isn't possible
    1 2 3 


    ['R6', 'R6', 'R8',
    'L10', 'L4', 'R6', 'L10', 'R8',
    'R6', 'L10',
    'R8',
    'R6', 'R6', 'R8',
    'L10', 'L4',
    'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8',
    'L10', 'L4', 'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10',
    'R6', 'L10']

    ['R6', 'R6', 'R8', 'L10', 'L4',
    'R6', 'L10',  'R8',
    'R6', 'L10', 'R8',
    'R6', 'R6', 'R8', 'L10', 'L4', 'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8', 'L10', 'L4', 'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8', 'L10', 'L4', 'L4', 'L12', 'R6', 'L10',
    'R6', 'L10']

   # solution?
   ['R6', 'R6', 'R8', 'L10', 'L4',
    'R6', 'L10', 'R8',
    'R6', 'L10', 'R8',
    'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10',
    'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10',
    'R6', 'L10', 'R8'] 
    A, B, B, A, C, A, C, A, C, B
    


    'R6', 'R6', 'R8', 'L10', 'L4', 'R6', 'L10', 'R8', 'R6',
    'L10', 'R8', 'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10', 'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10', 'R6', 'R6', 'R8', 'L10', 'L4',
    'L4', 'L12', 'R6', 'L10', 'R6', 'L10']
    '''


def run_partb():
    main_routine, A, B, C = get_steps()
    program = read_input()
    c = Computer(program=program, debug=DEBUG)
    def pass_input(in_arr, expect_input=True):
        for i in in_arr:
            output = c.run_program(program_input=i)
            if expect_input:
                assert output.opcode == 3
        return output

    pass_input(main_routine)
    pass_input(A)
    pass_input(B)
    pass_input(C)
    video = [ord('n'), 10]
    output = pass_input(video, expect_input=False)
    grid = parse_graph(output.output)
    print_graph(grid)
    print(output.output[-1])
    #visited, instructions = visit_scaffolds(grid)
    #print (instructions)

#run_parta()
run_partb()
# part b answer: 1022165