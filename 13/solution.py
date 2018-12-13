#!/usr/bin/python3

class Cart:
	CART_DIRECTIONS = { '^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0) }

	@classmethod
	def is_cart(cls, c):
		return c in cls.CART_DIRECTIONS

	def __init__(self, x, y, c):
		self.x, self.y = x, y
		self.xv, self.yv = self.CART_DIRECTIONS[c]
		self.turn_type = 0
		self.crashed = False

	def turn(self):
		# Intersection turn logic. 0: left, 1: straight, 2: right
		if self.turn_type == 0:
			self.xv, self.yv = self.yv, -self.xv
		elif self.turn_type == 2:
			self.xv, self.yv = -self.yv, self.xv
		self.turn_type = (self.turn_type + 1) % 3


track = []
carts = []
with open('input', 'r') as f:
	lines = f.readlines()
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if Cart.is_cart(c):
				carts.append(Cart(x, y, c))
		track.append(line.replace('^', '|').replace('v', '|').replace('<', '-').replace('>', '-'))


coords = set((c.x, c.y) for c in carts)  # For fast collision lookup
crashed_cart_count = 0
while crashed_cart_count < len(carts) - 1:
	for cart in carts:
		if cart.crashed:
			continue

		# Which direction do we need to go?
		curr_track_piece = track[cart.y][cart.x]
		if curr_track_piece == '\\':
			cart.xv, cart.yv = cart.yv, cart.xv
		elif curr_track_piece == '/':
			cart.xv, cart.yv = -cart.yv, -cart.xv
		elif curr_track_piece == '+':
			cart.turn()

		coords.remove((cart.x, cart.y))
		cart.x += cart.xv
		cart.y += cart.yv

		if (cart.x, cart.y) in coords:  # Crash!
			if crashed_cart_count == 0:
				print('First crash: (%d,%d)' % (cart.x, cart.y))

			for c in carts:
				if (c.x, c.y) == (cart.x, cart.y):
					c.crashed = True
			crashed_cart_count += 2
			coords.remove((cart.x, cart.y))
		else:
			coords.add((cart.x, cart.y))		
	carts = sorted(carts, key=lambda c: [c.y, c.x])  # Top to bottom, left to right

last_cart = [(c.x, c.y) for c in carts if not c.crashed].pop()
print('Last cart standing: (%d,%d)' % last_cart)