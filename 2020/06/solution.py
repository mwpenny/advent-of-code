#!/usr/bin/python3

with open('input', 'r') as f:
	groups = f.read().strip().split('\n\n')

	unique_group_answer_count = 0
	unanimous_group_answer_count = 0
	for group in groups:
		answers = [*map(set, group.split())]
		unique_group_answer_count += len(set.union(*answers))
		unanimous_group_answer_count += len(set.intersection(*answers))

	# Part 1
	print('Total unique group answers:', unique_group_answer_count)

	# Part 2
	print('Total unanimous group answers:', unanimous_group_answer_count)