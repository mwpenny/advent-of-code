#!/usr/bin/python3

UNIQUE_SEG_COUNT_DIGITS = { 2: 1, 3: 7, 4: 4, 7: 8 }

def sorted_str(s):
	return ''.join(sorted(s))


with open('input', 'r') as f:
	unique_segment_digit_count = 0
	value_total = 0

	for line in f:
		segments, output = [s.split() for s in line.strip().split(' | ')]

		digit_segments = {
			UNIQUE_SEG_COUNT_DIGITS[len(s)]: set(s)
			for s in segments if len(s) in UNIQUE_SEG_COUNT_DIGITS
		}

		for s in map(set, segments):
			if len(s) == 5:
				if digit_segments[1].issubset(s):
					digit_segments[3] = s
				elif len(s & digit_segments[4]) == 3:
					digit_segments[5] = s
				else:
					digit_segments[2] = s
			elif len(s) == 6:
				if digit_segments[4].issubset(s):
					digit_segments[9] = s
				elif digit_segments[1].issubset(s):
					digit_segments[0] = s
				else:
					digit_segments[6] = s

		segment_digits = { sorted_str(v): k for k, v in digit_segments.items() }

		for i, pattern in enumerate(reversed(output)):
			value = segment_digits[sorted_str(pattern)]

			if value in UNIQUE_SEG_COUNT_DIGITS.values():
				unique_segment_digit_count += 1
			value_total += value * pow(10, i)

	# Part 1
	print('Unique segment digit count:', unique_segment_digit_count)

	# Part 2
	print('Value total:', value_total)
