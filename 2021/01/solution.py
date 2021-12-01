#!/usr/bin/python3

def num_increases(measurements, window_size):
	return sum([
		1 for i, m in enumerate(measurements)
		if i >= window_size and m > measurements[i - window_size]
	])

with open('input', 'r') as f:
	measurements = [int(line) for line in f]

	# Part 1
	print('Number of 1-measurement increases', num_increases(measurements, 1))

	# Part 2
	print('Number of 3-measurement increases', num_increases(measurements, 3))
