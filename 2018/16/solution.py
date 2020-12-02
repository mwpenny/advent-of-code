#!/usr/bin/python3

import re

class CPU:
	INSTRUCTIONS = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
					'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

	def __init__(self):
		self.regs = [0 for i in range(4)]

	def run(self, loc):
		instruction, a, b, c = loc
		if instruction =='addr':
			self.regs[c] = self.regs[a] + self.regs[b]
		elif instruction =='addi':
			self.regs[c] = self.regs[a] + b
		elif instruction =='mulr':
			self.regs[c] = self.regs[a] * self.regs[b]
		elif instruction =='muli':
			self.regs[c] = self.regs[a] * b
		elif instruction =='banr':
			self.regs[c] = self.regs[a] & self.regs[b]
		elif instruction =='bani':
			self.regs[c] = self.regs[a] & b
		elif instruction =='borr':
			self.regs[c] = self.regs[a] | self.regs[b]
		elif instruction =='bori':
			self.regs[c] = self.regs[a] | b
		elif instruction =='setr':
			self.regs[c] = self.regs[a]
		elif instruction =='seti':
			self.regs[c] = a
		elif instruction =='gtir':
			self.regs[c] = int(a > self.regs[b])
		elif instruction =='gtri':
			self.regs[c] = int(self.regs[a] > b)
		elif instruction =='gtrr':
			self.regs[c] = int(self.regs[a] > self.regs[b])
		elif instruction =='eqir':
			self.regs[c] = int(a == self.regs[b])
		elif instruction =='eqri':
			self.regs[c] = int(self.regs[a] == b)
		elif instruction =='eqrr':
			self.regs[c] = int(self.regs[a] == self.regs[b])


LIST_REGEX = re.compile(r'.+?((?:\d(?:,\s)?)+)')
def parse_sample(sample):
	before, loc, after = sample.split('\n')

	before = [int(x) for x in LIST_REGEX.match(before).groups()[0].split(', ')]
	loc = [int(x) for x in loc.split(' ')]
	after = [int(x) for x in LIST_REGEX.match(after).groups()[0].split(', ')]

	return before, loc, after


very_ambiguous_opcodes = 0
opcode_map = [set(CPU.INSTRUCTIONS) for i in range(len(CPU.INSTRUCTIONS))]
with open('input', 'r') as f:
	samples, code = f.read().split('\n\n\n\n')

	cpu = CPU()
	for sample in samples.split('\n\n'):
		before, loc, after = parse_sample(sample)

		# Which instruction(s) does this sample look like?
		matched_instructions = set()
		for instruction in CPU.INSTRUCTIONS:
			cpu.regs = before[:]
			cpu.run([instruction] + loc[1:])
			if cpu.regs == after:
				matched_instructions.add(instruction)

		if len(matched_instructions) > 0:
			opcode_map[loc[0]].intersection_update(matched_instructions)
		if len(matched_instructions) >= 3:
			very_ambiguous_opcodes += 1

	# Part 1
	print('Very ambiguous opcodes (>= 3 matches):', very_ambiguous_opcodes)

	# Part 2
	#
	# Determine opcode => instruction mapping by continually removing already
	# found instructions until all that is left is one instruction per opcode.
	# Assumes that there were enough samples to provide sufficient information.
	found_instructions = set()
	while len(found_instructions) < len(opcode_map):
		for opcode, instructions in enumerate(opcode_map):
			if len(instructions) == 1:
				found_instructions.update(instructions)
			else:
				instructions.difference_update(found_instructions)

	# Run test program
	cpu = CPU()
	for line in code.strip().split('\n'):
		loc = [int(x) for x in line.strip().split(' ')]
		loc[0] = next(iter(opcode_map[loc[0]]))
		cpu.run(loc)
	print('Register 0 after test program:', cpu.regs[0])