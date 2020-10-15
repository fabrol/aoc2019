from typing import Tuple, Dict
import pprint

class OreNode(object):
    def __init__(self):
        self.amount = 0

    def produce(self, num_output: int, name_to_node: Dict):
        self.amount += num_output

    def __str__(self):
        return f'Ore : {self.amount}'

class Node(object):

    def __init__(self, inputs : Dict[str, int], output: Tuple[str, int]):
        self.inputs = inputs
        self.name = output[0]
        self.output_qty = output[1]
        self.avail_produced = 0

    def __str__(self):
        reaction = ['%s %s' % (self.inputs[k], k) for k in sorted(self.inputs)]
        return f'{self.name}: Reaction: {"".join(reaction)} -> {self.output_qty} {self.name}'

    def react(self, name_to_node: Dict, num_reactions: int):
        for element, amt in self.inputs.items():
            name_to_node[element].produce(num_output = amt*num_reactions, name_to_node = name_to_node)

    def produce(self, num_output: int, name_to_node: Dict):
        # This means some reaction is requiring this quantity.

        # Don't need a reaction b/c we already produced stuff \o/
        if num_output <= self.avail_produced:
            self.avail_produced -= num_output
            return
        
        to_produce = num_output - self.avail_produced

        num_reactions = to_produce // self.output_qty
        leftover = to_produce % self.output_qty
        if leftover:
            num_reactions += 1

        produced = num_reactions * self.output_qty
        # Examples
        #    6 // 3 -> 2  (want: 2)
        #    3 // 3 -> 1  (want: 1)
        #    5 // 3 -> 1  (want: 2)
        #    3 // 6 -> 0  (want: 1)
        '''
        while to_produce > 0:
            # Run 1 reaction. (for each node: input_node.produce(x))
            num_reactions += 1
            to_produce -= self.output_qty
            produced += self.output_qty
        '''

        self.react(name_to_node, num_reactions)

        # self.avail_produced = to_produce % self.output_qty
        #print(f'{self.name}: Produced {produced}, num_output={num_output}, orig={orig_to_produce}')
        assert (produced >= to_produce)
        self.avail_produced = produced - to_produce
        

        
        


def read_input(filename='day14.in'):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def parse(input_str):
    name_to_node = {}

    for line in input_str.split('\n'):
        if line.strip() == '':
            continue

        inputs, output = line.strip().split('=>')
        def chem_to_tuple(st, input_dict):
            amt, name = st.strip().split()
            amt = int(amt)
            if input_dict is not None:
                input_dict[name] = amt
            return (name, amt)

        input_dict = {}
        inputs = [chem_to_tuple(x, input_dict) for x in inputs.split(',')]
        output = chem_to_tuple(output, None)

        n = Node(input_dict, output)
        name_to_node[output[0]] = n

    ore_node = OreNode()
    name_to_node['ORE'] = ore_node

    # for _, node in name_to_node.items():
    #     print(f'{node}')
    return name_to_node

def run(input_str, fuel_amt=1):
    name_to_node = parse(input_str)
    name_to_node['FUEL'].produce(fuel_amt, name_to_node)
    return name_to_node['ORE'].amount


test_cases_a = [
    ("""
     10 ORE => 10 A
     1 ORE => 1 B
     7 A, 1 B => 1 C
     7 A, 1 C => 1 D
     7 A, 1 D => 1 E
     7 A, 1 E => 1 FUEL
     """, 31),
    ("""
     9 ORE => 2 A
     8 ORE => 3 B
     7 ORE => 5 C
     3 A, 4 B => 1 AB
     5 B, 7 C => 1 BC
     4 C, 1 A => 1 CA
     2 AB, 3 BC, 4 CA => 1 FUEL
     """, 165),
    ("""
     157 ORE => 5 NZVS
     165 ORE => 6 DCFZ
     44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
     12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
     179 ORE => 7 PSHF
     177 ORE => 5 HKGWZ
     7 DCFZ, 7 PSHF => 2 XJWVT
     165 ORE => 2 GPVTF
     3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
     """, 13312),
     ("""
      2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
      17 NVRVD, 3 JNWZP => 8 VPVL
      53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
      22 VJHF, 37 MNCFX => 5 FWMGM
      139 ORE => 4 NVRVD
      144 ORE => 7 JNWZP
      5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
      5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
      145 ORE => 6 MNCFX
      1 NVRVD => 8 CXFTF
      1 VJHF, 6 MNCFX => 4 RFSQX
      176 ORE => 6 VJHF
      """, 180697),
     ("""
     171 ORE => 8 CNZTR
     7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
     114 ORE => 4 BHXH
     14 VRPVC => 6 BMBT
     6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
     6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
     15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
     13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
     5 BMBT => 4 WPTQ
     189 ORE => 9 KTJDG
     1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
     12 VRPVC, 27 CNZTR => 2 XDBXC
     15 KTJDG, 12 BHXH => 5 XCVML
     3 BHXH, 2 VRPVC => 7 MZWV
     121 ORE => 7 VRPVC
     7 XCVML => 6 RJRHP
     5 BHXH, 4 VRPVC => 5 LTCX
     """, 2210736),
]

test_cases_b = [
    ("""
     157 ORE => 5 NZVS
     165 ORE => 6 DCFZ
     44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
     12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
     179 ORE => 7 PSHF
     177 ORE => 5 HKGWZ
     7 DCFZ, 7 PSHF => 2 XJWVT
     165 ORE => 2 GPVTF
     3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
     """, 82892753, 13312),
]

def test_parta(test_cases):
    # test_cases = [test_cases[0], test_cases[1]]
    for input_str, expected_ore in test_cases:
        ore = run(input_str)
        print(f'Produced ore: {ore}')
        if ore != expected_ore:
            print(f'ERROR: Expected {expected_ore} and got {ore}.')

#test_parta(test_cases_a)

#print(run_parta(read_input()))

def test_partb(test_cases):
    # test_cases = [test_cases[0], test_cases[1]]
    for input_str, output_fuel, expected_ore in test_cases:
        ore_1 = run(input_str, output_fuel)
        ore_2 = run(input_str, output_fuel + 1)
        # 1000000000000 (ore_1 is less, ore_2 is more)
        print(f'Produced ore: {ore_1} {ore_2}')

            
#test_partb(test_cases_b)

# Choose starting min and max numbers
# Start with middle of range
# if < 1 trillion -> increase output_fuel; set new min
# if > 1 trillion -> decrease output_fuel; set new max


def run_partb(input_str, lower, upper, target):
    current_closest_ore = -1
    current_closest_fuel = -1
    while lower <= upper:
        mid = lower + (upper - lower) // 2
        name_to_node = parse(input_str)
        name_to_node['FUEL'].produce(mid, name_to_node)
        ore = name_to_node['ORE'].amount

        if ore < target:
            if ore > current_closest_ore:
                current_closest_fuel = mid
                current_closest_ore = ore
            lower = mid + 1
        elif ore > target:
            upper = mid - 1
        else:
            current_closest_fuel = mid
            current_closest_ore = ore
            print(f'Exactly on target.')
            break
        print (f'Iter {mid} {ore:.8E} with {lower} : {upper} and fuel {current_closest_fuel} and ore {current_closest_ore:.3E}')
    print (f'Got {current_closest_fuel} and {lower} and ore {current_closest_ore}')

    return current_closest_fuel


run_partb(read_input(), 1111111, 2000000, 1000000000000)