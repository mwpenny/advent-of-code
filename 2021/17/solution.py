#!/usr/bin/python3

import re

AREA_REGEX = re.compile(r'.+x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')


with open('input', 'r') as f:
	left, right, bottom, top = map(int, AREA_REGEX.match(f.read().strip()).groups())

	# Part 1
	# Height will return to 0 after peaking, at which point y velocity will be
	# -start_y_vel - 1. Therefore, the optimal velocity is -bottom - 1 as it
	# results in hitting the bottom of the target area the first step after y=0.
	#
	# Since the y velocity decreases by 1 each step, the peak height is equal to
	# the sum over the starting y velocity to 1.
	print('Optimal height:', (bottom * (bottom + 1)) // 2)

	# Part 2
	# Try all possibilities until the first step in either direction overshoots
	vel_count = 0
	for initial_vel_x in range(right + 1):
		for initial_vel_y in range(bottom, -bottom):
			pos = (0, 0)
			vel = (initial_vel_x, initial_vel_y)
			while pos[0] <= right and pos[1] >= bottom:
				if left <= pos[0] <= right and bottom <= pos[1] <= top:
					vel_count += 1
					break
				pos = (pos[0] + vel[0], pos[1] + vel[1])
				vel = (max(0, vel[0] - 1), vel[1] - 1)
	print('Number of velocities resulting in target hit:', vel_count)
