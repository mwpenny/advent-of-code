#!/usr/bin/python3

from collections import defaultdict

with open('input', 'r') as f:
	points = defaultdict(int)
	points_non_diagonal = defaultdict(int)

	for start, end in [line.strip().split(' -> ') for line in f]:
		x1, y1 = map(int, start.split(','))
		x2, y2 = map(int, end.split(','))

		x_inc = -1 if x1 > x2 else 1
		y_inc = -1 if y1 > y2 else 1
		x, y = x1 - x_inc, y1 - y_inc
		while (x, y) != (x2, y2):
			x = x + x_inc if x != x2 else x
			y = y + y_inc if y != y2 else y

			points[x, y] += 1
			if x1 == x2 or y1 == y2:
				points_non_diagonal[x, y] += 1

	# Part 1
	overlaps = sum(1 for v in points_non_diagonal.values() if v > 1)
	print('Non-diagonal overlaps:', overlaps)

	# Part 2
	overlaps = sum(1 for v in points.values() if v > 1)
	print('All overlaps:', overlaps)
