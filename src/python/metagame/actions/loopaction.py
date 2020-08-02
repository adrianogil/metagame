

def run_foreach_action(action_parser, data, parent_args):
    current_concept = action_parser.game

    target_keywords = data[0].split("/")

    for keyword in target_keywords:
        if keyword not in current_concept:
            # Create a subconcept
            current_concept[keyword] = {}
        current_concept = current_concept[keyword]

    concept_list = current_concept.copy()

    for index, concept in enumerate(concept_list):
        action_parser.run_actions(data[1], [concept, index + 1])
