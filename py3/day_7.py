input_program = [3,8,1001,8,10,8,105,1,0,0,21,46,55,72,85,110,191,272,353,434,99999,3,9,1002,9,5,9,1001,9,2,9,102,3,9,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,4,9,99,3,9,1002,9,3,9,101,5,9,9,1002,9,3,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99]
from computer import Computer
import itertools
from typing import List

_DEBUG = False

def compute_amp_serial_output(amps: List[Computer], phase_sequence:List[int]):
    input = 0
    output = None

    # Initialize loop
    for i, amp in enumerate(amps):
        output = amp.run_program(phase_sequence[i])
        if _DEBUG:
            print(f'{i}: phase={phase_sequence[i]}-> output={output}')
        assert output.opcode == 3

    # Run the loop till completion
    loop_iter = 0
    while (True):
        for i, amp in enumerate(amps):
            output = amp.run_program(input)
            if _DEBUG:
                print(f'{loop_iter}, {i}: input={input} -> output={output}')
            input = output.output
        if output.opcode == 99:
            break
        loop_iter += 1
        if loop_iter > 10000:
            print('FAIL: reached max loop_iter')
            break
    return output

def find_optimal_setting(amp_program:str):
    # Go over all possible phase sequences while tracking max output
    max_output = -1
    max_phase = None
    options = list(itertools.permutations(list(range(5, 10))))

    for phase in options:
        amps = [Computer(program=amp_program, debug=_DEBUG) for _ in range(5)]
        output = compute_amp_serial_output(
            amps, phase)
        if output.output > max_output:
            max_output = output.output
            max_phase = phase
    
    return (max_phase, max_output)


# test_cases = [
#     # input program, expected phase setting sequence, expected max signal
#     ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], (4,3,2,1,0), 43210),
# 
#     # Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):
#     ([3,23,3,24,1002,24,10,24,1002,23,-1,23,
#     101,5,23,23,1,24,23,23,4,23,99,0,0], (0,1,2,3,4), 54321) ,
#     # Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):
#     ([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
#     1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], (1,0,4,3,2), 65210)
# ]

test_cases = [
    ([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], (9,8,7,6,5), 139629729),
    ([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], (9,7,8,5,6), 18216)
]

def run_tests(test_cases):
    for input_p, expected_phase, expected_max in test_cases:
        amps = [Computer(program=input_p, debug=_DEBUG) for _ in range(5)]
        first_max = compute_amp_serial_output(amps, expected_phase)
        if first_max.output != expected_max:
            print(f'FAIL: wrong compute_amp_serial. Found {first_max} and expected {expected_max}')
            return
        output_phase, output_max = find_optimal_setting(input_p)
        if output_phase != expected_phase:
            print(f'FAIL: wrong phase. Found {output_phase} and expected {expected_phase}')
        if output_max != expected_max:
           print(f'FAIL: wrong max. Found {output_max} and expected {expected_max}')
           return

run_tests(test_cases)

print(f"Optimal found: {find_optimal_setting(input_program)}")
