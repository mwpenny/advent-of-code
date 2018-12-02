#!/usr/bin/python3
from collections import defaultdict

twos = 0
threes = 0

with open('input', 'r') as f:
	for line in f:
		char_counts = defaultdict(int)
		for c in line:
			char_counts[c] += 1
		if 2 in char_counts.values():
			twos += 1
		if 3 in char_counts.values():
			threes += 1

print(twos * threes)