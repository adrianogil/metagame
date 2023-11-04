from metagame.framework.metagame import MetaGame

import metagame.utils.printme as printmemodule

if __name__ == "__main__":
    import sys
    
    game = MetaGame()
    
    if '-v' in sys.argv[1:]:
        print("Running game: %s" % (sys.argv[1:]))
        printmemodule.show_debug = True
    
    game.load_game([f for f in sys.argv[1:] if not f.startswith("-")])
    game.play()
