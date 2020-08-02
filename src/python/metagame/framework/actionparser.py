from metagame.utils.printme import printme
from .grammar import SimpleGrammar

from prompt_toolkit import PromptSession
from random import randint

import metagame.utils.printme

import json
import sys
import ast


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


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
        self.events = {}
        self.global_vars = {}

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
                    for global_var in self.global_vars:
                        arg = arg.replace("#" + str(global_var) + "#", self.global_vars[global_var])
                    if parent_args.__class__ == dict:
                        for key in parent_args:
                            arg = arg.replace("#" + key + "#", parent_args[key])
                    elif parent_args.__class__ == list:
                        for index, arg_value in enumerate(parent_args):
                            arg_index = "#arg" + str(index + 1) + "#"
                            printme("attempt to replace %s in %s with data %s " %
                                    (arg_index, arg, arg_value), debug=True)
                            if arg == arg_index:
                                arg = arg_value
                                break
                            else:
                                arg = arg.replace(arg_index, str(arg_value))
                    elif "#" in arg:
                        arg = self.parse_concept_inside_string(arg)
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
            current_concept = self.get_concept(data[0])

            printme("Returns concept %s" % (current_concept,), debug=True)

            return current_concept
        elif action_name == "get_concept_list":
            current_concept_list = self.get_concept(data[0])

            if current_concept_list.__class__ == dict:
                current_concept_list = list(current_concept_list.keys())

            printme("Returns concept list %s" % (current_concept_list,), debug=True)

            return current_concept_list
        elif action_name == "set_concept":
            self.set_concept(data[0], data[1:])
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

                verify_result = False
                printme("verify - concept_exists? %s" % (data[1],), debug=True)
                if self.get_concept(data[1], verify=True):
                    verify_result = True
                true_action = data[2]
                if len(data) > 3:  # Optional argument
                    false_action = data[3]
            elif data[0] == "equals":
                # print(str(data))
                if data[1].__class__ == list:
                    data[1] = self.run_actions(data[1], parent_args)
                if data[2].__class__ == list:
                    data[2] = self.run_actions(data[2], parent_args)
                verify_result = (data[1] == data[2])
                true_action = data[3]
                if len(data) > 4:  # Optional argument
                    false_action = data[4]

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

            for index, concept in enumerate(concept_list):
                self.run_actions(data[1], [concept, index + 1])
        elif action_name == "run":
            target_actions = data[0]
            if target_actions.__class__ == str:
                target_actions = ast.literal_eval(target_actions)
            return self.run_actions(target_actions, parent_args)
        elif action_name == "return":
            return data[0]
        elif action_name == "instantiate":
            target_concept = self.get_concept(data[0])
            store_concept = data[1]

            new_concept_name = data[0].split("/")[-1] + ("instance_%4d" % (randint(0, 9999),))
            new_concept = store_concept + "/" + new_concept_name

            self.global_vars["LAST_INSTANTIATE_ENTITY"] = new_concept

            self.set_concept(new_concept, target_concept)

        elif action_name in self.custom_actions:
            self.run_actions(self.custom_actions[action_name], data)
        elif action_name == "toggle_debug":
            metagame.utils.printme.show_debug = not metagame.utils.printme.show_debug
        else:
            return str([action_name] + data)

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
        words_player_action = player_action.strip().split(" ")
        words_registered_action = registered_action.strip().split(" ")

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

    def parse_concept_inside_string(self, arg):
        target_concepts = []

        current_concept = ""
        inside_concept = False

        for s in arg:
            if not inside_concept:
                if current_concept == "" and s == '#':
                    inside_concept = True
            else:
                if s == '#':
                    target_concepts.append(current_concept)
                    current_concept = ""
                    inside_concept = False
                else:
                    current_concept += s

        for concept in target_concepts:
            arg = arg.replace("#" + concept + "#", self.get_concept(concept))

        return arg

    def set_concept(self, concept_name, concept_value):
        target_keywords = concept_name.split("/")
        target_value = concept_value
        if concept_value.__class__ == list:
            if len(concept_value) > 2:
                # concept meaning will be a list
                target_value = concept_value[1:]
            else:
                target_value = concept_value[0]
        else:
            target_value = concept_value

        current_concept = self.game

        for keyword in target_keywords[:-1]:
            if keyword not in current_concept:
                # Create a subconcept
                current_concept[keyword] = {}
            current_concept = current_concept[keyword]

        current_concept[target_keywords[-1]] = target_value

    def get_concept(self, concept_name, verify=False):
        target_keywords = concept_name.split("/")
        current_concept = self.game

        if verify:
            last_concept = target_keywords[-1]
            target_keywords = target_keywords[:-1]

        try:
            for keyword in target_keywords:
                if is_integer(keyword):
                    keynumber = int(keyword) - 1
                    if current_concept.__class__ == list:
                        current_concept = current_concept[keynumber]
                    else:
                        keys_list = list(current_concept.keys())
                        current_concept = current_concept[keys_list[keynumber]]
                else:
                    current_concept = current_concept[keyword]
        except:
            return False

        if verify:
            return last_concept in current_concept

        return current_concept

    def register_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = {
                "subscribers": []
            }

    def propagate_event(self, event_name):
        if event_name in self.events:
            for subscriber in self.events[event_name]["subscribers"]:
                if subscriber in self.game:
                    subscriber_concept = self.game[subscriber]
                    if 'event_subscriber' in subscriber_concept:
                        if event_name in subscriber_concept["event_subscriber"]:
                            event_response = subscriber_concept["event_subscriber"][event_name]
                            if 'actions' in event_response:
                                self.run_actions(event_response["actions"])

    def register_event_subscriber(self, event, concept):
        if event in self.events:
            self.events[event]["subscribers"].append(concept)
        else:
            self.events[event] = {
                "subscribers": [concept]
            }
