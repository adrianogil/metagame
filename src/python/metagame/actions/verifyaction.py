from metagame.utils.printme import printme


def run_verify_action(action_parser, data, parent_args):
    verify_result = True
    true_action = None
    false_action = None

    if data[0].__class__ == list:
        verify_result = action_parser.run_actions(data[0], parent_args)
        true_action = data[1]
        if len(data) > 2:  # Optional argument
            false_action = data[2]
    elif data[0] == "concept_exists":

        verify_result = False
        printme("verify - concept_exists? %s" % (data[1],), debug=True)
        if action_parser.get_concept(data[1], verify=True):
            verify_result = True
        true_action = data[2]
        if len(data) > 3:  # Optional argument
            false_action = data[3]
    elif data[0] == "equals":
        # print(str(data))
        if data[1].__class__ == list:
            data[1] = action_parser.run_actions(data[1], parent_args)
        if data[2].__class__ == list:
            data[2] = action_parser.run_actions(data[2], parent_args)
        verify_result = (data[1] == data[2])
        true_action = data[3]
        if len(data) > 4:  # Optional argument
            false_action = data[4]

    if verify_result:
        printme("verify - running true action", debug=True)
        return action_parser.run_actions(true_action, parent_args)
    else:
        printme("verify - running false action", debug=True)
        return action_parser.run_actions(false_action, parent_args)
