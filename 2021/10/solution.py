#!/usr/bin/python3

from functools import reduce

CLOSING_CHARS = { '(': ')', '[': ']', '{': '}', '<': '>' }
ILLEGAL_CHAR_POINTS = { ')': 3, ']': 57, '}': 1197, '>': 25137 }
COMPLETION_CHAR_POINTS = { ')': 1, ']': 2, '}': 3, '>': 4 }

def parse_line(line):
	stack = []
	for c in line:
		if stack and c == CLOSING_CHARS[stack[-1]]:
			stack.pop()
		elif c in CLOSING_CHARS.values():
			return c, []  # Incorrect closing character
		else:
			stack.append(c)
	return None, [CLOSING_CHARS[c] for c in reversed(stack)]


with open('input', 'r') as f:
	error_score = 0
	completion_scores = []

	for line in f:
		invalid_char, completion_chars = parse_line(line.strip())
		if invalid_char:
			error_score += ILLEGAL_CHAR_POINTS[invalid_char]
		else:
			char_scores = map(COMPLETION_CHAR_POINTS.get, completion_chars)
			completion_scores.append(reduce(lambda a, b: (a * 5) + b, char_scores))

	# Part 1
	print('Syntax error score:', error_score)

	# Part 2
	middle_cmp_score = sorted(completion_scores)[len(completion_scores)//2]
	print('Middle completion score:', middle_cmp_score)
