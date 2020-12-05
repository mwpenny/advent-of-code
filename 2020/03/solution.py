#!/usr/bin/python3

from math import prod

def count_trees(terrain, slope_x, slope_y):
	tree_count = 0

	x = slope_x
	for line in terrain[slope_y::slope_y]:
		if line[x % len(line)] == '#':
			tree_count += 1
		x += slope_x
	return tree_count


with open('input', 'r') as f:
	terrain = [line.strip() for line in f.readlines()]

	# Part 1
	print('Tree count for slope (3, 1):', count_trees(terrain, 3, 1))

	# Part 2
	slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
	product = prod(count_trees(terrain, x, y) for x, y in slopes)
	print('Product of tree counts for all slopes:', product)