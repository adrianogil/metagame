from .metagame import MetaGame
from .commands import setup_game as commands_setup_game
from .simpleplayer import setup_game as simpleplayer_setup_game


class MetaGameFramework(object):
    def __init__(self):
        pass

    @staticmethod
    def create_game():
        game = MetaGame()

        commands_setup_game(game)
        simpleplayer_setup_game(game)

        return game
