#!/usr/bin/python3

def simulate(p1_cards, p2_cards, recursive):
	seen_states = set()

	while p1_cards and p2_cards:
		if recursive:
			state = (tuple(p1_cards), tuple(p2_cards))
			if state in seen_states:
				return True
			seen_states.add(state)

		p1_card, p2_card = p1_cards.pop(0), p2_cards.pop(0)
		if recursive and len(p1_cards) >= p1_card and len(p2_cards) >= p2_card:
			p1_wins = simulate(p1_cards[:p1_card], p2_cards[:p2_card], recursive)
		else:
			p1_wins = p1_card > p2_card

		if p1_wins:
			p1_cards += [p1_card, p2_card]
		else:
			p2_cards += [p2_card, p1_card]

	return bool(p1_cards)

def winning_score(p1_cards, p2_cards, recursive):
	simulate(p1_cards, p2_cards, recursive)
	return sum(map(lambda c: (c[0]+1)*c[1], enumerate(reversed(p1_cards or p2_cards))))


with open('input', 'r') as f:
	split = f.read().strip().split('\n\n')
	p1_cards = list(map(int, split[0].split('\n')[1:]))
	p2_cards = list(map(int, split[1].split('\n')[1:]))

	# Part 1
	print('Winning score:', winning_score(p1_cards[:], p2_cards[:], False))

	# Part 2
	print('Winning score (recursive):', winning_score(p1_cards[:], p2_cards[:], True))