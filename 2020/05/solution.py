#!/usr/bin/python3

with open('input', 'r') as f:
	seen_ids = set()
	for line in f.readlines():
		id_binary = line.strip() \
			.replace('F', '0').replace('L', '0') \
			.replace('B', '1').replace('R', '1')
		seen_ids.add(int(id_binary, 2))

	# Part 1
	print('Max ID:', max(seen_ids))

	# Part 2
	all_ids = set(range(min(seen_ids), max(seen_ids) + 1))
	print('Missing ID:', all_ids.difference(seen_ids).pop())