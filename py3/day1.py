input_text = [106001,
131342,
51187,
87791,
68636,
109091,
111888,
98012,
90713,
54284,
143884,
121856,
117199,
77883,
132628,
123828,
56939,
50447,
77110,
103272,
148181,
59323,
98249,
110065,
144277,
108204,
92138,
54449,
108098,
119292,
65720,
136053,
116987,
78305,
143302,
145067,
106633,
90519,
58970,
57090,
77334,
55929,
95983,
139236,
62634,
89275,
113296,
59530,
114159,
98407,
120607,
84394,
91151,
135965,
56157,
114073,
95274,
75259,
60582,
136361,
54771,
53286,
70491,
131915,
114306,
120749,
117462,
86194,
112412,
140705,
72377,
113646,
145304,
60811,
127560,
78769,
99205,
127236,
136099,
69166,
141727,
115973,
100845,
90494,
62209,
85841,
116591,
78406,
140341,
139849,
55119,
64092,
58439,
52273,
51742,
57258,
95120,
138764,
106361,
82104 ,]

"""
Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

    For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
    For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
    For a mass of 1969, the fuel required is 654.
    For a mass of 100756, the fuel required is 33583.

The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your spacecraft?
"""

test_examples = [
    (14, 2),
    (1969, 966),
    (100756, 50346),
    ]
    
test_examples_list = [
    ([12,1969], 968)
    ]
    
def get_fuel(mass):
    return int(mass / 3) - 2
    

def get_total_fuel(mass_list):
  result = 0
  for mass in mass_list:
      while(mass > 0):
          mass = max(get_fuel(mass), 0)
          result += mass
  return result

for mass, fuel in test_examples:
    tf = get_total_fuel([mass])
    assert fuel == tf, 'fuel=%s, tf=%s' % (fuel, tf)
    
for masses, fuel in test_examples_list:
    assert fuel == get_total_fuel(masses)
    
print('done testing')


print(get_total_fuel(input_text))






