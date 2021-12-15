#!/usr/bin/python3

FLASH_THRESHOLD = 9

def adj_points(energy_levels, x, y):
	for x_ofs in range(-1, 2):
		for y_ofs in range(-1, 2):
			adj_x = x + x_ofs
			adj_y = y + y_ofs

			if (adj_x, adj_y) != (x, y) and \
			   0 <= adj_x < len(energy_levels[0]) and \
			   0 <= adj_y < len(energy_levels):
				yield adj_x, adj_y

def inc_energy(energy_levels, x, y, flashed):
	energy_levels[y][x] += 1
	if energy_levels[y][x] > FLASH_THRESHOLD and (x, y) not in flashed:
		flashed.add((x, y))
		for x, y in adj_points(energy_levels, x, y):
			inc_energy(energy_levels, x, y, flashed)

def simulate(energy_levels):
	flashed = set()

	for y, row in enumerate(energy_levels):
		for x in range(len(row)):
			inc_energy(energy_levels, x, y, flashed)

	for x, y in flashed:
		energy_levels[y][x] = 0

	return len(flashed)


with open('input', 'r') as f:
	energy_levels = [list(map(int, line.strip())) for line in f]

	# Part 1
	flash_count = sum(simulate(energy_levels) for _ in range(100))
	print('Flash count after 100 steps:', flash_count)

	# Part 2
	step = 101
	while simulate(energy_levels) != len(energy_levels) * len(energy_levels[0]):
		step += 1
	print('Steps required for synchronization:', step)
