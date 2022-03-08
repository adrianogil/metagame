

def describe_world(metagame):
    world_elements = metagame.get_concept('world/elements')

    main_world_description = [
        "Once upon a time, #world/location# ",
        'there was ' if len(world_elements) > 1 else 'there is '
    ]
    for index, element in enumerate(world_elements):
        main_world_description += ['#' + element['instance_name'] + '/short_description#']
        if index < (len(world_elements) - 1):
            if index == (len(world_elements) - 2):
                main_world_description += [' and ']
            else:
                main_world_description += [', ']
    metagame.print(main_world_description)


def describe_attack(metagame, event):
    metagame.print([
        ['grammar', {"text": ["And then"]}],
        ' ',
        "#" + event['attacker_instance_name'] + "/short_reference#",
        ' ',
        'destroyed' if event['intensity'] == 'destruction' else 'attacked',
        ' ',
        "#" + event['target_instance_name'] + "/short_reference#",
        '.'
    ])


def describe_event(metagame, event):
    if event['event_action'] == 'attack':
        describe_attack(metagame, event)

def describe_all_events(metagame):
    current_events = metagame.get_concept('world/events/timeline')
    if not current_events:
        # No events to be described
        return
    for event in current_events:
        describe_event(metagame, event)

def add_event(metagame, event):
    current_events = metagame.get_concept('world/events')
    if not current_events:
            current_events = {
                'timeline': []
            }
    current_events['timeline'] += [event]
    metagame.set_concept('world/events', current_events)


def generate_attack_action(metagame, attacker, target):
    def attack_action(data, parent_args):
        attack_event = {
            'event_action': 'attack',
            'attacker_instance_name': attacker,
            'target_instance_name': target,
            'intensity': 'destruction'
        }
        add_event(metagame, attack_event)

    return attack_action
