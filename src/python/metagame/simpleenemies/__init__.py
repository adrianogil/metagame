import metagame.framework
import metagame.simpleenemies.enemies as enemies


class MetaGameFramework(object):
    @staticmethod
    def create_game():
        game = metagame.framework.MetaGameFramework.create_game()
        enemies.setup_game(game)

        return game
