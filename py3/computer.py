import dataclasses
from typing import List, Optional

input_program = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,31,68,225,1001,13,87,224,1001,224,-118,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1,174,110,224,1001,224,-46,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1101,13,60,224,101,-73,224,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1101,87,72,225,101,47,84,224,101,-119,224,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1101,76,31,225,1102,60,43,225,1102,45,31,225,1102,63,9,225,2,170,122,224,1001,224,-486,224,4,224,102,8,223,223,101,2,224,224,1,223,224,223,1102,29,17,224,101,-493,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,1102,52,54,225,1102,27,15,225,102,26,113,224,1001,224,-1560,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1002,117,81,224,101,-3645,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,344,101,1,223,223,108,677,226,224,102,2,223,223,1006,224,359,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,374,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,389,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,419,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,434,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,449,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,464,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,494,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,509,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,524,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,539,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,569,101,1,223,223,1008,226,677,224,102,2,223,223,1005,224,584,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,629,101,1,223,223,107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,659,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226]


"""
Here are the initial and final states of a few more small programs:

1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
Once you have a working computer, the first step is to restore the gravity assist program (your puzzle input) to the "1202 program alarm" state it had just before the last computer caught fire. To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?

Opcode 3 takes a single integer as input and saves it to the position given
by its only parameter. For example, the instruction 3,50 would take an input value
and store it at address 50.
Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50
would output the value at address 50.

Your computer is only missing a few opcodes:

Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from
the second parameter. Otherwise, it does nothing.
Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from
 the second parameter. Otherwise, it does nothing.
Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
 given by the third parameter. Otherwise, it stores 0.
Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
 given by the third parameter. Otherwise, it stores 0.


1: add
2: multiply
3: input
4: output
5: jump-if-true
6: jump-if-false
7: less-than
8: equals
99: stop

* Support 3 and 4 opcode, maintaining output, input
* Support parameters
* Testing rig

"""

from typing import Tuple, List

day2_test_examples= [
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
    ]

day5_test_examples = [
    ([3,0,4,0,99], -1, -1, [-1,0,4,0,99]),
    ([3,0,4,1,99], -1, 0, [-1,0,4,1,99]),
    ([1002,4,3,4,33], 0, None, [1002,4,3,4,99] ),
    ([1101,100,-1,4,0], 0, None, [1101,100,-1,4,99])
]

day5_2_test_examples = [
    ([3,9,8,9,10,9,4,9,99,-1,8], 8, 1),
   ([3,9,8,9,10,9,4,9,99,-1,8], -1, 0),
   ([3,9,7,9,10,9,4,9,99,-1,8], -1, 1),
   ([3,9,7,9,10,9,4,9,99,-1,8], 8, 0),
   ([3,3,1108,-1,8,3,4,3,99], 8, 1),
]

long_test_program = [
   3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

"""
The above example program uses an input instruction to ask for a single number. The program will
then output 999 if the input value is below 8, output 1000 if the input value is equal to 8,
or output 1001 if the input value is greater than 8.
"""

# (program, input, expected_output)
day5_jump_test_examples = [
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0, 0), # (using position mode)
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 5, 1), # (using position mode)
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0, 0 ),  # (using immediate mode)
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 9, 1 ),  # (using immediate mode)
    (long_test_program, -1, 999),
    (long_test_program, 7, 999),
    (long_test_program, 8, 1000),
    (long_test_program, 9, 1001),
    (long_test_program, 32, 1001),
]


class ComputerError(Exception):
    pass

@dataclasses.dataclass
class ProgramOutput(object):
    opcode : int 
    output : List[int]


