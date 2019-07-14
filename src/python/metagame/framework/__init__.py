from metagame.framework.metagame import MetaGame
import metagame.framework.commands as commands


class MetaGameFramework(object):
    def __init__(self):
        pass

    @staticmethod
    def create_game():
        game = MetaGame()

        commands.setup_game(game)

        return game
