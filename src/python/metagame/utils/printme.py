
show_debug = False

target_buffer = {
    "game": None
}


def set_game_buffer(game_buffer):
    target_buffer["game"] = game_buffer


def printme(msg, debug=False):
    if not debug and target_buffer["game"]:
        target_buffer["game"].append(msg)

    if not debug or show_debug:
        print(msg)
