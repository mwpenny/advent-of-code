#!/usr/bin/python3

import re

class Rect:
	CLAIM_REGEX = re.compile(r'#\d+\s@\s(\d+),(\d+):\s(\d+)x(\d+)')

	def __init__(self, x, y, w, h):
		self.x, self.y, self.w, self.h = x, y, w, h

	@classmethod
	def from_claim_str(cls, claim_str):
		return Rect(*[int(x) for x in cls.CLAIM_REGEX.match(claim_str).groups()])

	def apply_to_fabric(self, fabric):
		for y in range(self.y, self.y + self.h):
			for x in range(self.x, self.x + self.w):
				fabric[y][x] += 1

	def has_no_overlaps(self, fabric):
		for y in range(self.y, self.y + self.h):
			for x in range(self.x, self.x + self.w):
				if fabric[y][x] != 1:
					return False
		return True


FABRIC_WIDTH = FABRIC_HEIGHT = 1000
fabric = [[0 for y in range(FABRIC_HEIGHT)] for x in range(FABRIC_WIDTH)]
claims = []

with open('input', 'r') as f:
	for line in f:
		claim = Rect.from_claim_str(line)
		claims.append(claim)
		claim.apply_to_fabric(fabric)

overlap = len([1 for x in range(FABRIC_WIDTH) for y in range(FABRIC_HEIGHT) if fabric[y][x] > 1])
unclaimed_rect_id = [i+1 for i in range(len(claims)) if claims[i].has_no_overlaps(fabric)].pop()
print(overlap, unclaimed_rect_id)