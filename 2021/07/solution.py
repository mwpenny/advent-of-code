#!/usr/bin/python3

with open('input', 'r') as f:
	positions = sorted(list(map(int, f.read().split(','))))

	# Part 1
	median = positions[len(positions) // 2]
	print('Human cost estimate:', sum(abs(median - p) for p in positions))

	# Part 2
	m = max(positions)
	gauss_sum = lambda a, b: (abs(a - b) * (abs(a - b) + 1)) // 2
	costs = [sum(gauss_sum(target, p) for p in positions) for target in range(m)]
	print('Crab cost estimate:', min(costs))
