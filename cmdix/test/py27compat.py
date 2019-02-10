import os

import six


def _mkdir(name, mode=None):
	args = (name,) if mode is None else (name, mode)
	return os.mkdir(*args)


mkdir = os.mkdir if six.PY3 else _mkdir
