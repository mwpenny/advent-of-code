#!/usr/bin/python3

class CPU:
	def __init__(self, code):
		self.regs = [0 for i in range(6)]
		self.code = code
		self.pc = 0
		self.pc_reg_idx = None

		if self.code[0][0] == '#ip':
			self.pc_reg_idx = self.code[0][1]
			self.code.pop(0)

	def update_bound_pc_reg(self):
		if self.pc_reg_idx is not None:
			self.regs[self.pc_reg_idx] = self.pc

	def run(self):
		while self.pc < len(self.code):
			instruction, a, b, c = self.code[self.pc]
			self.regs[self.pc_reg_idx] = self.pc
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
			self.pc = self.regs[self.pc_reg_idx]
			self.pc += 1

# Part 1 runs fast enough to interpret in a reasonable amount of time
with open('input', 'r') as f:
	code = []
	for line in f.read().split('\n'):
		loc = []
		for i, tok in enumerate(line.split(' ')):
			if i > 0:
				loc.append(int(tok))
			else:
				loc.append(tok)
		code.append(loc)

cpu = CPU(code)
cpu.run()
print('Part 1:', cpu.regs[0])

# Part 2. The algorithm in the input finds the sum of the factors of
# what is in cpu.regs[5]. Just calculate it.
n = 10551367
print('Sum of factors of %d:' % n, sum([i for i in range(1, n+1) if n % i == 0]))