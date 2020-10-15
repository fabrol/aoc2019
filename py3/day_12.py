import time
from typing import List, Tuple
from collections import defaultdict

part_a_testcases = [
    (
"""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""",
"""\
After 0 steps:
pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

After 1 step:
pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>

After 2 steps:
pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>

After 3 steps:
pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>

After 4 steps:
pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>

After 5 steps:
pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>

After 6 steps:
pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>

After 7 steps:
pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>

After 8 steps:
pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>

After 9 steps:
pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>

After 10 steps:
pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
""", 179),
("""<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""",
"""After 0 steps:
pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>

After 10 steps:
pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>

After 20 steps:
pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>

After 30 steps:
pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>

After 40 steps:
pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>

After 50 steps:
pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>

After 60 steps:
pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>

After 70 steps:
pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>

After 80 steps:
pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>

After 90 steps:
pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>

After 100 steps:
pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>""", 1940
)
]

# List[(Position, Velocity)]
# State = List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]

# Pos: 14, 7, 1, -4   Vel: 0, 0, 0, 0
# Pos: 14, 7, 1, -4   Vel: -3, -1, 1, 3
# Pos: 11, 6, 2, -1   Vel: -3, -1, 1, 3
# Pos: 11, 6, 2, -1   Vel: -3, -1, 1, 3
# Pos:  8, 5, 3,  2   Vel: -3, -1, 1, 3
# Pos:  8, 5, 3,  2   Vel: -3, -1, 1, 3
# Pos:  5, 4, 4,  5   Vel: -3, -1, 1, 3
# Pos:  5, 4, 4,  5   Vel: -2,  2, 2, -2 
# Pos:  3, 6, 6,  3   Vel: -2,  2, 2, -2 
# Pos:  3, 6, 6,  3   Vel:  2, -2, -2, 2 
# Pos:  5, 4, 4,  5   Vel:  2, -2, -2, 2 
 

from dataclasses import dataclass
import re

