#!/usr/bin/python3

from collections import Counter

def polymerize(template, rules, iterations):
	element_counts = Counter(template)
	element_pairs = Counter(''.join(p) for p in zip(template, template[1:]))

	for _ in range(iterations):
		new_pairs = Counter()
		for pair, count in element_pairs.items():
			to_insert = rules.get(pair)
			if to_insert is not None:
				element_counts[to_insert] += count
				new_pairs[f'{pair[0]}{to_insert}'] += count
				new_pairs[f'{to_insert}{pair[1]}'] += count
		element_pairs = new_pairs

	counts = element_counts.most_common()
	return counts[0][1] - counts[-1][1]


with open('input', 'r') as f:
	template, rules = f.read().strip().split('\n\n')
	rules = dict(rule.strip().split(' -> ') for rule in rules.split('\n'))

	# Part 1
	diff = polymerize(template, rules, 10)
	print('Most common minus least common after 10 insertions:', diff)

	# Part 2
	diff = polymerize(template, rules, 40)
	print('Most common minus least common after 40 insertions:', diff)
