#!/usr/bin/python3

def one_char_differs(str1, str2):
	diff_idx = -1
	for i in range(len(str1)):
		if str1[i] != str2[i]:
			if diff_idx >= 0:
				return False, -1
			diff_idx = i
	return True, diff_idx


def find_similar_ids(box_ids):
	for box1 in range(len(box_ids)):
		for box2 in range(box1 + 1, len(box_ids)):
			box1_id = box_ids[box1].strip()
			box2_id = box_ids[box2].strip()

			if len(box1_id) != len(box2_id):
				continue

			has_one_diff, diff_idx = one_char_differs(box1_id, box2_id)
			if has_one_diff:
				return box1_id, box2_id, box1_id[:diff_idx] + box1_id[diff_idx + 1:]


with open('input', 'r') as f:
	box_ids = f.readlines()
	print(find_similar_ids(box_ids))