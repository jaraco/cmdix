from __future__ import print_function

import six


def coerce(item):
	"""
	Always coerce the item to unicode.
	"""
	try:
		return item.__unicode__()
	except Exception:
		return str(item).decode()


def print_coerce(*args, **kwargs):
	args = map(coerce, args)
	return print(*args, **kwargs)


print_text = print if six.PY3 else print_coerce
