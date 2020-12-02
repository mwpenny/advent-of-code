#!/usr/bin/python3

import string

def react_polymer(polymer):
	stack = []
	for c in polymer:
		if len(stack) > 0 and c != stack[-1] and c.lower() == stack[-1].lower():
			stack.pop()
		else:
			stack.append(c)
	return len(stack)

def remove_unit_type(polymer, c):
	return ''.join(x for x in polymer if x.lower() != c)

with open('input', 'r') as f:
	polymer = f.read().strip()  # Newline = off by one error >:(

	# Part 1
	print(react_polymer(polymer))

	# Part 2
	print(min(react_polymer(remove_unit_type(polymer, c)) for c in string.ascii_lowercase))