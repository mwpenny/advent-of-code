#!/usr/bin/python3

from functools import reduce
import operator

def chinese_remainder(remainders, divisors):
	divisor_product = reduce(operator.mul, divisors)
	result = 0
	for remainder, divisor in zip(remainders, divisors):
		p = (divisor_product // divisor)
		result += p * pow(p, -1, divisor) * remainder
	return result % divisor_product


with open('input', 'r') as f:
	earliest_departure = int(f.readline().strip())
	busses = [(i, int(d)) for i, d in enumerate(f.read().split(',')) if d != 'x']

	# Part 1
	earliest_bus = min(busses, key=lambda b: divmod(earliest_departure, b[1])[0])[1]
	board_time = round(earliest_departure / earliest_bus) * earliest_bus
	result = earliest_bus * (board_time - earliest_departure)
	print('Earliest bus * minutes waiting', result)

	# Part 2
	remainders = [0] + [b[1] - (b[0] % b[1]) for b in busses[1:]]
	divisors = list(map(lambda b: b[1], busses))
	timestamp = chinese_remainder(remainders, divisors)
	print('Earliest timestamp for consecutive busses:', timestamp)