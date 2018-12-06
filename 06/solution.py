#!/usr/bin/python3

import sys
from collections import defaultdict

def manhattan(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)

def closest_coord(coords, x, y):
	min_dist = sys.maxsize
	dist_to_all = 0
	closest_coord = None
	for coord in coords:
		dist = manhattan(x, y, coord[0], coord[1])
		if dist == min_dist:
			closest_coord = None
		elif dist < min_dist:
			min_dist = dist
			closest_coord = coord
		dist_to_all += dist
	return closest_coord, dist_to_all

def coord_in_range(bounding_box, coord):
	return bounding_box[0] < coord[0] < bounding_box[2] and \
		   bounding_box[1] < coord[1] < bounding_box[3]

coords = []
bounding_box = [sys.maxsize, sys.maxsize, -1, -1]

with open('input', 'r') as f:
	for line in f:
		coord =  tuple(int(c) for c in line.strip().split(', '))
		bounding_box[0] = min(bounding_box[0], coord[0])
		bounding_box[1] = min(bounding_box[1], coord[1])
		bounding_box[2] = max(bounding_box[2], coord[0])
		bounding_box[3] = max(bounding_box[3], coord[1])
		coords.append(coord)

coord_region_areas = defaultdict(int)  # For part 1
cluster_region_area = 0  # For part 2
for x in range(bounding_box[0], bounding_box[2] + 1):
	for y in range(bounding_box[1], bounding_box[3] + 1):
		c, dist_to_all = closest_coord(coords, x, y)
		if c is not None and coord_in_range(bounding_box, c):
			coord_region_areas[c] += 1
		if dist_to_all < 10000:
			cluster_region_area += 1

print('Largest area:', max(coord_region_areas.values()))
print('Cluster region area:', cluster_region_area)