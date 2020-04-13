from metagame.utils.printme import printme
from .actionparser import ActionParser

import metagame.utils.printme as printmodule
import json


class MetaGame(object):
    def __init__(self):
        self.knownledge_base = {}
        self.knownledge_base_instances = {}
        self.events = {}
        self.action_parser = ActionParser()
        self.action_parser.game = self.knownledge_base

        self.knownledge_base["game"] = {
            "finished": False,
            "available_actions": [
                "help"
            ]
        }

    def register_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = {
                "subscribers": []
            }

    def propagate_event(self, event_name):
        if event_name in self.events:
            for subscriber in self.events[event_name]["subscribers"]:
                if subscriber in self.knownledge_base:
                    subscriber_concept = self.knownledge_base[subscriber]
                    if 'event_subscriber' in subscriber_concept:
                        if event_name in subscriber_concept["event_subscriber"]:
                            event_response = subscriber_concept["event_subscriber"][event_name]
                            if 'actions' in event_response:
                                self.action_parser.run_actions(event_response["actions"])

    def register_event_subscriber(self, event, concept):
        if event in self.events:
            self.events[event]["subscribers"].append(concept)
        else:
            self.events[event] = {
                "subscribers": [concept]
            }

    def parse_concept(self, concept, meaning):
        printme("MetaGame:parse_concept - " + concept, debug=True)

        if "event_subscriber" in meaning:
            event_data = meaning["event_subscriber"]
            for event in event_data:
                self.register_event_subscriber(event, concept)
        if "concept_type" in meaning:
            if meaning["concept_type"] == "action":
                self.action_parser.add_custom_action(
                    concept,
                    meaning["actions"])
            elif meaning["concept_type"] == "player_action":
                self.action_parser.add_player_action(
                    meaning["action_name"],
                    meaning["actions"])
            elif meaning["concept_type"] == "instance":
                parent_meaning = meaning["instanceof"]
                new_meaning = self.knownledge_base[parent_meaning]
                for subconcept in meaning:
                    new_meaning[subconcept] = meaning[subconcept]
                new_meaning["concept_type"] = "definition"
                meaning = new_meaning
        self.knownledge_base[concept] = meaning

    def load_game_data(self, game_file_data):
        with open(game_file_data, 'r') as f:
            game_data = json.load(f)

            for game_concept in game_data:
                self.parse_concept(game_concept, game_data[game_concept])

    def load_game(self, game_files):
        if game_files.__class__ == list:
            for game_file in game_files:
                self.load_game_data(game_file)
        else:
            self.load_game_data(game_files)

    def play(self):
        if "history" in self.knownledge_base["game"]:
            for history_log in self.knownledge_base["game"]["history"]:
                print(history_log)
        else:
            self.knownledge_base["game"]["history"] = []
            printmodule.set_game_buffer(self.knownledge_base["game"])
            printme("=" * 8 + " Starting game " + "=" * 8 + "\n\n")
            self.propagate_event("on_game_started")

        while not self.knownledge_base["game"]["finished"]:
            player_cmd = self.action_parser.run_action("get_player_command_action")
            printme(">> %s" % (player_cmd,), only_history=True)
            self.action_parser.run_player_action(player_cmd)


def main_game():
    game = MetaGame()
    game.play()


if __name__ == "__main__":
    main_game()
