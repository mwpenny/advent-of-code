#!/usr/bin/python3

import heapq
import re
import sys

INPUT_REGEX = re.compile(r'depth:\s(\d+)\ntarget:\s(\d+),(\d+)')

class Cave:
	EQ_NONE = 0
	EQ_TORCH = 1
	EQ_GEAR = 2

	def __init__(self, depth, tx, ty):
		self.erosion_levels = {}
		self.depth = depth
		self.tx = tx
		self.ty = ty
		self.distances = {(0, 0, self.EQ_TORCH): 0}  # Start

	def get_erosion_level(self, x, y):
		erosion_level = self.erosion_levels.get((x, y), None)
		if erosion_level is None:
			if (x, y) == (0, 0) or (x, y) == (self.tx, self.ty):
				geo_idx = 0
			elif x != 0 and y == 0:
				geo_idx = x * 16807
			elif x == 0:
				geo_idx = y * 48271
			else:
				geo_idx = self.get_erosion_level(x - 1, y) * \
					self.get_erosion_level(x, y - 1)
			erosion_level = (geo_idx + cave_depth) % 20183
			self.erosion_levels[(x, y)] = erosion_level
		return erosion_level

	def possible_moves(self, n):
		moves = []
		dist = self.distances[n]
		x, y, equip = n
		curr_region_type = self.get_erosion_level(x, y) % 3

		# Equipment swaps
		moves.extend([(dist + 7, x, y, e) for e in range(3) if e != curr_region_type])

		# Movement
		for (x_ofs, y_ofs) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			new_x, new_y = x + x_ofs, y + y_ofs
			if new_x >= 0 and new_y >= 0 and (self.get_erosion_level(new_x, new_y) % 3) != equip:
				moves.append((dist + 1, new_x, new_y, equip))
		return moves

	def find_target(self):
		start = (self.tx + self.ty, 0, 0, self.EQ_TORCH)
		fringe = [start]
		closed = set()

		# A*
		while fringe:
			_, x, y, equip = heapq.heappop(fringe)
			pos = (x, y, equip)
			closed.add(pos)

			if pos == (self.tx, self.ty, self.EQ_TORCH):
				return self.distances[pos]

			for move in self.possible_moves(pos):
				move_dist, move_x, move_y, move_equip = move
				m = (move_x, move_y, move_equip)

				if m in closed or move_dist >= self.distances.get(m, sys.maxsize):
					continue
				self.distances[(move_x, move_y, move_equip)] = move_dist
				f = move_dist + abs(move_x - tx) + abs(move_y + ty)
				heapq.heappush(fringe, (f, move_x, move_y, move_equip))


with open('input', 'r') as f:
	cave_depth, tx, ty = [int(x) for x in INPUT_REGEX.match(f.read().strip()).groups()]
	cave = Cave(cave_depth, tx, ty)

	# Part 1
	risk = 0
	for y in range(ty + 1):
		for x in range(tx + 1):
			risk += cave.get_erosion_level(x, y) % 3
	print('Risk:', risk)

	# Part 2
	print('Sortest path to target:', cave.find_target())