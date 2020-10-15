input_program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,2,6,23,27,1,6,27,31,2,31,9,35,1,35,6,39,1,10,39,43,2,9,43,47,1,5,47,51,2,51,6,55,1,5,55,59,2,13,59,63,1,63,5,67,2,67,13,71,1,71,9,75,1,75,6,79,2,79,6,83,1,83,5,87,2,87,9,91,2,9,91,95,1,5,95,99,2,99,13,103,1,103,5,107,1,2,107,111,1,111,5,0,99,2,14,0,0]


"""
Here are the initial and final states of a few more small programs:

1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
Once you have a working computer, the first step is to restore the gravity assist program (your puzzle input) to the "1202 program alarm" state it had just before the last computer caught fire. To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?

1: add
2: multiply
99: stop
"""


test_examples= [
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
    ]
    
class Computer:
    """I compute."""
    
    def __init__(self, program):
        self.program_ = program.copy()
    
    def op_add(self, loc_1, loc_2, out_loc):
        self.program_[out_loc] = self.program_[loc_1] + self.program_[loc_2]
        
    def op_multiply(self, loc_1, loc_2, out_loc):
        self.program_[out_loc] = self.program_[loc_1] * self.program_[loc_2]
    
    def run_program(self):
        for i in range(0,len(self.program_),4):
            op_code = self.program_[i]
            if op_code == 1:
                self.op_add(*self.program_[i+1:i+4])
            elif op_code == 2:
                self.op_multiply(*self.program_[i+1:i+4])
            elif op_code == 99:
                return
            else:
                print('fuck idk what to do with %d' % op_code)
            
    def get_final_program(self):
        return self.program_
        
    
def test():
    for input_p, output_p in test_examples:
      c = Computer(input_p)
      c.run_program()
      actual = c.get_final_program()
      assert actual == output_p, f"Input: {input_p}, Actual: {actual}, Expected: {output_p}"
      
test()

def run_part_a(p):
    c = Computer(p)
    c.run_program()
    output = c.get_final_program()
    print(output)
    return output[0]


print('Part a: %s' % run_part_a(input_program))
    
    
def find_noun_verb(target, input_p):
    original_p = input_p.copy()
    for noun in range(0,100):
        for verb in range(0,100):
            input_p = original_p
            input_p[1] = noun
            input_p[2] = verb
            c = Computer(input_p)
            c.run_program()
            if c.get_final_program()[0] == target:
                return (noun,verb)
    print('I am sad. Couldnt find matching noun/verb.')
    return None

def run_part_b(target, p):
  return find_noun_verb(target, p)
  
print(f"Part b: {run_part_b(19690720, input_program)}")


