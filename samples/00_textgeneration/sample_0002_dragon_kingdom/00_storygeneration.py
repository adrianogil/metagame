from metagame.framework.grammar import SimpleGrammar


def define_dragon(metagame, dragon_name=''):
    
    if not dragon_name:
        dragon_name = SimpleGrammar.parse({'text': ['Dragus', 'Draco', 'Drogo']})
    
    metagame.set_concept("dragon", 
    {
        "name": dragon_name,
        "mood": ["grammar", {
                     "text": ["#mood#"],
                     "mood": ["wrathful", "peaceful", "sleepy"]
                    }
                ],
        "wrathful_action": [
                ["print", "And then the dragon destroyed the castle."]
            ],
        "peaceful_action": [
                ["print", "And there is a peaceful dragon looking for flowers on mountains."]
            ],
        "sleepy_action": [
                ["print", "And the dragon went back to sleep."]
            ]
    })


def describe_world(metagame):
    main_world_description = [
        "Once upon a time, in a far way reign there was a castle and a ", 
        ["get_concept", "dragon/mood"],
        " dragon named #dragon/name#"
    ]
    metagame.print(main_world_description)


def setup_game(metagame):
    define_dragon(metagame, dragon_name='Dragus')
    describe_world(metagame)
    metagame.run_action("dragon/#dragon/mood#_action")
    metagame.run_action("exit")
