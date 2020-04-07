
show_debug = False

target_buffer = {
    "game": None
}


def set_game_buffer(game_buffer):
    target_buffer["game"] = game_buffer


def printme(msg, debug=False, only_history=False):
    if not debug and target_buffer["game"]:
        target_buffer["game"]["history"].append(msg)

    if not only_history and (not debug or show_debug):
        print(msg)
