
def setup_game(game):
    # print("simpleplayer.py::setup_game")
    player = game.generate_instance_of("damageable")
    player["name"] = "Player"
    player["health"] = 10
