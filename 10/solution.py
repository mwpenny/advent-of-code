#!/usr/bin/python3

from collections import defaultdict
import re
import sys


POINT_REGEX = re.compile(r'.+?(-?\d+),\s+(-?\d+).+?(-?\d+),\s+(-?\d+)')

class Point:
	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	def update(self):
		self.x += self.vx
		self.y += self.vy

points = []
with open('input', 'r') as f:
	points = [Point(*[int(x) for x in POINT_REGEX.match(line).groups()]) for line in f]

# Assumes the initial position will not contain the message
seconds = 0
likely_aligned = False
while not likely_aligned:
	filled_locations = defaultdict(bool)
	for p in points:
		p.update()
		filled_locations[(p.x, p.y)] = True

	# Heuristic: The points are probably aligned if all are beside at
	# least one other point (vertical, horizontal, or diagonal)
	likely_aligned = True
	for p in points:
		if not filled_locations[(p.x, p.y + 1)] and \
			not filled_locations[(p.x, p.y - 1)] and \
			not filled_locations[(p.x + 1, p.y)] and \
			not filled_locations[(p.x - 1, p.y)] and \
			not filled_locations[(p.x - 1, p.y - 1)] and \
			not filled_locations[(p.x - 1, p.y + 1)] and \
			not filled_locations[(p.x + 1, p.y - 1)] and \
			not filled_locations[(p.x + 1, p.y + 1)]:
			# A point is alone. Probably not aligned
			likely_aligned = False
			break
	seconds += 1

# Determine message bounds
min_x = min_y = sys.maxsize
max_x = max_y = -1
for p in points:
	min_x = min(p.x, min_x)
	min_y = min(p.y, min_y)
	max_x = max(p.x, max_x)
	max_y = max(p.y, max_y)

# Print (likely) message
for y in range(min_y, max_y + 1):
	for x in range(min_x, max_x + 1):
		print('#' if filled_locations[(x, y)] else '.'),
	print('')
print('Seconds to wait:', seconds)