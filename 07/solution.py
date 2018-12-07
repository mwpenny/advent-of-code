#!/usr/bin/python3

import re

class Node:
	def __init__(self, letter):
		self.letter = letter
		self.children = []
		self.parents = []

	def add_child(self, child):
		self.children.append(child)
		child.parents.append(self)

	def finish_build_step(self, stack):
		# Only move to the child if all of its dependencies are satisfied
		for child in self.children:
			child.parents.remove(self)
			if not child.parents:
				stack.append(child)

		# Always choose the next node that comes first alphabetically
		stack[:] = sorted(stack, reverse=True)

	def __lt__(self, other):
		return self.letter < other.letter

	def __eq__(self, other):
		return self.letter == other.letter

class Worker:
	def __init__(self):
		self.time = 0
		self.node = None

	def needs_work(self):
		return self.time == 0 and self.node is None

	def give_work(self, node):
		self.time = ord(node.letter) - ord('A') + 61
		self.node = node

	def update(self, stack):
		if self.time > 0:
			self.time -= 1
		if self.time == 0 and self.node is not None:
			# Finish work
			self.node.finish_build_step(stack)
			self.node = None


def build_tree():
	DEPENDENCY_REGEX = re.compile(r'Step (.) must be finished before step (.)')
	tree_nodes = {}

	with open('input', 'r') as f:
		for line in f:
			parent, child = DEPENDENCY_REGEX.match(line).groups()
			if child not in tree_nodes:
				tree_nodes[child] = Node(child)
			if parent not in tree_nodes:
				tree_nodes[parent] = Node(parent)
			tree_nodes[parent].add_child(tree_nodes[child])

	# There may be multiple roots. Put them all under one
	root = Node('')
	for node in tree_nodes.values():
		if not node.parents:
			root.add_child(node)
	root.children = sorted(root.children, reverse=True)
	return root


# Part 1
stack = [build_tree()]
build_order = ''
while stack:
	node = stack.pop()
	build_order += node.letter
	node.finish_build_step(stack)
print('Single-worker completion order:', build_order)


# Part 2
workers = [Worker() for i in range(5)]
stack = build_tree().children
time = 0
while True:
	# Update workers
	map(lambda w: w.update(stack), workers)

	# Look for more work
	for worker in workers:
		if worker.needs_work() and stack:
			worker.give_work(stack.pop())

	if all(worker.needs_work() for worker in workers):
		break
	time += 1

print('Time taken with %d workers' % len(workers), time)