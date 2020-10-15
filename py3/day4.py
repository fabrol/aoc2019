print("Hello World")

"""
    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 138241-674034.
"""

from collections import Counter

def check_num(num:int):
    num_str = str(num)
    if len(num_str) != 6:
        return False
    
    max_so_far = num_str[0]
    for n in num_str:
        # Check non-decreasing
        if n < max_so_far:
            return False
        if n > max_so_far:
            max_so_far = n
            
            
            # 377778
            # len(num_str) - 1 -> 5
            # i   3
            # prev 7
            # curr 7
            # has_run_of_two = False
    ''' 
    has_run_of_two = False
    i = 0
    
    while (True):
        cur = num_str[i]
        
        k = 0
        while ((i+k) < len(num_str) and num_str[i+k] == cur) : k += 1
        
        if k == 2:
            has_run_of_two = True
            break
        
        i += k
        if i >= len(num_str):
            break
    '''
            
    # Check if the string has a run of two
    prev = num_str[0]
    has_run_of_two = False
    for i in range(1, len(num_str)):
        curr = num_str[i]
        if prev != curr:
            prev = curr
            continue
        if i == (len(num_str) - 1):
          if num_str[i-2] != curr:
            has_run_of_two = True
        elif i == 1 :
          if num_str[i+1] != curr:
            has_run_of_two = True
        else:
            if num_str[i+1] != curr and num_str[i-2] != curr:
                has_run_of_two = True
        prev = curr
   
    if not has_run_of_two:
        return False
            
    # c = Counter(num_str)
    # if c.most_common()[0][1] < 2:
    #     return False
    
    return True

def run(puzzle_input):
    low, high = puzzle_input.split("-")
    possible_values = set()
    print(low)
    print(high)
    for i in range(int(low), int(high) + 1):
        if check_num(i):
            possible_values.add(i)
    
    # print(list(possible_values)[:200])
    print(len(possible_values))
    return len(possible_values)

test_cases = [
 (111111, False),
 (223450, False), 
 (123789, False), 
 (12378, False), 
 (1237899, False), 
 (111,False),
 (1234321, False),
 (135579, True),
 (123444, False),
 (111122, True),
 (377778, False)
]    

def run_test():
    for t, expected in test_cases:
        actual = check_num(t)
        if actual != expected:
            print("ERROR: %s. Expected %s, Found %s" % (t, expected, actual))
   
run_test()

print('Final output')
input_value = '138241-674034'
run(input_value)
