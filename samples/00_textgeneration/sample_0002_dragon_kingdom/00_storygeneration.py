



def describe_world(metagame):
    metagame.print(["Once upon a time, in a far way reign there was a castle and a ", ["get_concept", "dragon/mood"], " dragon."])


def setup_game(metagame):
    metagame.set_concept("dragon", 
    {
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
    describe_world(metagame)
    metagame.run_action("dragon/#dragon/mood#_action")

