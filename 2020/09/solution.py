#!/usr/bin/python3

PREAMBLE_LENGTH = 25

def find_addends(desired_sum, numbers):
	for num1 in numbers:
		num2 = desired_sum - num1
		if num2 in numbers:
			return (num1, num2)
	return (0, 0)

def find_contiguous_addends(desired_sum, numbers):
	for start_idx in range(len(numbers)):
		running_sum = 0

		for i, num in enumerate(numbers[start_idx:]):
			running_sum += num
			if running_sum > desired_sum:
				break
			elif running_sum == desired_sum:
				return numbers[start_idx:start_idx+i]
	return []


with open('input', 'r') as f:
	numbers = list(int(line) for line in f)

	for i in range(PREAMBLE_LENGTH, len(numbers)):
		prev_nums, num = numbers[i-PREAMBLE_LENGTH:i], numbers[i]
		if find_addends(num, prev_nums) == (0, 0):
			break

	# Part 1
	print('First invalid number:', num)

	# Part 2
	addends = find_contiguous_addends(num, numbers)
	weakness = min(addends) + max(addends)
	print('Encryption weakness:', weakness)