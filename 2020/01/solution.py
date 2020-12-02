#!/usr/bin/python3

def find_addends(desired_sum, numbers):
	for num1 in numbers:
		num2 = desired_sum - num1
		if num2 in numbers:
			return (num1, num2)
	return (0, 0)


DESIRED_SUM = 2020

with open('input', 'r') as f:
	numbers = [int(line) for line in f]

	# Part 1
	num1, num2 = find_addends(DESIRED_SUM, numbers)
	print('Product of two numbers', num1 * num2)

	# Part 2
	for i, num1 in enumerate(numbers):
		num2, num3 = find_addends(DESIRED_SUM - num1, numbers[i:])

		product = num2 * num3
		if product:
			print('Product of three numbers', num1 * product)
			break