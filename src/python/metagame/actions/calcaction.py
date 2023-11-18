from math import *
import re


def run_calc_action(action_parser, data, parent_args):
    # Step 1: Extract the calculation string
    calc_string = data[0]

    # Step 2: Identify variables
    variables = re.findall(r'#(.*?)#', calc_string)

    # Step 3: Replace variables with their values
    for var in variables:
        print(var)
        value = action_parser.get_concept(var)
        print(value)
        calc_string = calc_string.replace(f'#{var}#', str(value))

    # Step 4: Evaluate the calculation string
    result = eval(calc_string)

    return result
    