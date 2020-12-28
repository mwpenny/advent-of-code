#!/usr/bin/python3

def match_rule(s, rules, rulenum, i=0):
	if i >= len(s):
		return []

	rule = rules[rulenum]
	if rule.startswith('"'):
		return [i+1] if s[i] == rule.strip('"') else []

	match_end_indices = []
	for r in rule.split(' | '):
		search_indices = [i]

		for num in map(int, r.split()):
			search_indices = sum((match_rule(s, rules, num, i) for i in search_indices), [])
		match_end_indices += search_indices

	return match_end_indices

def is_valid(s, rules):
	return len(s) in match_rule(s, rules, 0)


with open('input', 'r') as f:
	rule_lines, message_lines = f.read().split('\n\n')
	rules = {int(line.split(': ')[0]): line.split(': ')[1] for line in rule_lines.split('\n')}
	messages = message_lines.split('\n')

	# Part 1
	valid_messages = [m for m in messages if is_valid(m, rules)]
	print('Valid message count:', len(valid_messages))

	# Part 2
	rules[8] = '42 | 42 8'
	rules[11] = '42 31 | 42 11 31'
	valid_messages = [m for m in messages if is_valid(m, rules)]
	print('Valid message count with modified rules:', len(valid_messages))