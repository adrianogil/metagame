import random


def add_indefinite_article(name):
	if name[0].lower() in ('a', 'e', 'i', 'o', 'u'):
		return "an " + name
	return "a " + name


def get_verb_inflection(verb, pronoun, time):
	if time == "present":
		if verb == "to be":
			inflection = {
				"I": ["'m", " am"],
				"you": ["'re", "are"],
				 "he": ["'s", "is"],
				 "she": ["'s", "is"],
				 "he": ["'s", "is"],
				 "it": ["'s", "is"],
			}
			return pronoun + inflection[pronoun][0]
	return ""


def get_adjective_from_attributes(object_concept):
	if "attributes" not in object_concept:
		return ""

	object_attributes = object_concept["attributes"]

	possible_adjective_gen = []

	if "size" in object_attributes:
		possible_adjective_gen.append(lambda x: x["size"] + " ")

	if "color" in object_attributes:
		possible_adjective_gen.append(lambda x: x["color"] + " ")		

	if len(possible_adjective_gen) == 0:
		return ""

	return random.choice(possible_adjective_gen)(object_attributes)


def describe_object(object_concept, description_method='categorically_concise'):
	# print(object_concept)
	category_name = object_concept.get("category_name", "")
	if description_method == "self_categorically_concise":
		pronoun = "I"
	else:
		pronoun = object_concept["pronouns"][0]
	return get_verb_inflection("to be", pronoun, "present") + " " + \
			add_indefinite_article(
				get_adjective_from_attributes(object_concept) + category_name) + "."


def define_world(metagame):
	dragon_category_concept = {
		"category_name": "dragon"
	}
	metagame.parse_concept("dragon", dragon_category_concept)
	smaug_dragon_concept = {
		"name": "Smaug",
		"instanceof": "dragon",
		"attributes": {
			"wings": {
				"color": "dark red"
			},
			"color": "black",
			"size": "colossal"
		},
		"pronouns": [
			"it", "its"
		]
	}
	metagame.parse_concept("Smaug_the_dragon", smaug_dragon_concept)

	knight_category_concept = {
		"category_name": "knight"
	}
	metagame.parse_concept("knight", knight_category_concept)
	scarlet_knight_concept = {
		"name": "Dora",
		"instanceof": "knight",
		"attributes": {
			"color": "blonde",
			"size": "meddium-sized"
		},
		"pronouns": [
			"She", "her"
		]
	}
	metagame.parse_concept("Dora_knight", scarlet_knight_concept)


def describe_world(metagame):
	description_sentence = describe_object(
		metagame.get_concept("Smaug_the_dragon"), 
		description_method="self_categorically_concise"
	)
	print(" - " + description_sentence)

	description_sentence = describe_object(
		metagame.get_concept("Dora_knight"), 
		description_method="self_categorically_concise"
	)
	print(" - " + description_sentence)

def setup_game(metagame):
	define_world(metagame)
	describe_world(metagame)
	metagame.run_action("exit")
