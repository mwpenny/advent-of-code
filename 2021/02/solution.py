#!/usr/bin/python3

with open('input', 'r') as f:
	pos = [0, 0, 0]

	for command in [line.strip().split(' ') for line in f]:
		direction = command[0]
		magnitude = int(command[1])

		if direction == 'forward':
			pos[0] += magnitude
			pos[1] += pos[2] * magnitude
		elif direction == 'up':
			pos[2] -= magnitude
		elif direction == 'down':
			pos[2] += magnitude

	# Part 1
	print('Movement 1 product:', pos[0] * pos[2])

	# Part 2
	print('Movement 2 product:', pos[0] * pos[1])
