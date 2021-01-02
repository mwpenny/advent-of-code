#!/usr/bin/python3

def simulate(cups, n):
	curr_cup = cups[0]
	next_cup = { c: cups[(i + 1) % len(cups)] for i, c in enumerate(cups) }

	for _ in range(n):
		c = curr_cup
		cups_to_move = [c := next_cup[c] for _ in range(3)]

		dst_cup = curr_cup
		while dst_cup == curr_cup or dst_cup in cups_to_move:
			dst_cup = ((dst_cup - 1) % (len(cups) + 1)) or len(cups)

		next_cup[curr_cup] = next_cup[cups_to_move[-1]]
		next_cup[cups_to_move[-1]] = next_cup[dst_cup]
		next_cup[dst_cup] = cups_to_move[0]

		curr_cup = next_cup[curr_cup]
	return next_cup


with open('input', 'r') as f:
	cups = [int(c) for c in f.read()]

	# Part 1
	next_cup = simulate(cups, 100)
	arrangement = ''
	cup = 1
	while (cup := next_cup[cup]) != 1:
		arrangement += str(cup)
	print('Arrangement after 100 moves:', arrangement)

	# Part 2
	cups += list(range(len(cups) + 1, 1000001))
	next_cup = simulate(cups, 10000000)
	print('Product of cups right of 1:', next_cup[1] * next_cup[next_cup[1]])