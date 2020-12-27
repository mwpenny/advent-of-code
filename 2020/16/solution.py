#!/usr/bin/python3

from functools import reduce
from math import prod
import re

RANGE_REGEX = re.compile(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)')

def parse_ticket(line):
	return list(map(int, line.split(',')))

def is_field_value_valid(num, field_ranges):
	return any(num in range(*r) for r in field_ranges)

def is_num_valid(num, fields):
	return any(is_field_value_valid(num, field_ranges) for field_ranges in fields.values())

def invalid_nums(ticket, fields):
	return [num for num in ticket if not is_num_valid(num, fields)]


with open('input', 'r') as f:
	field_lines, my_ticket_lines, nearby_lines = f.read().split('\n\n')

	fields = dict()
	for field_line in field_lines.splitlines():
		groups = RANGE_REGEX.search(field_line).groups()
		nums = list(map(int, groups[1:]))
		fields[groups[0]] = [(nums[0], nums[1]+1), (nums[2], nums[3]+1)]

	my_ticket = parse_ticket(my_ticket_lines.splitlines()[1])
	nearby_tickets = list(map(parse_ticket, nearby_lines.splitlines()[1:]))

	# Part 1
	invalid_total = reduce(lambda a, b: a + sum(invalid_nums(b, fields)), nearby_tickets, 0)
	print('Ticket scanning error rate:', invalid_total)

	# Part 2
	valid_tickets = [t for t in nearby_tickets if not invalid_nums(t, fields)]
	candidate_fields = [set(fields) for _ in fields]

	for valid_ticket in valid_tickets:
		for i, num in enumerate(valid_ticket):
			candidates = [f for f in fields if is_field_value_valid(num, fields[f])]
			candidate_fields[i].intersection_update(candidates)

	while True:
		ambiguous_fields = [fs for fs in candidate_fields if len(fs) > 1]
		if not ambiguous_fields:
			break

		for fields in ambiguous_fields:
			fields.difference_update(*(fs for fs in candidate_fields if len(fs) == 1))

	print('Departure field product:', prod(
		num for (i, num) in enumerate(my_ticket)
		if candidate_fields[i].pop().startswith('departure')
	))