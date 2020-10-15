from typing import Tuple, List
from decimal import Decimal
import math as m
from collections import defaultdict


DEBUG = True

def get_best_location(world_str:str) -> Tuple[int,Tuple[int,int]]:
    world = [list(row) for row in world_str.split('\n')]
    world = list(filter(lambda x : x != [], world))
    
    # Parse into a list of coordinates
    coords = []
    for y, row in enumerate(world):
        for x, val in enumerate(row):
            if val == '#':
                coords.append((x, y))

    if DEBUG:
        print (f"Asteroids : {len(coords)}")
        '''
        for coord in coords:
            print (coord)
        '''
       
    reachability_to_coords = {}  # num_reachable_asteriods -> coordinate
    for origin_x, origin_y in coords:
        slopes = set()
        for coord_x, coord_y in coords:
            if coord_x == origin_x and coord_y == origin_y:
                continue
            '''
            if (coord_x - origin_x) == 0 and coord_x > origin_x:
                slopes.add('INFINITE')
                continue
            if (coord_x - origin_x) == 0 and coord_x <= origin_x:
                slopes.add('-INFINITE')
                continue
            '''
            # calculate slope
            angle = m.atan2((coord_y - origin_y),(coord_x - origin_x))
            slope = float(round(angle, 6))
            slopes.add(slope)
            if DEBUG and origin_x == 1 and origin_y == 2:
                print(f'  ({origin_x}, {origin_y}) + ({coord_x}, {coord_y}) slope {slope}')
        reachability_to_coords[len(slopes)] = (origin_x, origin_y)
    # Return the coordinate and number of asteriods for which the max is reachable. 
    if DEBUG:
        print (f"{reachability_to_coords}")
    ret_reachability = max(reachability_to_coords.keys())
    return ret_reachability, reachability_to_coords[ret_reachability]

test_case0 = ("""
.#..#
.....
#####
....#
...##
""", (3, 4), 8)

test_case1 = ("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""", (5, 8), 33)

test_case2 = ("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""", (1, 2), 35)

test_case3 = ("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""", (6,3), 41)

test_case4 = ("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""", (11, 13), 210)

test_cases = [
    test_case0,
    test_case1,
    test_case2,
    test_case3,
    test_case4,
]

def run_test_cases(test_cases):
    for world_str, expected_coords, expected_reachable in test_cases:
        got_reachable, got_coords = get_best_location(world_str) 
        assert (got_reachable == expected_reachable) and (got_coords == expected_coords),\
            f"Expected: f{expected_coords}, f{expected_reachable} Got: f{got_coords}, f{got_reachable}"
    print ("All tests ran successfully")

#run_test_cases(test_cases)

input_str = """
.###.#...#.#.##.#.####..
.#....#####...#.######..
#.#.###.###.#.....#.####
##.###..##..####.#.####.
###########.#######.##.#
##########.#########.##.
.#.##.########.##...###.
###.#.##.#####.#.###.###
##.#####.##..###.#.##.#.
.#.#.#####.####.#..#####
.###.#####.#..#..##.#.##
########.##.#...########
.####..##..#.###.###.#.#
....######.##.#.######.#
###.####.######.#....###
############.#.#.##.####
##...##..####.####.#..##
.###.#########.###..#.##
#.##.#.#...##...#####..#
##.#..###############.##
##.###.#####.##.######..
##.#####.#.#.##..#######
...#######.######...####
#....#.#.#.####.#.#.#.##
"""

print(get_best_location(input_str))

def dist_bw(source, pt):
    return m.sqrt((pt[0] - source[0])**2 + (pt[1] - source[1])**2)

def get_hittable(coords: List[Tuple[int,int]], source:Tuple[int,int]) -> List[Tuple[int,int]]:
    origin_x, origin_y = source

    angles = defaultdict(list)  # angle -> list of ((x, y), dist) at that angle
    for coord_x, coord_y in coords:
        if coord_x == origin_x and coord_y == origin_y:
            continue
        cur_asteroid = (coord_x, coord_y)

        # calculate angle
        angle = m.atan2((coord_y - origin_y),(coord_x - origin_x))
        angle = float(round(angle, 6))
        angles[angle].append((cur_asteroid, dist_bw(source, cur_asteroid)))

    #  (-pi/2, 0), (0, pi/2), (pi/2, pi), (-pi, -pi/2)
    #          -pi/2
    #    4      |      1
    #  -pi/pi -------------- 0
    #   3       |      2
    #         pi/2
    # ordering should be quad1, quad2, quad3, quad4
    # get everything with value in (pi/2, pi)
    # take all those values and subtract 2pi
    # add back to list
    # order from least to greatest (-pi/2 -> pi/2)
    # -3pi/4 + 2pi = 5/4pi
    # -pi + 2pi = pi
    quad4_angles = [a for a in angles if a >= -m.pi and a < -m.pi/2]
    all_angles = sorted(angles, key=lambda a: a + 2*m.pi if a in quad4_angles else a)

    ret = []
    debug_out = []
    for angle in all_angles:
        pts = angles[angle]  # list of (tuple, dist)
        closest_point = sorted(pts, key=lambda x : x[1])[0]
        debug_out.append((closest_point[0],angle))
        ret.append(closest_point[0])
    if DEBUG:
        print (f"{debug_out}")

    return ret


def vaporization_order(world_str, max_asteroids, laser=None):
    world = [list(row) for row in world_str.split('\n')]
    world = list(filter(lambda x : x != [], world))

    coords = []
    laser = laser
    for y, row in enumerate(world):
        for x, val in enumerate(row):
            if val == '#':
                coords.append((x, y))
            if val == 'X':
                laser = (x, y)
    
    if DEBUG:
        print (f"Asteroids : {len(coords)}")
        print (f"Laser : {laser}")

    num_destroyed_asteroids = 0
    overall_order = []
    while num_destroyed_asteroids < max_asteroids:
        order = get_hittable(coords, laser)
        if not order:
            break
        overall_order.extend(order)
        num_destroyed_asteroids += len(order)
        if DEBUG:
            print (f"  {len(order)}: {order}")
        for coord in order:
            coords.remove(coord)
    return overall_order[:max_asteroids]


b_test_case1 = ("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.####X#####...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""", 
[
    (1, (11, 12)),
    (2, (12, 1)),
    (3, (12, 2)),
    (10, (12, 8)),
    (20, (16, 0)),
    (50, (16, 9)),
    (100, (10, 16)),
    (199, (9, 6)),
    (200, (8, 2)),
    (201, (10, 9)),
    (299, (11, 1)),
], 300)

"""
>>> math.atan2(13-12, 11-11) == math.pi/2
True

"""

def run_test_cases_b(cases):
    for world_str, expected_destroyed, max_iter in cases:
        destroyed_order = vaporization_order(world_str, max_iter)
        for expected_i, expected_coord in expected_destroyed:
            assert destroyed_order[expected_i-1] == expected_coord, f"Expected at {expected_i-1}:{expected_coord} Got {destroyed_order[expected_i-1]}"

#run_test_cases_b([b_test_case1])

def run_part_b(world_str, max_iter):
    destroyed_order = vaporization_order(world_str, max_iter, (20,18))
    return destroyed_order[max_iter - 1]

print(run_part_b(input_str, 200))