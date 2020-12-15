#!/usr/bin/python3

from copy import deepcopy

SEAT_OFFSETS = [
	(0, -1), (0, 1), (-1, 0), (1, 0),
	(-1, -1), (-1, 1), (1, -1), (1, 1)
]

def get_seat_state(seats, x, y):
	return seats[y][x] if 0 <= x < len(seats[0]) and 0 <= y < len(seats) else None

def dir_has_occupied_seat(seats, x, y, vec):
	while True:
		x += vec[0]
		y += vec[1]
		seen_seat_state = get_seat_state(seats, x, y)

		if seen_seat_state is None or seen_seat_state == 'L':
			return False
		elif seen_seat_state == '#':
			return True

def count_adj_occupied_seats(seats, x, y):
	return len([
		1 for ofs_x, ofs_y in SEAT_OFFSETS
		if get_seat_state(seats, x + ofs_x, y + ofs_y) == '#'
	])

def count_seen_occupied_seats(seats, x, y):
	return len([1 for ofs in SEAT_OFFSETS if dir_has_occupied_seat(seats, x, y, ofs)])

def count_occupied_seats(seats):
	return len([seat_state for row in seats for seat_state in row if seat_state == '#'])

def game_of_life(seats, seat_counter, seat_count_threshold):
	while True:
		next_generation = deepcopy(seats)

		for y, row in enumerate(seats):
			for x, seat_state in enumerate(row):
				if seat_state != '.':
					count = seat_counter(seats, x, y)

					if seat_state == 'L' and count == 0:
						next_generation[y][x] = '#'
					elif seat_state == '#' and count >= seat_count_threshold:
						next_generation[y][x] = 'L'

		if seats == next_generation:
			return count_occupied_seats(seats)
		seats = next_generation


with open('input', 'r') as f:
	seats = [list(line) for line in f.read().split()]

	# Part 1
	occupied_seat_count = game_of_life(seats, count_adj_occupied_seats, 4)
	print('Occupied seats after first settling:', occupied_seat_count)

	# Part 2
	occupied_seat_count = game_of_life(seats, count_seen_occupied_seats, 5)
	print('Occupied seats after second settling:', occupied_seat_count)