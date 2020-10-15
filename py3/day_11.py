from computer import Computer
from enum import IntEnum
import itertools
import dataclasses
from typing import List,Set,Tuple

DEBUG = True

puzzle_input = "3,8,1005,8,332,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,28,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,51,1,1103,5,10,1,1104,9,10,2,1003,0,10,1,5,16,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,88,1006,0,2,1006,0,62,2,8,2,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,121,1006,0,91,1006,0,22,1006,0,23,1006,0,1,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,155,1006,0,97,1,1004,2,10,2,1003,6,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,187,1,104,15,10,2,107,9,10,1006,0,37,1006,0,39,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,223,2,2,17,10,1,1102,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,253,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,276,1006,0,84,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,301,2,1009,9,10,1006,0,10,2,102,15,10,101,1,9,9,1007,9,997,10,1005,10,15,99,109,654,104,0,104,1,21102,1,936995738516,1,21101,0,349,0,1105,1,453,21102,1,825595015976,1,21102,1,360,0,1105,1,453,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,46375541763,1,1,21101,0,407,0,1105,1,453,21102,1,179339005019,1,21101,0,418,0,1106,0,453,3,10,104,0,104,0,3,10,104,0,104,0,21102,825012036372,1,1,21102,441,1,0,1105,1,453,21101,988648461076,0,1,21101,452,0,0,1105,1,453,99,109,2,22102,1,-1,1,21102,40,1,2,21102,484,1,3,21101,0,474,0,1106,0,517,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,479,480,495,4,0,1001,479,1,479,108,4,479,10,1006,10,511,1102,1,0,479,109,-2,2105,1,0,0,109,4,2102,1,-1,516,1207,-3,0,10,1006,10,534,21101,0,0,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21102,553,1,0,1106,0,558,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,581,2207,-4,-2,10,1006,10,581,22102,1,-4,-4,1105,1,649,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,0,600,0,1105,1,558,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,619,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,641,22102,1,-1,1,21102,1,641,0,106,0,516,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0"

class Fuck(Exception):
    pass


class Orientation(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

ORIENTATION_TO_DELTA = {
    Orientation.UP : (0,1),
    Orientation.RIGHT : (1,0),
    Orientation.DOWN : (0,-1),
    Orientation.LEFT : (-1,0),
}

def run_painting_robot(input_p):
    c = Computer(program=input_p, debug=False)
    panels = {} # From (X,Y) -> Color
    position = (0,0)
    camera_input = 1  # part a: 0, part b: 1
    orientation = Orientation.UP

    while True:
        # Run program with inputs.
        poutput = c.run_program(program_input=camera_input)
        if poutput.opcode == 99:
            break
        assert poutput.opcode == 3

        # Parse output. 
        assert (len(poutput.output) == 2)
        color, direction = poutput.output

        # Update panels
        panels[position] = color
        if DEBUG:
            print(f'{position}: color={color} dir={direction}')
        
        # Update positions
        # Orientations = 0: UP,1: RIGHT, 2:DOWN, 3:LEFT
        # 0 left 90* -> (Or - 1) % 4 , 1 right 90* -> (Or + 1) % 4
        # Update position
        '''
        offset = 1 if direction == 1 else -1
        orientation = (orientation + offset) % 4
        position = tuple([sum(x) for x in zip(position, ORIENTATION_TO_DELTA[orientation])])
        '''

        # (UP, 0) -> left (x - 1)
        # (DOWN, 1) -> left (x - 1)

        # (UP, 1) -> right (x + 1)
        # (DOWN, 0) -> right (x + 1)

        # (RIGHT, 0) -> up (y + 1)
        # (LEFT , 1) -> up (y + 1)
        
        if ((orientation == Orientation.UP and direction == 0) or
            (orientation == Orientation.DOWN and direction == 1)):
            position = (position[0] - 1, position[1])
            orientation = Orientation.LEFT
        elif ((orientation == Orientation.UP and direction == 1) or
              (orientation == Orientation.DOWN and direction == 0)):
            position = (position[0] + 1, position[1])
            orientation = Orientation.RIGHT
        elif ((orientation == Orientation.RIGHT and direction == 0) or
              (orientation == Orientation.LEFT and direction == 1)):
            position = (position[0], position[1] + 1)
            orientation = Orientation.UP
        elif ((orientation == Orientation.RIGHT and direction == 1) or
              (orientation == Orientation.LEFT and direction == 0)):
            position = (position[0], position[1] - 1)
            orientation = Orientation.DOWN
        else:
            print('fuck')
            raise Fuck('idk what to do')

        # Update camera input
        camera_input = panels.get(position, 0)
        
        if DEBUG:
            #print(f'  {position}: orie={orientation} camera={camera_input} offset={offset}')
            print(f'  {position}: orie={orientation} camera={camera_input}')

    if DEBUG:
        print(panels)

    return panels

def print_panels(panels):
    # panels = dict{(x,y) : color}
    min_x = min(p[0] for p in panels.keys())
    max_x = max(p[0] for p in panels.keys())
    min_y = min(p[1] for p in panels.keys())
    max_y = max(p[1] for p in panels.keys())
    width = max_x - min_x
    height = max_y - min_y

    if DEBUG:
        print(f'Grid: X:{min_x},{max_x} Y:{min_y}, {max_y}')

    for y in range(max_y, min_y - 1, -1):
        print('%4d ' % y, end='')
        for x in range(min_x, max_x):
            if (x,y) in panels:
                c = panels[(x, y)]
                v = ' ' if c == 0 else '#'
                print(v, end='')
            else:
                print(' ', end='')

        print('')
                

    '''
    for y in range(max_y, min_y, -1):
        for x in range(min_x, max_x):
            if (x,y) in panels:
                c = panels[(x, y)]
                v = ' ' if c else '#'
                print(v, end='')
            else:
                print(' ', end='')

        print('')
    '''

    '''
    max_y -> min_y
      min_x -> max_x
        

    if DEBUG:
        print (min_x, max_x, min_y, max_y)

    grid = [['.' for _ in range(width)] for _ in range(height)]
    for (x,y), color in panels.items():
        if color == 1:
            grid[x - min_x][y - min_y] = '#'

    for row in grid:
        print(*row)
    '''

panels = run_painting_robot([int(x) for x in puzzle_input.split(",")])
print(len(panels))
# assert len(panels) == 2373

print_panels(panels)