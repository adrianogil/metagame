from metagame.utils.printme import printme


def _search_for_concept(concept_root, concept_condition):
    result = None

    for prop in concept_root:
        printme("searching_for_concept in property %s" % (prop,), debug=True)
        prop_value = concept_root[prop]
        if prop_value.__class__ == dict:
            if concept_condition(prop_value):
                return prop_value
            else:
                result = _search_for_concept(prop_value, concept_condition)
                if result is not None:
                    return result
    return result


def run_search_for_concept_action(action_parser, data, parent_args):
    # Update references on action arguments

    data = data[0].copy()

    for key in data:
        data[key] = action_parser.parse_contextual_arg(data[key], "search_for_concept", parent_args)

    printme("searching_for_concept using args %s" % (data,), debug=True)

    concept_root = action_parser.get_concept(data["root"])

    def concept_condition(concept):
        condition_result = None
        condition_value = None

        if concept.__class__ in [list, dict]:
            if 'has_property' in data:
                target_property = data['has_property']
                if target_property in concept:
                    target_value = concept[target_property]

                    if 'property_value_contains' in data:
                        if data['property_value_contains'].__class__ == str and target_value.__class__ == str:
                            condition_value = data['property_value_contains'].lower() in target_value.lower()
                        else:
                            condition_value = data['property_value_contains'] in target_value

                if condition_result is None:
                    condition_result = condition_value
                else:
                    condition_result = condition_value and condition_result

        return condition_result

    concept_found = _search_for_concept(concept_root, concept_condition)

    return concept_found
