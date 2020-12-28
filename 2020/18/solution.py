#!/usr/bin/python3

from operator import add, mul

class Operator:
	def __init__(self, func):
		self.func = func

	def __or__(self, other):
		return self.func(other)

	def __ror__(self, other):
		return Operator(lambda x: self.func(other, x))

	def __and__(self, other):
		return self.__or__(other)

	def __rand__(self, other):
		return self.__ror__(other)


with open('input', 'r') as f:
	expressions = f.readlines()

	# Part 1
	print('Sum of expression results (equal precedence):', sum(
		eval(e.replace('+', '|Operator(add)|') .replace('*', '|Operator(mul)|'))
		for e in expressions
	))

	# Part 2
	print('Sum of expression results (addition precedence):', sum(
		eval(e.replace('+', '&Operator(add)&') .replace('*', '|Operator(mul)|'))
		for e in expressions
	))