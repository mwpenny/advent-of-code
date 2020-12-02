#!/usr/bin/python3

def process_node(header):
	child_node_count = header.pop(0)
	metadata_count = header.pop(0)

	child_node_values = []
	node_value = 0
	metadata_sum = 0

	for i in range(child_node_count):
		child_metadata_sum, child_node_value = process_node(header)
		metadata_sum += child_metadata_sum
		child_node_values.append(child_node_value)

	for i in range(metadata_count):
		m = header.pop(0)
		metadata_sum += m

		if not child_node_values:
			node_value += m
		elif 0 < m <= len(child_node_values):
			node_value += child_node_values[m - 1]

	return metadata_sum, node_value


with open('input', 'r') as f:
	serialized = [int(x) for x in f.read().strip().split(' ')]
	print(process_node(serialized))