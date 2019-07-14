
class MetaGame(object):

    def __init__(self):
        self.knownledge_base = {}
        self.knownledge_base_instances = {}
        self.actionset = {}

    def register_action(self, action_name, action):
        self.actionset[action_name] = action

    def run_action(self, action_name, data=None):
        return self.actionset[action_name](data)

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

    def setup_metagame(self):
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

        slime_monster = self.generate_instance_of("enemy")
        slime_monster['name'] = "Slime"
        self.set_kgb("slime_monster", slime_monster)

        kobold_monster = self.generate_instance_of("enemy")
        kobold_monster['name'] = "Kobold"
        self.set_kgb("kobold_monster", kobold_monster)

        self.set_kgb("current_enemies", {
                "concept_type": "enumeration",
                "all": [self.generate_instance_of(m) for m in self.get_kgb_instances("enemy")]
            })

    def play(self):
        self.setup_metagame()

        game_finished = False

        while not game_finished:
            user_cmd = self.run_action("get_user_command_action")
            data = {"command": user_cmd }
            self.run_action("process_user_command_action", data)


def main_game():
    game = MetaGame()
    game.play()


if __name__ == "__main__":
    main_game()
