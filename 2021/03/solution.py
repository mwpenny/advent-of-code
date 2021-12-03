#!/usr/bin/python3

def count_bits(nums, bit_length):
	set_bit_counts = [0] * bit_length
	for num in nums:
		for i in range(len(set_bit_counts)):
			set_bit_counts[i] += 1 if (num & (1 << i)) else -1

	most_common, least_common = 0, 0
	for i, count in enumerate(set_bit_counts):
		if count >= 0:
			most_common |= 1 << i
		else:
			least_common |= 1 << i
	return most_common, least_common

def filter_nums(nums, bit, filter_bits):
	return list(filter(lambda n: (n & (1 << bit)) == (filter_bits & (1 << bit)), nums))


with open('input', 'r') as f:
	nums = [int(line.strip(), 2) for line in f]
	bit_length = max(num.bit_length() for num in nums)

	# Part 1
	gamma_rate, epsilon_rate = count_bits(nums, bit_length)
	print('Power consumption:', gamma_rate * epsilon_rate)

	# Part 2
	filtered_most_common = nums
	filtered_least_common = nums
	for i in reversed(range(bit_length)):
		if len(filtered_most_common) > 1:
			most_common, _ = count_bits(filtered_most_common, bit_length)
			filtered_most_common = filter_nums(filtered_most_common, i, most_common)

		if len(filtered_least_common) > 1:
			_, least_common = count_bits(filtered_least_common, bit_length)
			filtered_least_common = filter_nums(filtered_least_common, i, least_common)

	print('Life support rating:', filtered_most_common[0] * filtered_least_common[0])
