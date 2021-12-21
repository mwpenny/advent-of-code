#!/usr/bin/python3

import heapq

ADJ_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def adj_points(x, y, width, height):
	for x_ofs, y_ofs in ADJ_OFFSETS:
		adj_x = x + x_ofs
		adj_y = y + y_ofs
		if 0 <= adj_x < width and 0 <= adj_y < height:
			yield adj_x, adj_y

def find_lowest_risk(risk_map, tile_count):
	tile_width, tile_height = len(risk_map[0]), len(risk_map)
	board_width, board_height = tile_width * tile_count, tile_height * tile_count

	to_explore = [(0, 0, 0)]
	heapq.heapify(to_explore)
	costs = dict()

	# Dijkstra's algorithm
	while to_explore:
		total_cost, x, y = heapq.heappop(to_explore)

		if (x, y) == (board_width - 1, board_height - 1):
			return total_cost

		for adj_x, adj_y in adj_points(x, y, board_width, board_height):
			risk = ((
				risk_map[adj_y % tile_height][adj_x % tile_width] +
				(adj_x // tile_width) + (adj_y // tile_height) - 1
			) % 9) + 1
			cost = total_cost + risk
			best_cost = costs.get((adj_x, adj_y), None)

			if best_cost is None or cost < best_cost:
				heapq.heappush(to_explore, (cost, adj_x, adj_y))
				costs[(adj_x, adj_y)] = cost


with open('input', 'r') as f:
	risk_map = [[*map(int, row)] for row in f.read().strip().split('\n')]

	# Part 1
	print('Lowest risk for 1-tile grid:', find_lowest_risk(risk_map, 1))

	# Part 2
	print('Lowest risk for 5-tile grid:', find_lowest_risk(risk_map, 5))
