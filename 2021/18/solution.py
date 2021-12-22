#!/usr/bin/python3

from itertools import product

class Pair:
	def __init__(self, left=None, right=None, value=None, parent=None):
		self.left = left
		self.right = right
		self.value = value
		self.parent = parent
		if self.left:
			self.left.parent = self
		if self.right:
			self.right.parent = self

	def __add__(self, other):
		p = Pair(left=self, right=other)
		p._reduce()
		return p

	def _find_value_node(self, search_order):
		if self.value is not None:
			return self
		return getattr(self, search_order[0])._find_value_node(search_order) or \
			getattr(self, search_order[1])._find_value_node(search_order)

	def _explode(self):
		directions = ('left', 'right')
		for i, direction in enumerate(directions):
			prev = self
			curr = self.parent
			while curr:
				adj = getattr(curr, direction)
				if prev is not adj:
					# Found a node to the left/right of the current one. Now
					# look for a value node starting on the side closest to the
					# current node.
					value_node = adj._find_value_node(
						(directions[len(directions) - 1 - i], directions[i])
					)
					if value_node:
						value_node.value += getattr(self, direction).value
						break
				prev = curr
				curr = curr.parent
		self.left = None
		self.right = None
		self.value = 0

	def _split(self):
		self.left = Pair(value=self.value // 2, parent=self)
		self.right = Pair(value=(self.value // 2) + (self.value % 2), parent=self)
		self.value = None

	def _depth(self):
		depth = 0
		curr = self.parent
		while curr:
			depth += 1
			curr = curr.parent
		return depth

	def _try_explode(self):
		if self.value is None:
			if self._depth() == 4:
				self._explode()
				return True
			return self.left._try_explode() or self.right._try_explode()

	def _try_split(self):
		if self.value is not None:
			if self.value >= 10:
				self._split()
				return True
		else:
			return self.left._try_split() or self.right._try_split()

	def _reduce(self):
		while self._try_explode() or self._try_split():
			pass

	@classmethod
	def make(cls, elem):
		if isinstance(elem, int):
			return Pair(value=elem)
		return Pair(left=cls.make(elem[0]), right=cls.make(elem[1]))

	def magnitude(self):
		if self.value is not None:
			return self.value
		return (3 * self.left.magnitude()) + (2 * self.right.magnitude())


with open('input', 'r') as f:
	pairs = [eval(line) for line in f]

	# Part 1
	parsed_pairs = map(Pair.make, pairs)
	final_sum = sum(parsed_pairs, start=next(parsed_pairs))
	print('Magnitude of final sum:', final_sum.magnitude())

	# Part 2
	max_magnitude = 0
	for p1, p2 in product(pairs, pairs):
		if p1 is not p2:
			s = (Pair.make(p1) + Pair.make(p2)).magnitude()
			max_magnitude = max(max_magnitude, s)
	print('Largest magnitude of 2-number sum', max_magnitude)
