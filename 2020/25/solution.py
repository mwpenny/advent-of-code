#!/usr/bin/python3

def lcg(seed, a=7, m=20201227):
	return (a * seed) % m

def find_loop_size(key):
	value = 1
	loops = 0
	while value != key:
		value = lcg(value)
		loops += 1
	return loops

def gen_key(pub, loops):
	value = 1
	for _ in range(loops):
		value = lcg(value, pub)
	return value


with open('input', 'r') as f:
	card_pub, door_pub = map(int, f.readlines())
	card_loop_size = find_loop_size(card_pub)
	card_priv = gen_key(door_pub, card_loop_size)
	print('Encryption key:', card_priv)