class Computer:
    """I compute."""

    EMPTY_LOCATION_ = -1
    
    def __init__(self, program, debug=False):
        self.program_ = program.copy()
        self.program_.extend([0]*10000)
        self.input_ = None
        self.output_ = []
        self.debug_ = debug
        self.index_ = 0
        self.relative_base_ = 0

        # Check self.input_
    
    def parse_params(self, operands : List, params : List):
        # params = list of values, each value is in {0, 1, 2}
        # operands = list of values that will be dereferenced or used directly
        # len(params) <= len(operands)
        if len(params) > len(operands):
            raise ComputerError('len(params) > len(operands): '
                                'params=%s, operands=%s' % (params, operands))
        output = []
        for i, operand in enumerate(operands):
            p = 0  # parameter mode: 0 (relative), 1 (direct), 2 (relative base)
            if i < len(params):
               p = params[i]
            if p == 0:
                output.append(self.program_[operand])
            elif p == 1:
                output.append(operand)
            elif p == 2:
                output.append(self.program_[operand + self.relative_base_])
            else:
                raise ComputerError('Found a parameter idk how to handle. '
                                    'p=%d, i=%d, operand=%s, operands=%s' % (p, i, operand, operands))
        return output

    def parse_params_for_addr(self, i: int, operands: List, params: List):
        if len(params) > len(operands):
            raise ComputerError('len(params) > len(operands): '
                                'params=%s, operands=%s' % (params, operands))
        if i >= len(operands):
            raise ComputerError('i >= len(operands): '
                                'i=%d, params=%s, operands=%s' % (i, params, operands))
        p = 0  # parameter mode: 0 (relative), 1 (direct), 2 (relative base)
        operand = operands[i]
        if i < len(params):
           p = params[i]
        if p == 0:
            return operand
        elif p == 1:
            return operand  # or throw error??
        elif p == 2:
            return operand + self.relative_base_

        raise ComputerError('Found a parameter idk how to handle. '
                            'p=%d, i=%d, operand=%s, operands=%s' % (p, i, operand, operands))


    
    def op_input(self, loc_1, params):
        read_position = self.parse_params_for_addr(0, [loc_1], params=params)
        if self.input_ == None:
            # raise(f'input op called with no input vals! {loc_1} {params}')
            return False
        self.program_[read_position] = self.input_
        self.input_ = None
        return True

    def op_output(self, loc_1, params):
        out_val = self.parse_params([loc_1], params=params)[0]
        self.output_.append(out_val)

        if self.debug_:
            print (f"Got output ({len(self.output_)}): {self.output_}")

    def op_adjust_relative_base(self, loc_1, params):
        orig_base = self.relative_base_

        adjustment = self.parse_params([loc_1], params=params)[0]
        self.relative_base_ += adjustment

        if self.debug_:
            print (f"Adjusting relative base from: {orig_base} to : {self.relative_base_}")


    def op_add(self, loc_1, loc_2, out_loc, params):
        operands = [loc_1, loc_2, out_loc]
        val1, val2, _ = self.parse_params(operands, params=params)
        out_pos = self.parse_params_for_addr(2, operands, params=params)

        output_val = val1 + val2
        self.program_[out_pos] = output_val
        if self.debug_:
            print(f'add: set {out_pos} to {output_val}')
        
    def op_multiply(self, loc_1, loc_2, out_loc, params):
        operands = [loc_1, loc_2, out_loc]
        val1, val2, _ = self.parse_params(operands, params=params)
        out_pos = self.parse_params_for_addr(2, operands, params=params)

        output_val = val1 * val2
        self.program_[out_pos] = output_val
        if self.debug_:
            print(f'multiply: set {out_pos} to {output_val}')

    def print_output(self):
        print(self.output_)
   
    def parse_opcode(self, op_code_str) -> Tuple[int, List[int]]:
        # 101102 -> 2, [1, 1, 0, 1]
        op_code = int(op_code_str[-2:])
        op_code_str = op_code_str[:-2][::-1]  # reverse the string
        return (op_code, [int(x) for x in op_code_str])

    def op_jump_if_true(self, loc_1, loc_2, params):
        val1, val2 = self.parse_params([loc_1, loc_2], params=params)
        if val1 != 0:
            if self.debug_:
                print(f'jumping-if-true to {val2} (val1={val1} == 1)')
            return val2
        if self.debug_:
            print(f'not jumping-if-true (val1={val1} != 0): {loc_1}, {loc_2}, {params}')
        return self.EMPTY_LOCATION_

    def op_jump_if_false(self, loc_1, loc_2, params):
        val1, val2 = self.parse_params([loc_1, loc_2], params=params)
        if val1 == 0:
            if self.debug_:
                print(f'jumping-if-false to {val2} (val1={val1} == 0)')
            return val2
        if self.debug_:
            print(f'not jumping-if-false (val1={val1} != 0): {loc_1}, {loc_2}, {params}')
        return self.EMPTY_LOCATION_

    def op_less_than(self, loc_1, loc_2, out_loc, params):
        operands = [loc_1, loc_2, out_loc]
        val1, val2, _ = self.parse_params(operands, params=params)
        out_pos = self.parse_params_for_addr(2, operands, params=params)

        output_val = 1 if (val1 < val2) else 0
        self.program_[out_pos] = output_val
        if self.debug_:
            print(f'less-than: set loc {out_pos} to val {output_val}')
        
    def op_equals(self, loc_1, loc_2, out_loc, params):
        operands = [loc_1, loc_2, out_loc]
        val1, val2, _ = self.parse_params(operands, params=params)
        out_pos = self.parse_params_for_addr(2, operands, params=params)

        output_val = 1 if (val1 == val2) else 0
        self.program_[out_pos] = output_val
        if self.debug_:
            print(f'equals: set loc {out_pos} to val {output_val}')
        
    """
    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from
    the second parameter. Otherwise, it does nothing.
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from
     the second parameter. Otherwise, it does nothing.
    Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
     given by the third parameter. Otherwise, it stores 0.
    Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
     given by the third parameter. Otherwise, it stores 0.
    """

    def run_program(self, program_input:Optional[int]) -> ProgramOutput:
        # Maybe revisit these asserts in the future.
        # For now, Computers are single use only.
        # assert self.input_ == None
        self.input_ = program_input
        # assert self.input_ != None
        # assert type(self.input_) == int
        self.output_ = []

        # IF THINGS ARE FUCKED, CHECK:
        # reset relative base
        # self.relative_base_ = 0
        # reset input?
        # reset output?

        # for i in range(0,len(self.program_),4):
        while(self.index_ < len(self.program_)):
            op_code_full = self.program_[self.index_]
            op_code_str = str(op_code_full)
            op_code, params = self.parse_opcode(op_code_str)

            if self.debug_:
                print(f'self.index_: {self.index_}, op_code: {op_code_full}, params: {params}')
            if op_code == 1:
                self.op_add(*self.program_[self.index_+1:self.index_+4], params)
                self.index_ += 4
            elif op_code == 2:
                self.op_multiply(*self.program_[self.index_+1:self.index_+4], params)
                self.index_ += 4
            elif op_code == 3:
                success = self.op_input(self.program_[self.index_+1], params)
                if not success:
                    return ProgramOutput(opcode=op_code, output=self.output_)
                self.index_ += 2
            elif op_code == 4:
                self.op_output(self.program_[self.index_+1], params)
                self.index_ += 2
            elif op_code == 5:
                ip = self.op_jump_if_true(*self.program_[self.index_+1:self.index_+3], params)
                if ip == self.EMPTY_LOCATION_:
                    self.index_ += 3
                else:
                    self.index_ = ip
            elif op_code == 6:
                ip = self.op_jump_if_false(*self.program_[self.index_+1:self.index_+3], params)
                self.index_ = (self.index_ + 3) if ip == self.EMPTY_LOCATION_ else ip
            elif op_code == 7:
                self.op_less_than(*self.program_[self.index_+1:self.index_+4], params)
                self.index_+=4
            elif op_code == 8:
                self.op_equals(*self.program_[self.index_+1:self.index_+4], params)
                self.index_+=4
            elif op_code == 9:
                self.op_adjust_relative_base(self.program_[self.index_+1], params)
                self.index_ += 2
            elif op_code == 99:
                return ProgramOutput(opcode=op_code, output=self.output_)
            else:
                raise ComputerError('fuck idk what to do with %d' % op_code)
        raise ComputerError('Reached the end of the program without hitting halt.')
            
    def get_final_program(self):
        return self.program_
        
