

def describe_action(object_concept, description_method='categorically_concise'):
	# print(object_concept)
	if description_method == 'categorically_concise':
		return "It's a " + object_concept['category_name'] + "."

def define_world(metagame):
	dragon_category_concept = {
		"category_name": "dragon"
	}
	metagame.parse_concept("dragon", dragon_category_concept)
	smaug_dragon_concept = {
		"concept_type": "instance",
		"name": "Smaug",
		"instanceof": "dragon"
	}
	metagame.parse_concept("Smaug_the_dragon", smaug_dragon_concept)


def describe_world(metagame):
	description = describe_action(metagame.get_concept("Smaug_the_dragon"))
	print(description)

def setup_game(metagame):
	define_world(metagame)
	describe_world(metagame)
	metagame.run_action("exit")
