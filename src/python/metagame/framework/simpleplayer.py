
def setup_game(game):
    player = game.generate_instance_of("damageable")
    player["name"] = "Player"
    player["health"] = 10
