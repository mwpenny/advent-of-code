#!/usr/bin/python3

from math import sin, cos, radians

# N, E, S, W
DIRECTION_VECTORS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# "It's not magic, it's linear algebra!"
def rotate_cw(x, y, angle):
	return (
		(x * cos(angle)) + (y * sin(angle)),
		(x * -sin(angle)) + (y * cos(angle))
	)

def rotate_ccw(x, y, angle):
	return (
		(x * cos(angle)) - (y * sin(angle)),
		(x * sin(angle)) + (y * cos(angle))
	)

def rotate(pos, origin, angle, rotation_func):
	rot_x, rot_y = rotation_func(pos[0], -pos[1], radians(angle))
	return (round(rot_x), -round(rot_y))

def add_vec(pos, vec, magnitude):
	return (pos[0] + (vec[0] * magnitude), pos[1] + (vec[1] * magnitude))

def move_direction(pos, command, magnitude):
	ofs_x, ofs_y = DIRECTION_VECTORS['NESW'.index(command)]
	return (pos[0] + (ofs_x * magnitude), pos[1] + (ofs_y * magnitude))


with open('input', 'r') as f:
	instructions = [(line[0], int(line[1:])) for line in f]

	# Part 1
	ship_pos = (0, 0)
	ship_dir = 1  # East
	for command, magnitude in instructions:
		if command in 'NESW':
			ship_pos = move_direction(ship_pos, command, magnitude)
		elif command == 'F':
			ship_pos = add_vec(ship_pos, DIRECTION_VECTORS[ship_dir], magnitude)
		elif command == 'L':
			ship_dir = (ship_dir - magnitude // 90) % len(DIRECTION_VECTORS)
		elif command == 'R':
			ship_dir = (ship_dir + magnitude // 90) % len(DIRECTION_VECTORS)
	print('Distance from start', abs(ship_pos[0]) + abs(ship_pos[1]))

	# Part 2
	ship_pos = (0, 0)
	waypoint_pos = (10, -1)
	for command, magnitude in instructions:
		if command in 'NESW':
			waypoint_pos = move_direction(waypoint_pos, command, magnitude)
		elif command == 'F':
			ship_pos = add_vec(ship_pos, waypoint_pos, magnitude)
		elif command == 'L':
			waypoint_pos = rotate(waypoint_pos, ship_pos, magnitude, rotate_ccw)
		elif command == 'R':
			waypoint_pos = rotate(waypoint_pos, ship_pos, magnitude, rotate_cw)
	print('Distance from start using waypoint', abs(ship_pos[0]) + abs(ship_pos[1]))