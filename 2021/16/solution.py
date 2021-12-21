#!/usr/bin/python3

from math import prod

class Packet:
	def __init__(self, bit_str):
		self._bit_str = bit_str
		self._idx = 0

		self.version = self._read_bits(3)
		self.type_id = self._read_bits(3)
		self.value = 0
		self.sub_packets = []

		if self.type_id == 4:
			value_bit_str = ''
			while True:
				bits = self._read_bits(5)
				value_bit_str += f'{bits & 0xF:04b}'
				if (bits & 0x10) == 0:
					break
			self.value = int(value_bit_str, 2)
		elif self._read_bits(1):
			sub_packet_count = self._read_bits(11)
			for _ in range(sub_packet_count):
				self.sub_packets.append(Packet(self._bit_str[self._idx:]))
				self._idx += self.sub_packets[-1]._idx
		else:
			sub_packets_len = self._read_bits(15)
			end = self._idx + sub_packets_len
			while self._idx < end:
				self.sub_packets.append(Packet(self._bit_str[self._idx:]))
				self._idx += self.sub_packets[-1]._idx

	def _read_bits(self, count):
		val = int(self._bit_str[self._idx:self._idx+count], 2)
		self._idx += count
		return val

	def sum_versions(self):
		return self.version + sum(p.sum_versions() for p in self.sub_packets)

	def evaluate(self):
		return [
			sum,
			prod,
			min,
			max,
			lambda _: self.value,
			lambda vals: vals[0] > vals[1],
			lambda vals: vals[0] < vals[1],
			lambda vals: vals[0] == vals[1]
		][self.type_id]([p.evaluate() for p in self.sub_packets])


with open('input', 'r') as f:
	hex_str = f.read().strip()
	bit_len = len(hex_str) * 4
	bin_str = f'{int(hex_str, 16):0{bit_len}b}'
	root = Packet(bin_str)

	# Part 1
	print('Sum of version numbers:', root.sum_versions())

	# Part 2
	print('Evaluated value:', root.evaluate())
