#!/usr/bin/python3

from collections import defaultdict, Counter
import re

GUARD_NUM_REGEX = re.compile(r'.*#(\d+)')
MINUTE_REGEX = re.compile(r'.*:(\d+)')

guards = defaultdict(Counter)

with open('input', 'r') as f:
	entries = sorted(f.readlines())

	guard_num = 0
	sleep_min = 0
	for entry in entries:
		m = GUARD_NUM_REGEX.match(entry)
		if m:
			guard_num = int(m.group(1))
		elif 'falls asleep' in entry:
			sleep_min = int(MINUTE_REGEX.match(entry).group(1))
		else:
			# Wakes up
			wake_min = int(MINUTE_REGEX.match(entry).group(1))
			guards[guard_num].update(range(sleep_min, wake_min))

# Part 1
sleepy_guard = max(guards.keys(), key=lambda gid: sum(guards[gid].values()))
guard_nap_time = guards[sleepy_guard].most_common(1)[0][0]
print(guard_nap_time * sleepy_guard)

# Part 2
most_slept_min = 0
most_slept_min_count = -1
most_slept_min_guard = 0
for m in range(60):
	count, gid = max([(guards[gid][m], gid) for gid in guards], key=lambda x: x[0])
	if count > most_slept_min_count:
		most_slept_min = m
		most_slept_min_count = count
		most_slept_min_guard = gid
print(most_slept_min * most_slept_min_guard)