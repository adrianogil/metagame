
def setup_game(game):
    # print("simpleplayer.py::setup_game")
    player = game.generate_instance_of("damageable")
    player["name"] = "Player"
    player["health"] = 10

    slime_monster = game.generate_instance_of("enemy")
    slime_monster['name'] = "Slime"
    game.set_kgb("slime_monster", slime_monster)

    kobold_monster = game.generate_instance_of("enemy")
    kobold_monster['name'] = "Kobold"
    game.set_kgb("kobold_monster", kobold_monster)

    game.set_kgb("current_enemies", {
                 "concept_type": "enumeration",
                 "all": [game.generate_instance_of(m) for m in game.get_kgb_instances("enemy")]
                 })
