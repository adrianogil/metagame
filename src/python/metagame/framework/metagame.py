from .actionparser import ActionParser

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

    def register_action(self, action_name, action):
        self.actionset[action_name] = action

    def register_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = {
                "subscribers": []
            }

    def get_kgb(self, kgb_concept):
        if kgb_concept not in self.knownledge_base:
            return None

        kgb_meaning = self.knownledge_base[kgb_concept]
        return kgb_meaning

    def set_kgb(self, kgb_concept, kgb_meaning):
        self.knownledge_base[kgb_concept] = kgb_meaning

        if 'instance' in kgb_meaning:
            for i in kgb_meaning['instance']:
                if i in self.knownledge_base_instances:
                    if kgb_concept not in self.knownledge_base_instances[i]:
                        self.knownledge_base_instances[i] = self.knownledge_base_instances[i] + [kgb_concept]
                else:
                    self.knownledge_base_instances[i] = [kgb_concept]

    def get_kgb_instances(self, kgb_instance):
        if kgb_instance not in self.knownledge_base_instances:
            return []

        return self.knownledge_base_instances[kgb_instance]

    def generate_instance_of(self, kgb_concept, new_concept=None):
        if new_concept is None:
            new_concept = {}

        kgb_meaning = self.get_kgb(kgb_concept)

        for props in kgb_meaning.keys():
            new_concept[props] = kgb_meaning[props]

        if 'instance' in new_concept:
            new_concept['instance'] = new_concept['instance'] + [kgb_concept]
        else:
            new_concept['instance'] = [kgb_concept]

        return new_concept

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
        self.knownledge_base[concept] = meaning

        if "event_subscriber" in meaning:
            event_data = meaning["event_subscriber"]
            for event in event_data:
                self.register_event_subscriber(event, concept)

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

    def setup_game(self):
        # entity
        self.set_kgb("entity", {
            "concept_type": "definition",
            "name": "entity"
        })

        # damageable
        def on_damage(self_data, event_data):
            self_data['health'] -= event_data['damage']
        self.register_action("on_damage_action", on_damage)

        damageable = self.generate_instance_of("entity")
        damageable['health'] = 1
        damageable['on_damage'] = "on_damage_action"
        self.set_kgb("damageable", damageable)

        # enemy
        enemy = self.generate_instance_of("damageable")
        self.set_kgb("enemy", enemy)

        self.set_kgb("current_enemies", {
                "concept_type": "enumeration",
                "all": [self.generate_instance_of(m) for m in self.get_kgb_instances("enemy")]
            })

    def play(self):
        self.propagate_event("on_game_started")

        while not self.knownledge_base["game"]["finished"]:
            player_cmd = self.action_parser.run_action("get_player_command_action")
            self.action_parser.run_player_action(player_cmd)


def main_game():
    game = MetaGame()
    game.play()


if __name__ == "__main__":
    main_game()
