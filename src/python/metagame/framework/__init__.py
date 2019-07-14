from metagame.framework.metagame import MetaGame
import metagame.framework.commands as commands
import metagame.framework.simpleplayer as simpleplayer


class MetaGameFramework(object):
    def __init__(self):
        pass

    @staticmethod
    def create_game():
        game = MetaGame()

        commands.setup_game(game)
        simpleplayer.setup_game(game)

        return game
