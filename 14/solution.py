#!/usr/bin/python3

scoreboard = [3, 7]
r1_idx = 0
r2_idx = 1

p1_recipe_count = None
with open('input', 'r') as f:
	p1_recipe_count = int(f.read().strip())
p2_pattern=[int(c) for c in str(p1_recipe_count)]

done = False
while not done:
	r1 = scoreboard[r1_idx]
	r2 = scoreboard[r2_idx]
	for c in str(r1 + r2):
		scoreboard.append(int(c))

		# Part 1
		if len(scoreboard) == p1_recipe_count + 10:
			print('10 recipes after input number:', ''.join(str(x) for x in scoreboard[p1_recipe_count:]))

		# Part 2
		if scoreboard[-len(p2_pattern):] == p2_pattern:
			print('Index of pattern:', len(scoreboard) - len(p2_pattern))
			done = True
			break

	r1_idx = (r1_idx + r1 + 1) % len(scoreboard)
	r2_idx = (r2_idx + r2 + 1) % len(scoreboard)