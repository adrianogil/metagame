from metagame.utils.numbers import is_integer


def run_iterate_action(action_parser, data, parent_args):
    iteration_target = data[0]

    if is_integer(iteration_target):
        iteration_target = int(iteration_target)
        for i in range(iteration_target):
            action_parser.run_actions(data[1], parent_args)
