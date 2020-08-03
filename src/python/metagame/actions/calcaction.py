from metagame.utils.numbers import is_integer


def run_calc_action(action_parser, data, parent_args):
    calc_string = data[0]

    current_number = [0, 0]

    calc_data = {
        "register": 0,
        "inside_number": False,
        "operation": None
    }

    operations = ['+', '-', '*', '/']

    def update_operation():
        if calc_data["register"] == 1:
            if calc_data["operation"] == "+":
                current_number[0] = current_number[0] + current_number[1]
            elif calc_data["operation"] == "-":
                current_number[0] = current_number[0] - current_number[1]
            elif calc_data["operation"] == "*":
                current_number[0] = current_number[0] * current_number[1]
            elif calc_data["operation"] == "/":
                current_number[0] = current_number[0] / current_number[1]

            calc_data["operation"] = None
            calc_data["register"] = 0
        else:
            calc_data["register"] = 1
        calc_data["inside_number"] = False

    for s in calc_string:
        if s == ' ':
            calc_data["inside_number"] = False
            update_operation()
            continue

        if is_integer(s):
            if not calc_data["inside_number"]:
                current_number[calc_data["register"]] = int(s)
                calc_data["inside_number"] = True
            else:
                current_number[calc_data["register"]] = current_number[calc_data["register"]] * 10 + int(s)
        else:
            update_operation()

            if s in operations:
                calc_data["operation"] = s
    update_operation()

    return current_number[0]
