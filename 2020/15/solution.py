#!/usr/bin/python3

from collections import defaultdict

with open('input', 'r') as f:
	starting_nums = list(map(int, f.read().split(',')))
	seen_nums = defaultdict(int, { num: i+1 for i, num in enumerate(starting_nums) })
	num = starting_nums[-1]

	for i in range(len(starting_nums), 30000000):
		# Part 1
		if i == 2020:
			print('2020th number spoken:', num)

		last_i = seen_nums[num]
		seen_nums[num] = i
		num = 0 if last_i == 0 else i - last_i

	# Part 2
	print('30000000th number spoken:', num)