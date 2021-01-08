import numpy as np

DEBUG=False
def create_matrix(n):
    m = np.ndarray((n,n))
    base_pattern = [0,1,0,-1]

    for idx in range(1,n+1):
        row = []
        row_base = []
        for el in base_pattern:
            row_base.extend([el]*idx)
        while len(row) < n+1:
            row.extend(row_base)
        row = row[1:n+1]
        assert len(row) == n
        m[idx-1] = row

    if DEBUG:
        print (f"Created matrix: \n {m}")

    return m

def create_matrix_b(n, final_index, num_entries):
    m = np.ndarray((num_entries,n))
    base_pattern = [0,1,0,-1]

    m_idx = 0
    for idx in range(final_index, final_index+num_entries):
        row = []
        row_base = []
        for el in base_pattern:
            row_base.extend([el]*idx)
        while len(row) < n+1:
            row.extend(row_base)
        row = row[1:n+1]
        assert len(row) == n
        m[m_idx] = row
        m_idx += 1

    if DEBUG:
        print (f"Created matrix: \n {m}")

    return m

def run_phase(input_list, op_matrix):
    input_vec = np.asarray(input_list)
    try:
        output_vec = np.matmul(op_matrix, input_vec)
    except Exception as e:
        print(f'halp {e}')

    # keep only the "ones" (remove negatives too)
    output = np.mod(np.abs(output_vec), 10)
    return output


"""
Here are the first eight digits of the final output list after 100 phases for some larger inputs:

    80871224585914546619083218645595 becomes 24176176.
    19617804207202209144916044189917 becomes 73745418.
    69317163492948606335995924319873 becomes 52432133.

input: 12345678 
1: 48226158
2: 34040438
3: 03415518
4: 01029498
"""

def run_parta(input_str, num_phases=100):
    curr_seq = [int(i) for i in input_str]
    m = create_matrix(len(input_str))
    for i in range(num_phases):
        print(f'Executing phase {i}')
        next_seq = run_phase(curr_seq, m)
        curr_seq = next_seq
    # do stuff
    return curr_seq[:8]

def run_partb(input_str, num_phases=100):
    curr_seq = [int(i) for i in input_str]
    curr_seq = [*curr_seq]*10000

    # calculate the index to go
    final_index = int(input_str[:7])
    # want to generate 8 * len(curr_seq) matrix
    # represent rows final_index to final_index + 7
    m = create_matrix_b(len(curr_seq), final_index=final_index, num_entries=8)
    for i in range(num_phases):
        print(f'Executing phase {i}')
        next_seq = run_phase(curr_seq, m)
        curr_seq = next_seq
    # do stuff
    return curr_seq[:8]

def test_parta():
    # run the first 4 steps of the phase calc
    input0 = [1,2,3,4,5,6,7,8]
    answers = [
        [4,8,2,2,6,1,5,8],
        [3,4,0,4,0,4,3,8],
        [0,3,4,1,5,5,1,8],
        [0,1,0,2,9,4,9,8],
    ]
    matrix = create_matrix(len(input0))
    for i in range(4):
        input0 = run_phase(input0, matrix)
        as_list = list(input0)
        expected = answers[i]
        assert as_list == expected, f"FAIL: Expected {expected} but found {input0}"

    test_case_list = [
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ]
    for input_str, ans_prefix in test_case_list:
        output = run_parta(input_str, num_phases=100)
        output_prefix = np.asarray(output[:8])
        ans_prefix_as_arr = np.asarray(list(ans_prefix), dtype=int)
        ans_prefix_as_int = [int(x) for x in ans_prefix]
        output_ints = [int(x) for x in output[:8]]
        assert output_ints == ans_prefix_as_int, f"FAIL: Expected {ans_prefix} but found {output_prefix}"
        # print (output_prefix, type(output_prefix), len(output_prefix))
        # print (ans_prefix_as_arr, type(ans_prefix_as_arr), len(ans_prefix_as_arr))
        # assert output_prefix.all(ans_prefix_as_arr), f"FAIL: Expected {ans_prefix} but found {output_prefix}"

def test_partb():
    test_case_list = [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ]
    for input_str, ans_prefix in test_case_list:
        output = run_partb(input_str=input_str, num_phases=100)
        ans_prefix_as_int = [int(x) for x in ans_prefix]
        output_ints = [int(x) for x in output[:8]]
        assert output_ints == ans_prefix_as_int, f"Expected {ans_prefix} but found {output_ints}"

#test_parta()

def read_input(filename='day16.in'):
    with open(filename, 'r') as f:
        contents = f.read().strip()
        return contents

#print(run_parta(read_input(), num_phases=100))

test_partb()
#run_partb(read_input(), num_phases=100)
    
# 2020-11-11 part b answer
# The bottom half of the matrix multiplication from
# part (a) is functionally a running sum:
#
#       ...           ..      ...
#  ... 0 0 1 1 1 1     w      w + x + y + z   
#  ... 0 0 0 1 1 1  *  x  =   x + y + z
#  ... 0 0 0 0 1 1     y      y + z
#  ... 0 0 0 0 0 1     z      z
#
# Conveniently, we only care about indexes
# 5970837 to 5970837 + 7
# There are 650*10k rows in the matrix. 
#
# So the solution is then to:
# For each phase,
#   ignore most of the matrix
#   calculate the running sum
#   keep the ones digit

def run_partb2(input_str, num_phases):
    # repeat the input_str 10k times
    curr_seq = [int(i) for i in input_str]
    curr_seq = [*curr_seq]*10000
    index = int(''.join(str(x) for x in input_str[:7]))
    vec = curr_seq[index:]
    print(f'index: {index}')
    print(f'vec: {len(vec)} {len(input_str)} {len(input_str) * 10000}')
    print(vec[:20])
    next_vec = [0]*len(vec)
    for _ in range(num_phases):
        running_sum = 0  
        for j in range(len(vec) - 1, -1, -1):
            running_sum += vec[j]
            next_vec[j] = running_sum
        for j in range(len(next_vec)):
            next_vec[j] = next_vec[j] % 10
        vec = next_vec
    return ''.join(str(x) for x in vec[:8])


pinput = '59708372326282850478374632294363143285591907230244898069506559289353324363446827480040836943068215774680673708005813752468017892971245448103168634442773462686566173338029941559688604621181240586891859988614902179556407022792661948523370366667688937217081165148397649462617248164167011250975576380324668693910824497627133242485090976104918375531998433324622853428842410855024093891994449937031688743195134239353469076295752542683739823044981442437538627404276327027998857400463920633633578266795454389967583600019852126383407785643022367809199144154166725123539386550399024919155708875622641704428963905767166129198009532884347151391845112189952083025'
print(run_partb2(pinput, num_phases=100))