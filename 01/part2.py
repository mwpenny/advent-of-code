#!/usr/bin/python3

freq = 0
freqs = set()
first_dup = None

with open('input', 'r') as f:
	while first_dup is None:
		f.seek(0)
		for line in f:
			freq += int(line)
			if freq in freqs:
				first_dup = freq
				break
			else:
				freqs.add(freq)

print(first_dup)