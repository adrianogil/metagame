from metagame.framework.grammar import SimpleGrammar

from basic_definition import describe_world, generate_attack_action, describe_all_events


def define_world(metagame):
    instance_name = 'castle'
    castle = {
        'name': 'castle',
        'instance_name': instance_name,
        'short_description': 'a castle',
        'short_reference': 'the castle'
    }
    metagame.set_concept('castle', castle)

    dragon = define_dragon(metagame)

    metagame.set_concept("world", {
        'location': 'in a far way reign',
        'elements': [castle, dragon]
    })

def define_dragon(metagame, dragon_name=''):
    
    if not dragon_name:
        dragon_name = SimpleGrammar.parse({'text': ['Dragus', 'Draco', 'Drogo']})

    dragon_mood = SimpleGrammar.parse({'mood': ['wrathful', 'peaceful', 'sleepy']}, target_tag='mood')
    
    instance_name = 'dragon'
    dragon_concept = {
        'name': dragon_name,
        'instance_name': instance_name,
        'short_description': 'a #dragon/mood# dragon',
        'short_reference': 'the dragon',
        'mood': dragon_mood,
        'wrathful_action': generate_attack_action(metagame, attacker='dragon', target='castle'),
        'peaceful_action': [
                ['print', 'And there is a peaceful dragon looking for flowers on mountains.']
            ],
        'sleepy_action': [
                ['print', 'And the dragon went back to sleep.']
            ]
    }

    metagame.set_concept(instance_name, dragon_concept)
    return dragon_concept


def setup_game(metagame):
    define_world(metagame)
    define_dragon(metagame)
    describe_world(metagame)
    metagame.run_action("dragon/#dragon/mood#_action")

    describe_all_events(metagame)

    metagame.run_action("exit")
