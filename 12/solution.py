#!/usr/bin/python3

initial_state = ''
trans_rules = {}
with open('input', 'r') as f:
	lines = f.readlines()

	# Pad beginning and end to keep array lookups in bounds
	initial_state = '..' + lines[0].strip().split('initial state: ')[1] + '...'
	for line in lines[2:]:
		rule, outcome = line.strip().split(' => ')
		trans_rules[rule] = outcome


def next_generation(gen, elem0_idx):
	next_gen = (trans_rules.get(gen[i-2:i+3], '.') for i in range(len(gen)))
	return '..' + ''.join(next_gen) + '...', elem0_idx + 2

def sum_gen(gen, elem0_idx):
	return sum(i - elem0_idx for i, c in enumerate(gen) if c == '#')


# Part 1. 20 generations is small enough to be manually calculated
current_gen = initial_state
pot0_idx = 2  # Account for padding
for i in range(20):
	current_gen, pot0_idx = next_generation(current_gen, pot0_idx)
print('Sum of occupied pot numbers after 20 generations:', sum_gen(current_gen, pot0_idx))


# Part 2
#
# Assume that after a sufficiently large number of generations, the
# difference in output value between them becomes constant
current_gen = initial_state
pot0_idx = 2  # Account for padding
gen_count = 250  # Arbitrarily chosen "large enough" number of generations
last_sum = 0
last_diff = 0
for i in range(gen_count):
	current_gen, pot0_idx = next_generation(current_gen, pot0_idx)
	s = sum_gen(current_gen, pot0_idx)
	last_diff = s - last_sum
	last_sum = s

print('Sum of occupied pot numbers after 20 generations', last_sum + (50000000000 - gen_count) * last_diff)