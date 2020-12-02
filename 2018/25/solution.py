#!/usr/bin/python3

class DisjointSet:
	def __init__(self, n):
		self.parents = list(range(n))
		self.ranks = [0] * n
		self.count = n

	def find(self, x):
		if self.parents[x] != x:
			self.parents[x] = self.find(self.parents[x])
		return self.parents[x]

	def union(self, x, y):
		root_x = self.find(x)
		root_y = self.find(y)

		if root_x != root_y:
			shorter, taller = sorted([root_x, root_y], key=lambda r: self.ranks[r])
			self.parents[shorter] = taller
			if self.ranks[shorter] == self.ranks[taller]:
				self.ranks[taller] += 1
			self.count -= 1


def manhattan(p1, p2):
	return sum(abs(p1[i] - p2[i]) for i in range(4))


points = []
with open('input', 'r') as f:
	points = [tuple([int(x) for x in line.strip().split(',')]) for line in f]

sets = DisjointSet(len(points))
for x in range(len(points)):
	for y in range(x):
		if manhattan(points[x], points[y]) <= 3:
			sets.union(x, y)
print('Constellation count:', sets.count)