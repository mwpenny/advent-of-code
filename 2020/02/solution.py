#!/usr/bin/python3

from collections import Counter
import re

POLICY_REGEX = re.compile(r'(\d+)-(\d+)\s(\w)')

with open('input', 'r') as f:
	policy1_valid_passwords = 0
	policy2_valid_passwords = 0

	for line in f:
		policy_str, password = line.split(': ')
		char_counts = Counter(password)

		parsed_policy = POLICY_REGEX.match(policy_str).groups()
		first_num, second_num = [int(x) for x in parsed_policy[:2]]
		char = parsed_policy[2]

		if first_num <= char_counts[char] <= second_num:
			policy1_valid_passwords += 1
		if (password[first_num - 1] == char) != (password[second_num - 1] == char):
			policy2_valid_passwords += 1

	# Part 1
	print('Number of valid passwords under policy 1:', policy1_valid_passwords)

	# Part 2
	print('Number of valid passwords under policy 2:', policy2_valid_passwords)