@dataclass
class Position:
    x: int = 0
    y: int = 0
    z: int = 0

    def update(self, velocity):
        self.x += velocity.x
        self.y += velocity.y
        self.z += velocity.z

    def __repr__(self):
        return f'p=({self.x},{self.y},{self.z})'

    def to_potential(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __hash__(self):
        return hash((self.x,self.y,self.z))

@dataclass
class Velocity:
    x: int = 0
    y: int = 0
    z: int = 0
    
    def __repr__(self):
        return f'v=({self.x},{self.y},{self.z})'

    def change(self, delta, reverse=False):
        multiplier = 1
        if reverse:
            multiplier = -1
        self.x += multiplier * delta[0]
        self.y += multiplier * delta[1]
        self.z += multiplier * delta[2]

    def to_kinetic(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __hash__(self):
        return hash((self.x,self.y,self.z))



@dataclass
class MoonState:
    velocity: Velocity
    position: Position

    def __hash__(self):
        return hash((self.velocity, self.position))
        
    def per_dimension_split(self):
        return ((self.velocity.x, self.position.x),
                (self.velocity.y, self.position.y),
                (self.velocity.z, self.position.z))

_DEBUG = False

def calculate_velocity_delta(a, b):
    delta = [0, 0, 0]
    if a.position.x != b.position.x:
        delta[0] = -1 if a.position.x > b.position.x else 1
    if a.position.y != b.position.y:
        delta[1] = -1 if a.position.y > b.position.y else 1
    if a.position.z != b.position.z:
        delta[2] = -1 if a.position.z > b.position.z else 1
    return delta

def test_calculate():
    m1 = MoonState(position=Position(x=-1, y=0, z=5), velocity=Velocity())
    m2 = MoonState(position=Position(x=2, y=-10, z=5), velocity=Velocity())
    expected = [1, -1, 0]
    inverse = [-1, 1, 0]
    found = calculate_velocity_delta(m1, m2)
    found2 = calculate_velocity_delta(m2, m1)
    assert expected == found, f"Found: {found} Expected: {expected}"
    assert inverse == found2, f"Found: {found2} Expected: {inverse}"

test_calculate()

def simulate_step(moons:List[MoonState]):
    # Velocity learns about gravity
    for i in range(len(moons) - 1):
        for j in range(i+1, len(moons)):
            delta = calculate_velocity_delta(moons[i], moons[j])
            moons[i].velocity.change(delta)
            moons[j].velocity.change(delta, reverse=True)
    
    if _DEBUG:
        print('Done updating velocity.')
        for i in range(len(moons)):
            print(f'Moon {i}:')
            print(moons[i])

    # Positions updated based on velocity
    for moon in moons:
        moon.position.update(moon.velocity)

    if _DEBUG:
        print('Done updating positions.')
        for i in range(len(moons)):
            print(f'Moon {i}:')
            print(moons[i])
    return moons

def test_moons():
    m1 = MoonState(position=Position(x=-1, y=0, z=5), velocity=Velocity())
    m2 = MoonState(position=Position(x=2, y=-10, z=5), velocity=Velocity())
    moons = simulate_step([m1, m2])
    m1 = MoonState(position=Position(x=0, y=-1, z=5), velocity=Velocity())
    m2 = MoonState(position=Position(x=1, y=-9, z=5), velocity=Velocity())

test_moons()

def calculate_energy(moons: List[MoonState]):
    total_energy = 0
    for i, moon in enumerate(moons):
        # potential: sum abs_val of positions
        pot = moon.position.to_potential()

        # kinetic: sum of abs_val of velocity
        kin = moon.velocity.to_kinetic()
        moon_energy = pot * kin
        if _DEBUG:
            print(f'moon {i}: pot={pot}, kin={kin}, moon_energy={moon_energy}')
        total_energy += moon_energy
    if _DEBUG:
        print(f'total_energy: {total_energy}')
    return total_energy
        


def run_part_a_testcases(cases):
    for initial_position, outputs, expected_energy in cases:
        initial_states = []
        for planet_str in initial_position.split('\n'):
            pos = Position(*[int(x) for x in re.findall('(-?\d+)',planet_str)])
            state = MoonState(position=pos, velocity=Velocity())
            initial_states.append(state)

        breaks = {}
        for breakpoints in outputs.split('\n\n'):
            lines = breakpoints.split('\n')

            step_no = int(re.findall('(-?\d+)',lines[0])[0])
            states = []
            for planet in lines[1:]:
                splits = [int(x) for x in re.findall('(-?\d+)',planet)]
                states.append(MoonState(position=Position(*splits[0:3]), velocity=Velocity(*splits[3:6])))
            breaks[step_no] = states
        
        print ("Starting with ", initial_states)

        states = initial_states
        for itr in range(0, max(breaks)):
            if itr in breaks:
                assert states == breaks[itr], f"Itr:{itr} \nExpected:\n{breaks[itr]},\nFound:\n{states}"
            
            states = simulate_step(states)
            
        assert expected_energy == calculate_energy(states), f"Expected: {expected_energy}, Found: {calculate_energy(states)}"

#run_part_a_testcases(part_a_testcases)

part_a_moons = [
    MoonState(position=Position(x=14, y=2, z=8), velocity=Velocity()),
    MoonState(position=Position(x=7, y=4, z=10), velocity=Velocity()),
    MoonState(position=Position(x=1, y=17, z=16), velocity=Velocity()),
    MoonState(position=Position(x=-4, y=-1, z=1), velocity=Velocity())
]

test_moons = [
    MoonState(position=Position(x=-1, y=0, z=2), velocity=Velocity()),
    MoonState(position=Position(x=2, y=-10, z=-7), velocity=Velocity()),
    MoonState(position=Position(x=4, y=-8, z=8), velocity=Velocity()),
    MoonState(position=Position(x=3, y=5, z=-1), velocity=Velocity())
]

test_moons_l = [
    MoonState(position=Position(x=-8, y=-10, z=0), velocity=Velocity()),
    MoonState(position=Position(x=5, y=5, z=10), velocity=Velocity()),
    MoonState(position=Position(x=2, y=-7, z=3), velocity=Velocity()),
    MoonState(position=Position(x=9, y=-8, z=-3), velocity=Velocity())
]

def run_part_a(moons):
    #jhistory = (set(),set(),set()) # (Set{((PX_1,VX_1), PX_2, VX_2, X_3,X_4)} tuples so far), (Set of Y History tuples so far)
    history = set()
    history.add(tuple(moons))
    itr = 0
    while True:
        t = time.time()
        moons = simulate_step(moons)
        if tuple(moons) in history:
            print (f"Found repeat at itr {itr}")
            break
        history.add(tuple(moons))
        itr += 1
        if (itr  == 44):
            print (f"Iteration : {itr} Time taken: {time.time() -t } moons:\n {moons}")

    return calculate_energy(moons)

def run_part_a_per_axis(moons):
    class History:
        def __init__(self):
            self.x = defaultdict(list)
            self.y = defaultdict(list)
            self.z = defaultdict(list)

            self.x_iter_length = None
            self.y_iter_length = None
            self.z_iter_length = None

        def add(self, x, y, z, itr):
            found_x,found_y,found_z = False,False,False

            # Need: iteration length and first encounter
            # max(first_encounters) + LCM(iteration_lengths)

            if x in self.x and self.x_iter_length is None:
                print(f"Found x repeat value {x} at itr: {itr}")
                found_x = True
                self.x_iter_length = itr - self.x[x][0]
            else:
                self.x[x].append(itr)

            if y in self.y and self.y_iter_length is None:
                print(f"Found y repeat value {y} at itr: {itr}")
                found_y = True
                self.y_iter_length = itr - self.y[y][0]
            else:
                self.y[y].append(itr)

            if z in self.z and self.z_iter_length is None:
                print(f"Found z repeat value {z} at itr: {itr}")
                found_z = True
                self.z_iter_length = itr - self.z[z][0]
            else:
                self.z[z].append(itr)

            if (self.x_iter_length and self.y_iter_length and self.z_iter_length):
                print (f"Found all repeat at itr {itr}, {x}, {y}, {z}, "
                       f"Previous itrs: {self.x[x]}, {self.y[y]}, {self.z[z]}"
                       f"itr_lens: {self.x_iter_length}, {self.y_iter_length}, {self.z_iter_length}")
                exit(0)

        def add_moons(self, moons : List[MoonState]):
            x_updates = []
            y_updates = []
            z_updates = []

            #for moon in moons:
            #    for 



    history = History()
    itr = 0
    print( "Adding ,", list(zip(*[m.per_dimension_split() for m in moons])))
    history.add(*zip(*[m.per_dimension_split() for m in moons]), itr)
    while True:
        t = time.time()
        moons = simulate_step(moons)
        '''
        if tuple(moons) in history:
            print (f"Found repeat at itr {itr}")
            break
        '''
        history.add(*zip(*[m.per_dimension_split() for m in moons]), itr)
        itr += 1
        if (itr % 100000) == 0:
            print (f"Iteration : {itr} Time taken: {time.time() -t } moons: {moons}")

    return calculate_energy(moons)
#run_part_a(part_a_moons)
#run_part_a(test_moons)
run_part_a_per_axis(part_a_moons)

# $ python day_12.py 
# Iteration : 43 Time taken: 2.9802322387695312e-05 moons:
#  [MoonState(velocity=v=(3,1,1), position=p=(2,-7,2)),
#  MoonState(velocity=v=(-2,-3,-3), position=p=(1,2,-7)),
#  MoonState(velocity=v=(0,-1,3), position=p=(3,-1,8)),
#  MoonState(velocity=v=(-1,3,-1), position=p=(2,-7,-1))]
# Found repeat at itr 2771

'''
 [MoonState(velocity=v=(3,3,0), position=p=(5,-4,2)), MoonState(velocity=v=(1,-6,0), position=p=(2,-4,-7)), MoonState(velocity=v=(-3,-2,0), position=p=(0,-3,8)), MoonState(velocity=v=(-1,5,0), position=p=(1,-2,-1))]
Found allrepeat at itr 43, ((3, 5), (1, 2), (-3, 0), (-1, 1)), ((3, -4), (-6, -4), (-2, -3), (5, -2)), ((0, 2), (0, -7), (0, 8), (0, -1))
'''