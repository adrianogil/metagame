from metagame.framework.metagame import MetaGame

if __name__ == "__main__":
    import sys
    print("Running game: %s" % (sys.argv[1:]))
    game = MetaGame()
    game.load_game(sys.argv[1:])
    game.play()
