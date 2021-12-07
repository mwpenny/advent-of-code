#!/usr/bin/python3

GESTATION_PERIOD = 7
PUBERTY_PERIOD = 2

def simulate(fish, days):
	birthdays = [0] * (GESTATION_PERIOD + PUBERTY_PERIOD)

	for f in fish:
		birthdays[f] += 1

	for d in range(days):
		# Offspring will have first birth after gestation and puberty periods
		# Parents will give birth again after gestation period
		born_today = birthdays[d % len(birthdays)]
		birthdays[(d + GESTATION_PERIOD) % len(birthdays)] += born_today

	return sum(birthdays)


with open('input', 'r') as f:
	fish = list(map(int, f.read().split(',')))

	# Part 1
	print('Laternfish count after 80 days:', simulate(fish, 80))

	# Part 2
	print('Laternfish count after 256 days:', simulate(fish, 256))
