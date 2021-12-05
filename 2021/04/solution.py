#!/usr/bin/python3

from collections import OrderedDict

BOARD_LENGTH = 5

def update_boards(boards, winners, num):
	for board_idx, board in enumerate(boards):
		if board_idx in winners:
			continue

		for pos, (board_num, _) in board.items():
			if board_num == num:
				board[pos] = (num, True)

		for i in range(BOARD_LENGTH):
			if all(board[(i, j)][1] for j in range(BOARD_LENGTH)) or \
				all(board[(j, i)][1] for j in range(BOARD_LENGTH)):
				winners[board_idx] = num
				break

def board_score(boards, board_idx, num):
	unmarked = filter(lambda space: not space[1], boards[board_idx].values())
	return num * sum(space[0] for space in unmarked)


with open('input', 'r') as f:
	nums = [int(num_str) for num_str in f.readline().strip().split(',')]
	boards = []

	while f.readline():
		board = dict()
		for y in range(BOARD_LENGTH):
			for x, num in enumerate(map(int, f.readline().split())):
				board[x, y] = (num, False)
		boards.append(board)

	winners = OrderedDict()
	while nums:
		num = nums.pop(0)
		update_boards(boards, winners, num)

	# Part 1
	print('Score of first winner:', board_score(boards, *winners.popitem(False)))

	# Part 2
	print('Score of last winner:', board_score(boards, *winners.popitem()))
