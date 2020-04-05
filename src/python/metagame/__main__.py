from metagame.simpleenemies import MetaGameFramework

if __name__ == "__main__":
    print("Running 'simpleenemies' game")
    game = MetaGameFramework.create_game()
    game.play()
