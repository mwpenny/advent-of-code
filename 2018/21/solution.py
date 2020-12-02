#!/usr/bin/python3

first_seen_end_value = None
last_seen_end_value = None
seen_end_values = set()

# Python implementation of input program. Run until the end value repeats
reg_3 = 0
while True:
	reg_2 = reg_3 | 65536
	reg_3 = 1505483

	while True:
		reg_4 = reg_2 & 255
		reg_3 = (((reg_3 + reg_4) & 16777215) * 65899) & 16777215
		if reg_2 < 256:
			break
		else:
			reg_2 //= 256

	if first_seen_end_value is None:
		first_seen_end_value = reg_3
	if reg_3 in seen_end_values:
		break
	seen_end_values.add(reg_3)
	last_seen_end_value = reg_3

print('Earliest termination:', first_seen_end_value)
print('Latest termination:', last_seen_end_value)