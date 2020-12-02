#!/usr/bin/python3

from collections import deque
import sys

# Pathfinding using breadth-first search (simple, and fast enough for this
# purpose).s Using BFS, we will always find the shortest path. Successors
# are added in reading order, so ties always go to the top leftmost point.
class SearchNode:
	def __init__(self, x, y, parent=None):
		self.parent = parent
		self.x, self.y = x, y

	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)

	def __lt__(self, other):
		return (self.y, self.x) < (other.y, other.x)

	def __hash__(self):
		return hash((self.x, self.y))

def bfs(start_x, start_y, goal_x, goal_y, sim):
	fringe = deque([SearchNode(start_x, start_y)])
	goal_node = SearchNode(goal_x, goal_y)
	closed = set()

	while len(fringe) > 0:
		node = fringe.popleft()
		if node in closed:
			continue
		closed.add(node)

		if node == goal_node:
			path_cost = 1
			next_step = None
			while node.parent is not None:
				path_cost += 1
				next_step = node
				node = node.parent
			return path_cost, next_step
		else:
			for (x, y) in sim.adj_points(node, Unit.not_unit):
				fringe.append(SearchNode(x, y, node))
	return None, None


# Elf or goblin
class Unit:
	def __init__(self, sim, x, y, elf, atk):
		self.hp = 200
		self.sim = sim
		self.x, self.y = x, y
		self.elf = elf
		self.atk = atk

	@classmethod
	def not_unit(cls, u):
		return u is None or u.dead()

	def dead(self):
		return self.hp <= 0

	def attack(self, other):
		other.hp -= self.atk

	def is_enemy(self, other):
		return other is not None and not other.dead() and self.elf != other.elf

	def try_attack_target(self):
		targets = []
		for (x, y) in self.sim.adj_points(self, self.is_enemy):
			targets.append(sim.units[(x, y)])

		if targets:
			self.attack(min(targets, key=lambda t: t.hp))
			return True
		return False

	def try_move_toward_target(self):
		dests = []
		for u in self.sim.units.values():
			if self.is_enemy(u):
				dests.extend(self.sim.adj_points(u, self.not_unit))

		# Find minimum cost move, using reading order to resolve ties
		min_cost = sys.maxsize
		dest = SearchNode(sys.maxsize, sys.maxsize)
		for (dst_x, dst_y) in dests:
			cost, first_step = bfs(self.x, self.y, dst_x, dst_y, self.sim)
			if (first_step is not None and cost < min_cost) or (cost == min_cost and first_step < dest):
				min_cost = cost
				dest = first_step

		# Found a point to move into
		if min_cost != sys.maxsize:
			del self.sim.units[(self.x, self.y)]
			self.x, self.y = dest.x, dest.y
			self.sim.units[(self.x, self.y)] = self
			return True
		return False

# Elf vs. goblin fight
class Simulation:
	READING_ORDER_OFFSETS = [(0, -1), (-1, 0), (1, 0), (0, 1)]

	def __init__(self, cave, units):
		self.units = units
		self.cave = cave

	@classmethod
	def from_input(cls, elf_atk=3, file='input'):
		sim = Simulation([], {})
		with open(file, 'r') as f:
			lines = f.readlines()
			for y, line in enumerate(lines):
				for x, c in enumerate(line):
					if c in 'EG':
						elf = c == 'E'
						sim.units[(x, y)] = Unit(sim, x, y, elf, elf_atk if elf else 3)
				sim.cave.append(line.replace('G', '.').replace('E', '.'))
		return sim

	def adj_points(self, p, condition):
		# Find non-blocked points adjacent to p arranged in reading order
		points = []
		for (ofs_x, ofs_y) in self.READING_ORDER_OFFSETS:
			adj_x, adj_y = p.x + ofs_x, p.y + ofs_y
			if self.cave[adj_y][adj_x] != '#':
				u = self.units.get((adj_x, adj_y), None)
				if condition(u):
					points.append((adj_x, adj_y))
		return points

	def alive_units(self):
		alive_elves = sum(1 for u in self.units.values() if not u.dead() and u.elf)
		alive_goblins = sum(1 for u in self.units.values() if not u.dead() and not u.elf)
		return alive_elves, alive_goblins

	def simulate(self, break_on_elf_death=False):
		# Fight!
		turns = 0
		start_alive_elves, _ = self.alive_units()
		while True:
			turn_order = sorted(self.units.values(), key=lambda u: [u.y, u.x])  # "Reading order"
			for i, unit in enumerate(turn_order):
				if unit.dead():
					continue

				if not unit.try_attack_target():
					# Nothing to attack. Need to move
					unit.try_move_toward_target() and unit.try_attack_target()

				alive_elves, alive_goblins = self.alive_units()
				elf_deaths = start_alive_elves - alive_elves
				if break_on_elf_death and elf_deaths > 0:  # For part 2
					return None, elf_deaths
				elif (alive_goblins == 0) or (alive_elves == 0):  # Done!
					# Edge case: last enemy dies at the end of the round
					if i == len(turn_order) - 1:
						turns += 1
					return turns * sum(u.hp for u in sim.units.values() if not u.dead()), elf_deaths
			turns += 1

# Part 1
sim = Simulation.from_input()
print ('Battle 1 outcome:', sim.simulate()[0])

# Part 2
elf_atk = 4
while True:
	sim = Simulation.from_input(elf_atk)
	outcome, elf_deaths = sim.simulate(True)
	if elf_deaths == 0:
		print('No elf death outcome:', outcome)
		break
	elf_atk += 1