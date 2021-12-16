#!/usr/bin/python3

from collections import defaultdict

def traverse(graph, allow_visit_lower_twice):
	path_count = 0
	to_visit = [('start', set(), False)]

	while to_visit:
		node, visited, visited_lower_twice = to_visit.pop()
		visited.add(node)

		if node == 'end':
			path_count += 1
		else:
			for n in graph[node]:
				if n.isupper() or n not in visited:
					to_visit.append((n, set(visited), visited_lower_twice))
				elif not visited_lower_twice and n != 'start' and allow_visit_lower_twice:
					to_visit.append((n, set(visited), True))
	return path_count


with open('input', 'r') as f:
	graph = defaultdict(set)
	for line in f:
		a, b = line.strip().split('-')
		graph[a].add(b)
		graph[b].add(a)

	# Part 1
	print('Paths visiting small caves at most once:', traverse(graph, False))

	# Part 2
	print('Paths visiting one small cave up to 2 times:', traverse(graph, True))
