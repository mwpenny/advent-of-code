#!/usr/bin/python3

from math import prod

ADJ_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def adj_points(heightmap, x, y):
	for x_ofs, y_ofs in ADJ_OFFSETS:
		adj_x = x + x_ofs
		adj_y = y + y_ofs
		if 0 <= adj_x < len(row) and 0 <= adj_y < len(heightmap):
			yield adj_x, adj_y


with open('input', 'r') as f:
	heightmap = [list(map(int, line.strip())) for line in f]

	# Part 1
	low_points = []
	for y, row in enumerate(heightmap):
		for x, p in enumerate(row):
			if all(p < heightmap[y][x] for x, y in adj_points(heightmap, x, y)):
				low_points.append((x, y))

	print('Total risk level:', sum(heightmap[y][x] + 1 for x, y in low_points))

	# Part 2
	basins = []
	for p in low_points:
		to_explore = [p]
		seen_points = set()

		while to_explore:
			p = to_explore.pop()
			seen_points.add(p)

			for adj_p in adj_points(heightmap, *p):
				adj_x, adj_y = adj_p
				if heightmap[adj_y][adj_x] < 9 and adj_p not in seen_points:
					to_explore.append(adj_p)
		basins.append(seen_points)

	basin_sizes = sorted(len(basin) for basin in basins)
	print('Product of size of 3 largest basins:', prod(basin_sizes[-3:]))
