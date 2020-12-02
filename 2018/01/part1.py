#!/usr/bin/python3

freq = 0

with open('input', 'r') as f:
	for line in f:
		freq += int(line)

print(freq)