"""
def day2_test():
    for input_p, output_p in day2_test_examples:
      c = Computer(input_p, 0)
      c.run_program()
      actual = c.get_final_program()
      assert actual == output_p, f"Input: {input_p}, Actual: {actual}, Expected: {output_p}"
      
day2_test()

def day5_test():
    for input_p, input_value, output_expected, output_p in day5_test_examples:
      c = Computer(input_p,input_value,False)
      output_ = c.run_program()
      actual = c.get_final_program()
      assert actual == output_p, f"Input: {input_p}, Actual: {actual}, Expected: {output_p}"
      assert output_ == output_expected, f"Program Complete: {input_p} Output: {output_}, Expected: {output_expected}"

day5_test()

def day5_2_test():
    for input_p, input_value, output_expected in (day5_2_test_examples + day5_jump_test_examples):
      c = Computer(input_p,input_value,False)
      output_ = c.run_program()
      actual = c.get_final_program()
      #assert actual == output_p, f"Input: {input_p}, Actual: {actual}, Expected: {output_p}"
      assert output_ == output_expected, f"Program Complete: {input_p} Output Program: {actual} Output: {output_}, Expected: {output_expected}"
day5_2_test()

def run_part_a(program, p_input):
    c = Computer(program, p_input, True)
    output = c.run_program()
    output_program = c.get_final_program()
    return output

print('Part b: %s' % run_part_a(input_program, 5))
    
# def find_noun_verb(target, input_p):
#     original_p = input_p.copy()
#     for noun in range(0,100):
#         for verb in range(0,100):
#             input_p = original_p
#             input_p[1] = noun
#             input_p[2] = verb
#             c = Computer(input_p)
#             c.run_program()
#             if c.get_final_program()[0] == target:
#                 return (noun,verb)
#     print('I am sad. Couldnt find matching noun/verb.')
#     return None

# def run_part_b(target, p):
#   return find_noun_verb(target, p)
  
# print(f"Part b: {run_part_b(19690720, input_program)}")



"""
