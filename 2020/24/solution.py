#!/usr/bin/python3

from collections import defaultdict
import re

DIRECTION_REGEX = re.compile(r'e|se|sw|w|nw|ne')
DIRECTION_OFFSETS = {
	'e': (1, 0), 'se': (1, 1), 'sw': (0, 1),
	'w': (-1, 0), 'nw': (-1, -1), 'ne': (0, -1)
}

def tile_neighborhood(coords, tiles):
	return [coords] + [
		(coords[0] + ofs_x, coords[1] + ofs_y)
		for ofs_x, ofs_y in DIRECTION_OFFSETS.values()
	]

def game_of_life(tiles):
	new_tiles = tiles.copy()
	for coords in set().union(*(tile_neighborhood(c, tiles) for c in tiles)):
		is_black = tiles[coords]
		black_neighbors = sum(tiles[c] for c in tile_neighborhood(coords, tiles)) - is_black

		if is_black and not (1 <= black_neighbors <= 2):
			new_tiles[coords] = False
		elif not is_black and black_neighbors == 2:
			new_tiles[coords] = True
	return new_tiles

def black_tiles(tiles):
	return sum(tiles.values())


with open('input', 'r') as f:
	tiles = defaultdict(bool)

	for directions in f:
		directions = DIRECTION_REGEX.findall(directions)
		x, y = 0, 0
		for direction in directions:
			ofs_x, ofs_y = DIRECTION_OFFSETS[direction]
			x += ofs_x
			y += ofs_y
		tiles[(x, y)] = not tiles[(x, y)]

	# Part 1
	print('Black tiles after flipping:', black_tiles(tiles))

	# Part 2
	for _ in range(100):
		tiles = game_of_life(tiles)
	print('Black tiles after 100 days:', black_tiles(tiles))