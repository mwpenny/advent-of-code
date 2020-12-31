#!/usr/bin/python3

from collections import Counter

with open('input', 'r') as f:
	ing_counts = Counter()
	possible_bad_ings = dict()

	for line in f:
		split = line.split(' (contains ')
		ingredients, allergens = split[0].split(), split[1].strip()[:-1].split(', ')
		ing_counts.update(ingredients)

		for allergen in allergens:
			if allergen not in possible_bad_ings:
				possible_bad_ings[allergen] = set(ingredients)
			else:
				possible_bad_ings[allergen] &= set(ingredients)

	# Part 1
	safe_ings = set(ing_counts.keys()) - set().union(*possible_bad_ings.values())
	print('Safe ingredient occurrences:', sum(map(ing_counts.get, safe_ings)))

	# Part 2
	while True:
		ambiguous_ings = [i for i in possible_bad_ings.values() if len(i) > 1]
		if not ambiguous_ings:
			break

		definitive_ings = [i for i in possible_bad_ings.values() if len(i) == 1]
		for ingredients in ambiguous_ings:
			ingredients.difference_update(*definitive_ings)

	bad_ings = map(set.pop, (map(possible_bad_ings.get, sorted(possible_bad_ings.keys()))))
	print('Dangerous ingredients:', ','.join(bad_ings))