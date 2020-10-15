from computer import Computer
import itertools
from typing import List
import numpy as np


DEBUG = False

_TO_TILE = {
    0: ' ',  # empty
    1: '|',  # wall
    2: 'x',  # block
    3: '-',  # paddle
    4: 'o',  # ball
}

BOARD = None

def display(triples):
    # tiles = [t[2] for t in triples]
    # wall_tiles = [t for t in tiles if t == 1]
    global BOARD
    if BOARD is None:
        print('First few triples: %s' % triples[:10])
        max_x = max([t[0] for t in triples]) + 1
        max_y = max([t[1] for t in triples]) + 1
        BOARD = []
        for _ in range(max_y):
            BOARD.append([' '] * max_x)
        print(f'max_x: {max_x} max_y: {max_y} ')

    for triple in triples:
        # x is from left, y is from top
        x, y, tile_id = triple
        #print(f'x: {x} y: {y} {tile_id}')
        BOARD[y][x] = _TO_TILE[tile_id]
        tile = _TO_TILE[tile_id]
        #print(f'x: {x} y: {y} {tile}')
    for row in BOARD:
        print(''.join(row))
        


def run_part_1():
    program = read_input()
    c = Computer(program=program, debug=DEBUG)
    p_output = c.run_program(None)
    output = p_output.output
    triples = [output[i: i+3] for i in range(0,len(output),3)]  # list of (x, y, tile)
    print('First few triples: %s' % triples[:10])
    tiles = [t[2] for t in triples]
    block_tiles_n = sum([x == 2 for x in tiles])
    print (f'Block tiles: {block_tiles_n}')


def run_part_2():
    program = read_input()
    c = Computer(program=program, debug=DEBUG)

    output_op = None
    next_input = 0
    ball_last_pos = None

    while output_op != 99:
        p_output = c.run_program(next_input)
        output = p_output.output
        output_op = p_output.opcode

        triples = [output[i: i+3] for i in range(0,len(output),3)]  # list of (x, y, tile)
        triples_display = list(filter(lambda p : p[0] != -1, triples))
        display(triples_display)

        score = list(filter(lambda p : p[0] == -1, triples))
        if score:
            print (f"Score: {score[0][2]}")

        ball_pos_x = list(filter(lambda p : p[2] == 4, triples))[0][0]
        paddle_pos_x = list(filter(lambda p : p[2] == 3, triples))[0][0]
        if output_op == 3:
            joystick = 0
            if ball_pos_x > paddle_pos_x:
                joystick = 1
            elif ball_pos_x < paddle_pos_x:
                joystick = -1

            next_input = joystick # int(input())

def read_input(filename='day_13.in'):
    with open(filename, 'r') as f:
        program = [int(x) for x in f.readline().split(',')]
        return program

# run_tests(part_a_testcases)

# run_part_1()
run_part_2()

"""
 The software draws tiles to the screen with output instructions: every three output instructions specify the x position (distance from the left), y position (distance from the top), and tile id. The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

"""
