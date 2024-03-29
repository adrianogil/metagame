from metagame.utils.printme import printme
from metagame.actions.actionparser import ActionParser

import metagame.utils.printme as printmodule
import json
import copy
import os


class MetaGame(object):
    """
    The MetaGame class represents the game engine that runs the game. It loads game data from files,
    parses the data, and runs the game loop.

    Attributes:
        knownledge_base (dict): The knowledge base of the game engine.
        knownledge_base_instances (dict): The instances of the knowledge base.
        action_parser (ActionParser): The action parser that handles game actions.
    """

    def __init__(self):
        """
        Initializes a new instance of the MetaGame class.
        """
        self.knownledge_base = {}
        self.knownledge_base_instances = {}
        self.action_parser = ActionParser()
        self.action_parser.game = self.knownledge_base

        self.knownledge_base["game"] = {
            "finished": False,
            "available_actions": [
                "help"
            ]
        }

    def parse_concept(self, concept, meaning):
        """
        Parses a concept and its meaning, and updates the knowledge base accordingly.

        Args:
            concept (str): The concept to be parsed.
            meaning (dict): The meaning of the concept.
        """
        printme("MetaGame:parse_concept - " + concept, debug=True)

        if "event_subscriber" in meaning:
            event_data = meaning["event_subscriber"]
            for event in event_data:
                self.action_parser.register_event_subscriber(event, concept)

        if "concept_type" in meaning:
            if meaning["concept_type"] == "action":
                # Register new general action (used by the game)
                self.action_parser.add_custom_action(concept, meaning["actions"])
            elif meaning["concept_type"] == "player_action":
                # Register new player action (used by the player)
                if meaning["action_name"].__class__ == list:
                    for player_action in meaning["action_name"]:
                        self.action_parser.add_player_action(
                            player_action,
                            meaning["actions"])
                else:
                    self.action_parser.add_player_action(
                        meaning["action_name"],
                        meaning["actions"])
            elif meaning["concept_type"] == "instance":
                parent_meaning = meaning["instanceof"]
                new_meaning = copy.deepcopy(self.knownledge_base[parent_meaning])
                for subconcept in meaning:
                    new_meaning[subconcept] = meaning[subconcept]
                new_meaning["concept_type"] = "definition"
                meaning = new_meaning
        elif meaning.__class__ == dict:
            if 'instanceof' in meaning:
                parent_meaning = meaning["instanceof"]
                new_meaning = copy.deepcopy(self.knownledge_base[parent_meaning])
                for subconcept in meaning:
                    new_meaning[subconcept] = meaning[subconcept]
                new_meaning["concept_type"] = "definition"
                meaning = new_meaning
            else:
                meaning["concept_type"] = "definition"
        self.knownledge_base[concept] = meaning

    def load_game_data(self, game_file_data):
        """
        Loads game data from a file.

        Args:
            game_file_data (str): The path to the game file.
        """
        printme('[python.metagame.framework.metagame] MetaGame:load_game_data -' + ' game_file_data - ' + str(game_file_data), debug=True)
        if '.pyc' in game_file_data:
            return
        if game_file_data.endswith('.py'):
            import importlib.util
            spec = importlib.util.spec_from_file_location("module.name", game_file_data)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            foo.setup_game(self)
        else:
            self.load_game_data_json(game_file_data)

    def load_game_data_json(self, game_file_data):
        """
        Loads game data from a JSON file.

        Args:
            game_file_data (str): The path to the JSON file.
        """
        with open(game_file_data, 'r') as f:
            game_data = json.load(f)

            for game_concept in game_data:
                self.parse_concept(game_concept, game_data[game_concept])

    def load_game(self, game_files):
        """
        Loads game data from one or more files.

        Args:
            game_files (str or list): The path to the game file(s).
        """
        printme("MetaGame:load_game - " + str(game_files), debug=True)
        if game_files.__class__ == list:
            for game_file in game_files:
                self.load_game(game_file)
        elif os.path.isdir(game_files):
            self.load_game(list(map(lambda x: os.path.join(game_files, x), sorted(os.listdir(game_files)))))
        else:
            self.load_game_data(game_files)

    def play(self):
        """
        Runs the game loop.
        """
        if "history" in self.knownledge_base["game"]:
            for history_log in self.knownledge_base["game"]["history"]:
                print(history_log)
        else:
            self.knownledge_base["game"]["history"] = []
            printmodule.set_game_buffer(self.knownledge_base["game"])
            printme("=" * 8 + " Starting game " + "=" * 8 + "\n\n", debug=True)
            self.action_parser.propagate_event("on_game_started")

        while not self.knownledge_base["game"]["finished"]:
            player_cmd = self.action_parser.run_action("get_player_command_action")
            printme(">> %s" % (player_cmd,), only_history=True)
            self.action_parser.run_player_action(player_cmd)

    def set_concept(self, concept, data):
        """
        Sets the value of a concept in the knowledge base.

        Args:
            concept (str): The concept to be set.
            data (any): The value to be set.
        """
        self.action_parser.run_action("set_concept", [concept, data])

    def get_concept(self, concept):
        """
        Gets the value of a concept from the knowledge base.

        Args:
            concept (str): The concept to be retrieved.

        Returns:
            any: The value of the concept.
        """
        return self.action_parser.get_concept(concept)

    def print(self, data):
        """
        Prints data to the console.

        Args:
            data (any): The data to be printed.
        """
        self.action_parser.run_action("print", data)

    def run_action(self, action_name, data=None):
        """
        Runs a game action.

        Args:
            action_name (str): The name of the action to be run.
            data (list, optional): The data to be passed to the action. Defaults to None.
        """
        if not data:
            data = []
        self.action_parser.run_action(action_name, data)


def main_game():
    game = MetaGame()
    game.play()


if __name__ == "__main__":
    main_game()
