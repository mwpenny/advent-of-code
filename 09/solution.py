#!/usr/bin/python3

from collections import defaultdict
import re

class Marble:
	def __init__(self, value):
		self.value = value
		self.left = self
		self.right = self

	def append_right(self, marble):
		marble.left = self
		marble.right = self.right
		self.right.left = marble
		self.right = marble

	def remove(self):
		self.right.left = self.left
		self.left.right = self.right


def get_max_score(player_count, marble_count):
	marbles = (Marble(i) for i in range(marble_count))
	player_scores = defaultdict(int)

	curr_marble = next(marbles)
	curr_player = 0
	for to_insert in marbles:
		if to_insert.value % 23 == 0:
			player_scores[curr_player] += to_insert.value
			to_remove = curr_marble.left.left.left.left.left.left.left  # To the left
			player_scores[curr_player] += to_remove.value
			curr_marble = to_remove.right
			to_remove.remove()
		else:
			curr_marble.right.append_right(to_insert)
			curr_marble = to_insert
		curr_player = (curr_player + 1) % player_count
	return max(player_scores.values())


MARBLE_REGEX = re.compile(r'(\d+).+?(\d+)')

with open('input', 'r') as f:
	player_count, last_marble_value = (int(x) for x in MARBLE_REGEX.match(f.read()).groups())

	# Part 1
	print(get_max_score(player_count, last_marble_value + 1))

	# Part 2
	print(get_max_score(player_count, (last_marble_value + 1)* 100))