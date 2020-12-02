#!/usr/bin/python3

import re

NANOBOT_REGEX = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>,\sr=(\d+)')

nanobots = []
with open('input', 'r') as f:
	for line in f:
		nanobots.append([int(x) for x in NANOBOT_REGEX.match(line).groups()])

def dist(n1, n2):
	# Manhattan distance
	return sum(abs(n1[i] - n2[i]) for i in range(3))

# Part 1
strongest = max(nanobots, key=lambda k: k[3])
in_range = filter(lambda n: dist(strongest, n) <= strongest[3], nanobots)
print('Bots in range of strongest:', len(list(in_range)))

# Part 2
# Group nanobots that are in range of each other
intersecting_nanobots = [nanobots[:1]]
for n1 in nanobots[1:]:
	found_intersection = False
	for intersecting_group in intersecting_nanobots:
		if all(dist(n1, n2) <= n1[3] + n2[3] for n2 in intersecting_group):
			intersecting_group.append(n1)
			found_intersection = True
	if not found_intersection:
		intersecting_nanobots.append([n1])

# For the largest group of bots, find the distance of
# the closest point of the farthest bot's range
largest_group = max(intersecting_nanobots, key=len)
point_dist = max([dist(k, (0,0,0)) - k[3] + 1 for k in largest_group])
print('Shortest distance to most bots:', point_dist)