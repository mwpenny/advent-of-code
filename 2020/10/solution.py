#!/usr/bin/python3

from collections import Counter, defaultdict

def build_graph(joltages, nodes=defaultdict(list)):
	parent = joltages[0]
	for i, joltage in enumerate(joltages[1:]):
		if joltage - parent <= 3:
			nodes[parent].append(joltage)
			if joltage not in nodes:
				build_graph(joltages[i+1:], nodes)
		else:
			break
	return nodes

def count_paths(nodes, root=0, path_counts=dict()):
	children = nodes[root]
	if children:
		count = 0
		for node in children:
			if node not in path_counts:
				path_counts[node] = count_paths(nodes, node, path_counts)
			count += path_counts[node]
		return count
	return 1


with open('input', 'r') as f:
	joltages = sorted([int(line) for line in f])
	joltages = [0] + joltages + [joltages[-1] + 3]

	# Part 1
	diff_counts = Counter([j - joltages[i] for i, j in enumerate(joltages[1:])])
	print('1-jolt diffs * 3-jolt diffs:', diff_counts[1] * diff_counts[3])

	# Part 2
	count = count_paths(build_graph(joltages))
	print('Number of arrangements:', count)