#!/usr/bin/python3

import re

UNIT_COUNT_HP_REGEX = re.compile(r'(\d+) units each with (\d+) hit points')
WEAKNESS_REGEX = re.compile(r'.+weak to (.+?)[;|\)]')
IMMUNITY_REGEX = re.compile(r'.+immune to (.+?)[;|\)]')
ATTACK_REGEX = re.compile(r'.+that does (\d+) (.+?) damage at initiative (\d+)')

class Group:
	def __init__(self, count, hp, weaknesses, immunities,
				 damage, damage_type, initiative, infection):
		self.unit_count = count
		self.unit_hp = hp
		self.weaknesses = set(weaknesses)
		self.immunities = set(immunities)

		self.damage = damage
		self.damage_type = damage_type
		self.initiative = initiative
		self.infection = infection

		self.target = None
		self.targeted = False

	def effective_power(self):
		return self.unit_count * self.damage

	def dead(self):
		return self.unit_count <= 0

	def damage_to_give(self, other):
		if self.damage_type in other.immunities:
			return 0
		elif self.damage_type in other.weaknesses:
			return self.effective_power() * 2
		return self.effective_power()

	def target_stats(self):
		if self.target is None:
			return (0, 0, 0)
		return (
			self.damage_to_give(self.target),
			self.target.effective_power(),
			self.target.initiative
		)

	def attack_target(self):
		units_killed = self.damage_to_give(self.target) // self.target.unit_hp
		self.target.unit_count -= units_killed
		self.target.targeted = False

		# We just killed a group that was targeting another group
		# The targeted group should be able to be targeted again
		if self.target.dead():
			if self.target.target:
				self.target.target.targeted = False
				self.target.target = None

		self.target = None
		return units_killed


# Input parsing
def try_match_array(regex, text):
	s = regex.match(text)
	if s:
		return s.groups()[0].split(', ')
	return []

def get_groups(text, infection, boost):
	groups = []
	for line in text:
		stripped = line.strip()

		count, hp = UNIT_COUNT_HP_REGEX.match(stripped).groups()
		weaknesses = try_match_array(WEAKNESS_REGEX, stripped)
		immunities = try_match_array(IMMUNITY_REGEX, stripped)
		damage, damage_type, initiative = ATTACK_REGEX.match(stripped).groups()

		damage = int(damage)
		if not infection:
			damage += boost
		g = Group(int(count), int(hp), weaknesses, immunities,
				  damage, damage_type, int(initiative), infection)
		groups.append(g)
	return groups

def parse_input(boost=0):
	with open('input', 'r') as f:
		split = f.read().strip().split('Immune System:\n')[1]
		split = split.split('\n\nInfection:\n')

		immune_system = get_groups(split[0].split('\n'), False, boost)
		infection = get_groups(split[1].split('\n'), True, boost)
	return immune_system, infection
# /Input parsing


def select_targets(army, enemies):
	sort_key = lambda g: (g.effective_power(), g.initiative)
	for group in sorted(army, key=sort_key, reverse=True):
		if group.dead():
			continue

		for enemy in enemies:
			if enemy.dead() or enemy.targeted:
				continue

			enemy_stats = (
				group.damage_to_give(enemy),
				enemy.effective_power(),
				enemy.initiative
			)
			if enemy_stats[0] == 0:
				continue

			if enemy_stats > group.target_stats():
				if group.target is not None:
					group.target.targeted = False
				group.target = enemy
				enemy.targeted = True

def fight(immune_system, infection):
	while True:
		select_targets(immune_system, infection)
		select_targets(infection, immune_system)

		all_groups = sorted(immune_system + infection, key=lambda g: g.initiative, reverse=True)
		someone_died = False
		for group in all_groups:
			if group.dead():
				continue
			if group.target is not None:
				units_killed = group.attack_target()
				if units_killed:
					someone_died = True

		if not someone_died:
			return 0, 0  # Stalemate

		immune_alive = sum(u.unit_count for u in immune_system if not u.dead())
		infection_alive = sum(u.unit_count for u in infection if not u.dead())

		if not immune_alive or not infection_alive:
			return immune_alive, infection_alive


# Part 1
print('Units alive in winning army:', max(fight(*parse_input())))

# Part 2
boost = 0
while True:
	immune_alive, infected_alive = fight(*parse_input(boost))
	if immune_alive:
		print('Immune units alive after boost of %d:' % boost, immune_alive)
		break
	boost += 1