#!/usr/bin/python3

from collections import defaultdict, deque

curr_roots = {(0, 0)}
branch_roots = []
branch_leaves = []
edges = defaultdict(set)
with open('input', 'r') as f:
	# Construct graph
	for c in f.read().strip()[1:-1]:  # Skip '^' and '$'
		if c == '(':
			branch_roots.append(curr_roots)
			branch_leaves.append(set())
		elif c == '|':
			branch_leaves[-1].update(curr_roots)
			curr_roots = branch_roots[-1]
		elif c == ')':
			branch_roots.pop()
			branch_leaves[-1].update(curr_roots)
			curr_roots = branch_leaves.pop()
		elif c in 'NSEW':
			# Apply move to all branches
			new_roots = set()
			for n in curr_roots:
				x_ofs = (c == 'S') - (c == 'N')
				y_ofs = (c == 'E') - (c == 'W')
				new_pos = (n[0] + x_ofs, n[1] + y_ofs)
				edges[n].add(new_pos)
				edges[new_pos].add(n)
				new_roots.add(new_pos)
			curr_roots = new_roots

	# BFS
	fringe = deque([((0, 0), 0)])
	closed = set()
	path_cost = 0
	long_paths = 0
	while fringe:
		v, d = fringe.popleft()
		if v in closed:
			continue
		closed.add(v)
		dist = d
		if dist >= 1000:
			long_paths += 1
		fringe.extend((v2, dist + 1) for v2 in edges[v])
	print('Distance to farthest room:', dist)
	print('Rooms >= 1000 away:', long_paths)