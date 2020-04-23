from metagame.utils.printme import printme
from .grammar import SimpleGrammar

from prompt_toolkit import PromptSession

import metagame.utils.printme

import json
import sys


class ActionParser:
    def __init__(self):
        self.player_actions = {
            "debug": [
                ["toggle_debug"]
            ]
        }
        self.custom_actions = {}
        self.game = None
        self.session = PromptSession()

    def add_custom_action(self, action_name, actions):
        printme("ActionParser:add_player_action - action_name: " + action_name, debug=True)
        self.custom_actions[action_name] = actions

    def add_player_action(self, action_name, actions):
        printme("ActionParser:add_player_action - action_name: " + action_name, debug=True)
        self.player_actions[action_name] = actions

    def run_action(self, action_name, data=None, parent_args=None):
        printme("running action: %s with data %s and parent args: %s" %
                (action_name, data, parent_args), debug=True)

        if data is not None:
            new_data = []
            for arg in data:
                if (action_name != "verify" and
                   action_name != "for_each_concept") and arg.__class__ == list:
                    arg = self.run_actions(arg, parent_args)
                if arg.__class__ == str:
                    if parent_args.__class__ == dict:
                        for key in parent_args:
                            arg = arg.replace("#" + key + "#", parent_args[key])
                    elif parent_args.__class__ == list:
                        for index, arg_value in enumerate(parent_args):
                            printme("attempt to replace %s in %s with data %s " %
                                    ("#arg" + str(index + 1) + "#", arg, arg_value), debug=True)
                            arg = arg.replace("#arg" + str(index + 1) + "#", arg_value)
                printme("final arg: %s" % (arg,), debug=True)
                new_data.append(arg)
            data = new_data

        if action_name == "get_player_command_action":
            return self.session.prompt(">> ")
        elif action_name == "print":
            print_msg = ""

            for print_arg in data:
                msg = print_arg
                if msg.__class__ == list:
                    msg = self.run_action(msg[0], msg[1:], parent_args)
                print_msg += str(msg)

            printme(print_msg)
        elif action_name == "exit":
            sys.exit()
        elif action_name == "save":
            with open(data[0], 'w') as f:
                json.dump(self.game, f)
        elif action_name == "get_concept":
            target_keywords = data[0].split("/")
            current_concept = self.game

            for keyword in target_keywords:
                current_concept = current_concept[keyword]

            printme("Returns concept %s" % (current_concept,), debug=True)

            return current_concept

        elif action_name == "set_concept":
            target_keywords = data[0].split("/")
            target_value = data[1]
            if len(data) > 2:
                # concept meaning will be a list
                target_value = data[1:]

            current_concept = self.game

            for keyword in target_keywords[:-1]:
                if keyword not in current_concept:
                    # Create a subconcept
                    current_concept[keyword] = {}
                current_concept = current_concept[keyword]

            current_concept[target_keywords[-1]] = target_value
        elif action_name == "remove_concept":
            target_keywords = data[0].split("/")

            current_concept = self.game

            for keyword in target_keywords[:-1]:
                if keyword not in current_concept:
                    # Create a subconcept
                    current_concept[keyword] = {}
                current_concept = current_concept[keyword]

            if current_concept.__class__ == list:
                current_concept.remove(target_keywords[-1])
            else:
                current_concept.pop(target_keywords[-1])
        elif action_name == "grammar":
            grammar = SimpleGrammar()

            target_grammar = data[0]
            if target_grammar.__class__ == list:
                target_grammar = target_grammar[0]
            printme("loading grammar: %s" % (target_grammar,), debug=True)

            text = grammar.parse(target_grammar)

            printme("grammar generated text: %s" % (text,), debug=True)

            return text
        elif action_name == "verify":
            verify_result = True

            true_action = None
            false_action = None

            if data[0].__class__ == list:
                verify_result = self.run_actions(data[0], parent_args)
                true_action = data[1]
                if len(data) > 2:  # Optional argument
                    false_action = data[2]
            elif data[0] == "concept_exists":
                current_concept = self.game

                target_keywords = data[1].split("/")

                for keyword in target_keywords[:-1]:
                    if keyword not in current_concept:
                        # Create a subconcept
                        current_concept[keyword] = {}
                    current_concept = current_concept[keyword]

                verify_result = target_keywords[-1] in current_concept
                true_action = data[2]
                if len(data) > 3:  # Optional argument
                    false_action = data[3]

            if verify_result:
                printme("verify - running true action", debug=True)
                return self.run_actions(true_action, parent_args)
            else:
                printme("verify - running false action", debug=True)
                return self.run_actions(false_action, parent_args)
        elif action_name == "for_each_concept":
            current_concept = self.game

            target_keywords = data[0].split("/")

            for keyword in target_keywords:
                if keyword not in current_concept:
                    # Create a subconcept
                    current_concept[keyword] = {}
                current_concept = current_concept[keyword]

            concept_list = current_concept.copy()

            for concept in concept_list:
                self.run_actions(data[1], [concept])
        elif action_name == "run":
            return self.run_actions(data[0], parent_args)
        elif action_name == "return":
            return data[0]
        elif action_name in self.custom_actions:
            self.run_actions(self.custom_actions[action_name], data)
        elif action_name == "toggle_debug":
            metagame.utils.printme.show_debug = not metagame.utils.printme.show_debug

    def run_actions(self, actions, args=None):
        if actions is None:
            return

        if len(actions) > 0 and actions[0].__class__ == list:
            for action in actions[:-1]:
                self.run_action(action[0], action[1:], args)
            return self.run_action(actions[-1][0], actions[-1][1:], args)
        else:
            return self.run_action(actions[0], actions[1:], args)

    def actions_matches(self, player_action, registered_action):
        words_player_action = player_action.split(" ")
        words_registered_action = registered_action.split(" ")

        if len(words_registered_action) != len(words_player_action):
            return False

        for action, register in zip(words_player_action, words_registered_action):
            printme("actions_matches: %s - %s" % (action, register), debug=True)
            if action != register and not register.isupper():
                printme("actions_matches: %s - %s - return False" % (action, register), debug=True)
                return False


        printme("actions_matches: %s - %s - return True" % (player_action, registered_action), debug=True)
        return True

    def parse_actions_args(self, player_action, registered_action):
        words_player_action = player_action.strip().split(" ")
        words_registered_action = registered_action.strip().split(" ")

        dict_arg = {}

        for action, register in zip(words_player_action, words_registered_action):
            if register.isupper():
                dict_arg[register] = action

        return dict_arg

    def run_player_action(self, player_action):
        # player_cmds = player_action.split(" ")

        # action_name = player_cmds[0]

        if player_action == "help":
            printme("The following commands are available:")
            for action in self.game["game"]["available_actions"]:
                printme("- %s" % (action,))
            for action in self.player_actions:
                printme("- %s" % (action,))
        else:
            for action in self.player_actions:
                if self.actions_matches(player_action, action):
                    self.run_actions(self.player_actions[action],
                                     self.parse_actions_args(player_action, action))
