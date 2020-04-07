
class ActionParser:
    def __init__(self):
        self.actionset = {}
        self.game = None

    def register_action(self, action_name, action):
        self.actionset[action_name] = action

    def run_action(self, action_name, data=None):
        print("[Debug] running action: " + action_name +
              " with data %s" % (data,))
        if action_name == "get_player_command_action":
            return input(">>")
        elif action_name == "print":
            print(str(data[0]))

    def run_actions(self, actions):
        for action in actions:
            self.run_action(action[0], action[1:])

    def run_player_action(self, player_action):
        player_cmds = player_action.split(" ")

        if player_cmds[0] == "help":
            for action in self.game["game"]["available_actions"]:
                print("- %s" % (action,))
