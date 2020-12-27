#!/usr/bin/python3

from collections import defaultdict

def active_cubes(coords, cubes):
	return len([c for c in coords if cubes[c]])

def get_neighborhood(coord, dimensions, i=0):
	if i == dimensions:
		return {coord}
	return set.union(*[
		get_neighborhood((coord[:i] + (coord[i] + ofs,) + coord[i+1:]), dimensions, i+1)
		for ofs in range(-1, 2)
	])

def game_of_life(cubes, dimensions):
	for _ in range(6):
		next_generation = cubes.copy()

		for coord in set().union(*(get_neighborhood(coord, dimensions) for coord in cubes)):
			neighbors = get_neighborhood(coord, dimensions).difference({coord})
			active_neighbors = active_cubes(neighbors, cubes)

			if cubes[coord] and active_neighbors not in (2, 3):
				next_generation[coord] = False
			elif not cubes[coord] and active_neighbors == 3:
				next_generation[coord] = True

		cubes = next_generation

	return active_cubes(cubes, cubes)


with open('input', 'r') as f:
	cubes_3d = defaultdict(bool)
	cubes_4d = defaultdict(bool)
	for y, row in enumerate(f.readlines()):
		for x, col in enumerate(row.strip()):
			cubes_3d[(x, y, 0)] = cubes_4d[(x, y, 0, 0)] = col == '#'

	# Part 1
	print('Active cubes after 3D initialization:', game_of_life(cubes_3d, 3))

	# Part 2
	print('Active cubes after 4D initialization:', game_of_life(cubes_4d, 4))