#!/usr/bin/python3

from collections import defaultdict, Counter
import copy

AREA_WIDTH = AREA_HEIGHT = 50
def starting_area():
	area = [['.' for y in range(AREA_WIDTH)] for x in range(AREA_HEIGHT)]
	with open('input', 'r') as f:
		for y, row in enumerate(f):
			for x, col in enumerate(row.strip()):
				area[y][x] = col
	return area

def adjacent_acres(x, y, area):
	acres = defaultdict(int)
	for x_ofs in range(-1, 2):
		for y_ofs in range(-1, 2):
			adj_x = x + x_ofs
			adj_y = y + y_ofs
			if (adj_x, adj_y) == (x, y) or \
				not 0 <= adj_x < AREA_WIDTH or not 0 <= adj_y < AREA_HEIGHT:
				continue
			acres[area[adj_y][adj_x]] += 1
	return acres

def life(area, mins=1):
	for minute in range(mins):
		new_area = copy.deepcopy(area)
		for y, row in enumerate(area):
			for x, col in enumerate(row):
				adj = adjacent_acres(x, y, area)
				if col == '.' and adj['|'] >= 3:
					new_area[y][x] = '|'
				elif col == '|' and adj['#'] >= 3:
					new_area[y][x] = '#'
				elif col == '#' and (adj['#'] == 0 or adj['|'] == 0):
					new_area[y][x] = '.'
		area = new_area
	return area

def area_counts(area):
	counts = Counter()
	for row in area:
		counts.update(row)
	return counts


# Part 1
area = life(starting_area(), 10)
counts = area_counts(area)
print('Num wooded * num lumber after 10 mins:', counts['|'] * counts['#'])

# Part 2
area = starting_area()
area_indexes = {}
products = []
minute = 1
while True:
	# Get cycle of unique products
	area = life(area)
	area_str = ''.join(''.join(row) for row in area)
	if area_str not in area_indexes:
		area_indexes[area_str] = minute

		counts = area_counts(area)
		products.append(counts['|'] * counts['#'])
	else:
		# Assume that once we hit a known board, the pattern has repeated
		cycle_start_idx = area_indexes[area_str]
		cycle_len = minute - cycle_start_idx
		cycle_elem_idx = (1000000000 - cycle_start_idx) % cycle_len
		print('Num wooded * num lumber after 1000000000 mins:', products[cycle_start_idx + cycle_elem_idx - 1])
		break
	minute += 1