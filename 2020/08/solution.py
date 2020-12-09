#!/usr/bin/python3

class CPU:
	def __init__(self, code):
		self.code = code
		self.a = 0
		self.pc = 0
		self.looped = False
		self.executed_locations = set()

	def run(self):
		while self.pc < len(self.code):
			if self.pc in self.executed_locations:
				self.looped = True
				break
			self.executed_locations.add(self.pc)

			instruction, operand = self.code[self.pc]
			if instruction == 'acc':
				self.a += operand
			elif instruction == 'jmp':
				self.pc += operand
				continue

			self.pc += 1

		return self.a


with open('input', 'r') as f:
	code = [(line[0], int(line[1])) for line in (line.split() for line in f)]
	cpu = CPU(code)

	# Part 1
	print('Accumulator before loop:', cpu.run())

	# Part 2
	# Brute force until we get it
	for i, line in enumerate(code):
		instruction, operand = line
		if instruction in ['nop', 'jmp']:
			code_copy = code[:]
			code_copy[i] = ('nop' if instruction == 'jmp' else 'jmp', operand)

			cpu = CPU(code_copy)
			a = cpu.run()
			if not cpu.looped:
				break
	print('Accumulator after normal execution', a)