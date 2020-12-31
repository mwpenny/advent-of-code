#!/usr/bin/python3

from collections import Counter
from math import prod
import re

ID_REGEX = re.compile(r'(\d+)')
SEAMONSTER_WIDTH = 20
SEAMONSTER_WATER_TILE_COUNT = 15

def find_seamonsters(tile):
	seamonster_count = 0
	for ofs in range(len(tile.rows[0]) - SEAMONSTER_WIDTH + 1):
		pattern_start_row = None
		row1_regex = re.compile(f'.{{{18 + ofs}}}#')
		row2_regex = re.compile(f'.{{{ofs}}}#{f".{{4}}##" * 3}#')
		row3_regex = re.compile(f'.{{{ofs}}}.{{1}}#{f".{{2}}#" * 5}')

		for i, row in enumerate(tile.rows):
			if pattern_start_row is not None:
				if i == pattern_start_row + 1 and not row2_regex.match(row):
					pattern_start_row = None
				elif i == pattern_start_row + 2:
					if row3_regex.match(row):
						seamonster_count += 1
					pattern_start_row = None

			if not pattern_start_row and row1_regex.match(row):
				pattern_start_row = i
	return seamonster_count

class Tile:
	def __init__(self, tid, rows):
		self.id = tid
		self.rows = rows
		self.link_top = self.link_bottom = self.link_left = self.link_right = None

	def top(self):
		return self.rows[0]

	def bottom(self):
		return self.rows[-1]

	def left(self):
		return ''.join(row[0] for row in self.rows)

	def right(self):
		return ''.join(row[-1] for row in self.rows)

	def inner(self):
		return [row[1:-1] for row in self.rows[1:-1]]

	def connected_tiles(self):
		return list(filter(bool, [
			self.link_top, self.link_bottom, self.link_left, self.link_right
		]))

	def try_connect(self, other):
		if not self.link_top and not other.link_bottom and self.top() == other.bottom():
			self.link_top = other
			other.link_bottom = self
		elif not self.link_bottom and not other.link_top and self.bottom() == other.top():
			self.link_bottom = other
			other.link_top = self
		elif not self.link_left and not other.link_right and self.left() == other.right():
			self.link_left = other
			other.link_right = self
		elif not self.link_right and not other.link_left and self.right() == other.left():
			self.link_right = other
			other.link_left = self
		else:
			return False
		return True

	def rol(self):
		self.rows = [
			''.join(row[i] for row in self.rows)
			for i in range(len(self.rows) -1, -1, -1)
		]

	def flip_x(self):
		self.rows = [row[::-1] for row in self.rows]

	def flip_y(self):
		self.rows = self.rows[::-1]

	def flip_xy(self):
		self.flip_x()
		self.flip_y()

	def reorient_until(self, pred):
		transformations = [lambda: None, self.flip_x, self.flip_y, self.flip_xy]
		for transformation in transformations:
			transformation()
			for _ in range(4):
				if pred(self):
					return
				self.rol()
			transformation()

	def tile_row(self):
		t = self
		while t:
			yield t
			t = t.link_right

	def tile_col(self):
		t = self
		while t:
			yield t
			t = t.link_bottom


with open('input', 'r') as f:
	tiles = [
		Tile(int(ID_REGEX.findall(tile_lines[0])[0]), tile_lines[1:])
		for tile_lines in (t.splitlines() for t in f.read().split('\n\n'))
	]

	tiles_to_examine = [tiles[0]]
	seen_tiles = set()

	while tiles_to_examine:
		tile = tiles_to_examine.pop()

		if tile.id not in seen_tiles:
			for tile2 in tiles:
				# If the second piece isn't connected to anything, try all possible
				# rotations and transformation. Otherwise, only try it as-is.
				if tile.id != tile2.id and not tile.try_connect(tile2) and not tile2.connected_tiles():
					tile2.reorient_until(lambda t: tile.try_connect(t))
			tiles_to_examine += tile.connected_tiles()
			seen_tiles.add(tile.id)

	# Part 1
	corners = [t.id for t in tiles if len(t.connected_tiles()) == 2]
	print('Product of corner IDs:', prod(corners))

	# Part 2
	image_rows = []
	top_left = next(t for t in tiles if not t.link_left and not t.link_top)
	for row_start in top_left.tile_col():
		row_tiles = [t.inner() for t in row_start.tile_row()]
		image_rows += list(''.join(cols) for cols in zip(*row_tiles))
	image = Tile(0, image_rows)

	image.reorient_until(lambda t: find_seamonsters(t) > 0)
	seamonster_water_tiles = find_seamonsters(image) * SEAMONSTER_WATER_TILE_COUNT
	roughness = Counter(''.join(image_rows))['#'] - seamonster_water_tiles
	print('Water roughness:', roughness)