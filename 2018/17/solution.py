#!/usr/bin/python3

import re
import sys

COORD_REGEX = re.compile(r'[x|y]=(\d+),\s[x|y]=(.+)')
WATER_SOURCE = (500, 0)

clay = set()
active_water = set([WATER_SOURCE])
settled_water = set()
plateaus = []
curr_water = [WATER_SOURCE]

with open('input', 'r') as f:
	for line in f:
		m = COORD_REGEX.match(line.strip()).groups()
		coords = int(m[0]), [int(c) for c in m[1].split('..')]
		x_first = line[0] == 'x'
		if x_first:
			x = coords[0]
		else:
			y = coords[0]

		for c in range(coords[1][0], coords[1][1] + 1):
			if x_first:
				clay.add((x, c))
			else:
				clay.add((c, y))

min_y = sys.maxsize
max_y = -sys.maxsize - 1
for (x, y) in clay:
	min_y = min(min_y, y)
	max_y = max(max_y, y)


def is_empty(coord):
	return coord not in clay and coord not in active_water and coord not in settled_water

def move_possible(coord):
	x, y = coord
	return is_empty((x - 1 , y)) or is_empty((x + 1 , y))


while curr_water:
	w = curr_water.pop()
	x, y = w
	down = (x, y + 1)
	left = (x - 1 , y)
	right = (x + 1, y)

	active_water.add(w)

	if down[1] <= max_y and is_empty(down):
		curr_water.append(w)
		curr_water.append(down)
		plateaus.append(set([down]))
	elif down in clay or down in settled_water:
		moves = []
		if is_empty(left):
			plateaus[-1].add(left)
			moves.append(left)
		if is_empty(right):
			plateaus[-1].add(right)
			moves.append(right)

		if not moves:
			if all(not move_possible(coord) for coord in plateaus[-1]):
				active_water.difference_update(plateaus[-1])
				settled_water.update(plateaus[-1])
				curr_water = [coord for coord in curr_water if coord not in plateaus[-1]]
				plateaus.pop()
		else:
			curr_water.append(w)
			curr_water.extend(moves)

active_water = set(w for w in active_water if min_y <= w[1] <= max_y)
print('Total water:', len(active_water.union(settled_water)))
print('Settled water:', len(settled_water))