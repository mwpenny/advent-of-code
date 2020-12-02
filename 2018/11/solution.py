#!/usr/bin/python3

import sys

GRID_SERIAL_NUM = None  # Puzzle input
GRID_WIDTH = 300
GRID_HEIGHT = 300

with open('input', 'r') as f:
	GRID_SERIAL_NUM = int(f.read().strip())


def get_power_level(x, y):
	rack_id = x + 10
	power_level = ((rack_id * y) + GRID_SERIAL_NUM) * rack_id
	return ((power_level // 100) % 10) - 5

# Summed-area/partial sum table.
# areas[y][x] stores the sum of power levels in the rectangle from (0, 0) to (x, y)
areas = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
for y in range(1, GRID_HEIGHT):
	for x in range(1, GRID_WIDTH):
		areas[y][x] = get_power_level(x + 1, y + 1) + areas[y][x - 1] + areas[y - 1][x] - areas[y - 1][x - 1]

def square_power(x, y, square_size):
	x2 = x + square_size - 1
	y2 = y + square_size - 1
	return areas[y2][x2] - areas[y2][x - 1] - areas[y - 1][x2] + areas[y - 1][x - 1]

def highest_power_square(square_size):
	best_x = -1
	best_y = -1
	best_power = -sys.maxsize - 1
	for y in range(1, GRID_HEIGHT - square_size):
		for x in range(1, GRID_WIDTH - square_size):
			power = square_power(x, y, square_size)
			if power > best_power:
				best_x, best_y, best_power = x, y, power
	return best_x+1, best_y+1, best_power


# Part 1
print('Highest power 3x3 square: (x, y, power) = (%d, %d, %d)' % highest_power_square(3))

# Part 2
best_x = -1
best_y = -1
best_size = -1
best_power = -sys.maxsize - 1
for square_size in range(1, GRID_WIDTH):
	x, y, power = highest_power_square(square_size)
	if power > best_power:
		best_x, best_y, best_size, best_power = x, y, square_size, power
print('Highest power NxN square: (x, y, size, power) = (%d, %d, %d, %d)' % (best_x, best_y, best_size, best_power))