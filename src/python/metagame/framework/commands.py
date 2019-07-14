import json


def setup_game(game):
    def get_command(data):
        user_command = input(">> ")
        return user_command

    def process_command(data):
        command = data["command"]
        if command is None:
            print("Can't understand your action!")

        command_name = command.split(" ")[0] + "_command"
        all_commands = game.get_kgb("available_commands")["all"]

        if command_name not in all_commands:
            print("Command is not available")
            return

        command = game.get_kgb(command_name)

        if command is None:
            print("Can't understand your action!")
        else:
            game.run_action(command['action'], data)
    game.register_action("get_user_command_action", get_command)
    game.register_action("process_user_command_action", process_command)

    game.set_kgb("command", {
            "concept_type": "definition"
        })

    ###### Look ######
    def look_command_action(data):
        current_enemies = game.get_kgb("current_enemies")['all']

        print("You can see: ")
        if len(current_enemies) > 0:
            for e in current_enemies:
                print(" - %s" % (e['name'],))
        else:
            print("- Nothing at all")
    game.register_action("look_command_action", look_command_action)

    look_command = game.generate_instance_of("command")
    look_command['action'] = "look_command_action"
    game.set_kgb("look_command", look_command)

    ###### Save ######
    def save_command_action(data):
        command = data["command"]
        target_file = command.split(" ")[1]
        with open(target_file, 'w') as f:
            json.dump(game.knownledge_base, f)
    game.register_action("save_command_action", save_command_action)
    save_command = game.generate_instance_of("command")
    save_command['action'] = "save_command_action"
    game.set_kgb("save_command", save_command)

    ###### Load ######
    def load_command_action(data):
        command = data["command"]
        target_file = command.split(" ")[1]
        with open(target_file, 'r') as f:
            knownledge_base = json.load(f)
        game.knownledge_base = knownledge_base
        print("Loaded new knownledge base")
    game.register_action("load_command_action", load_command_action)

    load_command = game.generate_instance_of("command")
    load_command["action"] = "load_command_action"
    game.set_kgb("load_command", load_command)

    ###### Quit ######
    def quit_command_action(data):
        exit()
    game.register_action("quit_command_action", quit_command_action)

    quit_command = game.generate_instance_of("command")
    quit_command['action'] = "quit_command_action"
    game.set_kgb("quit_command", quit_command)


    ###### Help ######
    def help_command_action(data):
        all_commands = game.get_kgb("available_commands")["all"]
        all_commands_str = " ".join([c[:-8] for c in all_commands])

        print("You can use the following commands:")
        print("\t" + all_commands_str)
    game.register_action("help_command_action", help_command_action)

    help_command = game.generate_instance_of("command")
    help_command['action'] = "help_command_action"
    game.set_kgb("help_command", help_command)

    game.set_kgb("available_commands", {
                "concept_type": "enumeration",
                "all": ["look_command", "load_command", "save_command", "help_command", "quit_command"]
            })
