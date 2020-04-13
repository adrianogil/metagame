from metagame.utils.printme import printme
from .grammar import SimpleGrammar

from prompt_toolkit import PromptSession
import json
import sys


class ActionParser:
    def __init__(self):
        self.player_actions = {}
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
        printme("[Debug] running action: " + action_name +
                " with data %s" % (data,), debug=True)

        if data is not None:
            new_data = []
            for arg in data:
                if arg.__class__ == list:
                    arg = self.run_actions(arg)
                if arg.__class__ == str:
                    if arg.startswith("!arg"):
                        arg_number = int(arg[4:])
                        arg = parent_args[arg_number - 1]
                new_data.append(arg)
            data = new_data

        if action_name == "get_player_command_action":
            return self.session.prompt(">> ")
        elif action_name == "print":
            msg = data[0]

            if msg.__class__ == list:
                msg = self.run_action(msg[0], msg[1:])

            printme(str(msg))
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
        elif action_name == "grammar":
            grammar = SimpleGrammar()
            return grammar.parse(data[0])
        elif action_name in self.custom_actions:
            self.run_actions(self.custom_actions[action_name])

    def run_actions(self, actions, args=None):
        for action in actions:
            self.run_action(action[0], action[1:], args)

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
                if player_action.startswith(action):
                    self.run_actions(self.player_actions[action])
