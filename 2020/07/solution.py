#!/usr/bin/python3

from collections import defaultdict
import re

PARENT_BAG_REGEX = re.compile(r'^(.+?) bags')
CHILD_BAG_REGEX = re.compile(r'(\d+) (.+?) bag')

def unique_bag_ancestors(bags, bag_name):
	parents = set(name for name, children in bags.items() if bag_name in children)
	return set.union(
		parents,
		*(unique_bag_ancestors(bags, parent) for parent in parents)
	)

def bag_child_count(bags, bag_name):
	children = bags[bag_name]
	return sum(
		count * (bag_child_count(bags, name) + 1) for name, count in children.items()
	)


with open('input', 'r') as f:
	# <parent bag name, <child bag name, count>>
	bags = defaultdict(dict)

	for line in f:
		parent_bag_name = PARENT_BAG_REGEX.match(line).groups()[0]
		for child_bag_count, child_bag_name in CHILD_BAG_REGEX.findall(line):
			bags[parent_bag_name][child_bag_name] = int(child_bag_count)

	# Part 1
	ancestor_count = len(unique_bag_ancestors(bags, 'shiny gold'))
	print('# of bags that can contain shiny gold:', ancestor_count)

	# Part 2
	child_count = bag_child_count(bags, 'shiny gold')
	print('# of bags contained within shiny gold:', child_count)