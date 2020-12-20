#!/usr/bin/python3

import re

MASK_REGEX = re.compile(r'mask = (.+)')
CODE_REGEX = re.compile(r'mem\[(\d+)\] = (\d+)')

def get_floating_addrs(addr):
	addrs = []
	if 'X' in addr:
		addrs += get_floating_addrs(addr.replace('X', '1', 1))
		addrs += get_floating_addrs(addr.replace('X', '0', 1))
	else:
		addrs.append(int(addr, 2))
	return addrs


with open('input', 'r') as f:
	memory = dict()
	floating_memory = dict()
	or_mask = 0
	and_mask = -1

	for line in f:
		mask_match = MASK_REGEX.match(line)
		if mask_match:
			mask = mask_match.groups()[0]
			or_mask = int(mask.replace('X', '0'), 2)
			and_mask = int(mask.replace('X', '1'), 2)
		else:
			idx, value = map(int, CODE_REGEX.match(line).groups())
			memory[idx] = (value | or_mask) & and_mask

			floating_addresses = get_floating_addrs(
				''.join([mask[i] if mask[i] != '0' else b for i, b in enumerate(f'{idx:036b}')])
			)
			for addr in floating_addresses:
				floating_memory[addr] = value

	# Part 1
	s = sum(memory.values())
	print('Sum of memory after initialization:', s)

	# Part 2
	s = sum(floating_memory.values())
	print('Sum of floating memory after initialization:', s)