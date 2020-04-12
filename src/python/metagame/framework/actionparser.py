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

    def run_action(self, action_name, data=None):
        printme("[Debug] running action: " + action_name +
                " with data %s" % (data,), debug=True)
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
        elif action_name == "set_concept":
            target_keywords = data[0].split("/")
            target_value = data[1]

            current_concept = self.game

            for keyword in target_keywords[:-1]:
                current_concept = current_concept[keyword]
            current_concept[target_keywords[-1]] = target_value
        elif action_name == "grammar":
            grammar = SimpleGrammar()
            return grammar.parse(data[0])
        elif action_name in self.custom_actions:
            self.run_actions(self.custom_actions[action_name])

    def run_actions(self, actions):
        for action in actions:
            self.run_action(action[0], action[1:])

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
