
class ActionParser:
    def __init__(self):
        self.actionset = {}

    def register_action(self, action_name, action):
        self.actionset[action_name] = action

    def run_action(self, action_name, data=None):
        print("[Debug] running action: " + action_name +
              " with data %s" % (data,))

    def run_actions(self, actions):
        for action in actions:
            self.run_action(action[0], action[1:])
