#!/usr/bin/python3

import re

PASSPORT_REGEX = re.compile(r'(\S+):(\S+)')

HEIGHT_REGEX = re.compile(r'(((15|16|17|18)[0-9]|19[0-3])cm)|((59|6[0-9]|7[0-6])in)')
HAIR_COLOR_REGEX = re.compile(r'#[0-9a-f]{6}')
VALID_EYE_COLORS = set(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])

PASSPORT_VALIDATORS = {
	'byr': lambda val: val.isdigit() and 1920 <= int(val) <= 2002,
	'iyr': lambda val: val.isdigit() and 2010 <= int(val) <= 2020,
	'eyr': lambda val: val.isdigit() and 2020 <= int(val) <= 2030,
	'hgt': lambda val: HEIGHT_REGEX.match(val) is not None,
	'hcl': lambda val: HAIR_COLOR_REGEX.match(val) is not None,
	'ecl': lambda val: val in VALID_EYE_COLORS,
	'pid': lambda val: val.isdigit() and len(val) == 9
}

def is_valid(passport, extended_validation):
	required_keys = PASSPORT_VALIDATORS.keys()
	if set(passport.keys()).intersection(required_keys) != required_keys:
		return False

	if extended_validation:
		for key in required_keys:
			if not PASSPORT_VALIDATORS[key](passport[key]):
				return False
	return True


with open('input', 'r') as f:
	passport_strs = f.read().split('\n\n')
	passports = list(map(lambda s: dict(PASSPORT_REGEX.findall(s)), passport_strs))

	# Part 1
	valid_passports = [p for p in passports if is_valid(p, False)]
	print('Valid passports:', len(valid_passports))

	# Part 2
	valid_passports_extended = [p for p in passports if is_valid(p, True)]
	print('Valid passports (extended validation):', len(valid_passports_extended))