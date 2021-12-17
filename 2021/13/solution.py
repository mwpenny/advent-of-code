#!/usr/bin/python3

def fold(points, x=None, y=None):
	new_points = set()
	for px, py in points:
		if x is not None and px > x:
			px = x - abs(px - x)
		elif y is not None and py > y:
			py = y - abs(py - y)
		new_points.add((px, py))
	return new_points

def print_points(points):
	max_x = max(x for x, _ in points)
	max_y = max(y for _, y in points)
	for y in range(max_y + 1):
		for x in range(max_x + 1):
			print('#' if (x, y) in points else '.', end='')
		print()


with open('input', 'r') as f:
	points, instructions = [s.split('\n') for s in f.read().strip().split('\n\n')]
	points = set(tuple(map(int, p.split(','))) for p in points)

	for i, instruction in enumerate(instructions):
		axis, num = instruction.split()[-1].split('=')
		points = fold(points, **{ axis: int(num) })

		# Part 1
		if i == 0:
			print('Points after first fold:', len(points))

	# Part 2
	print('Thermal camera code:')
	print_points(points)
