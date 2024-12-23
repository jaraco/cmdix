import os
import pathlib
import sys


def walk_py311(path):
    for dirpath, dirnames, filenames in os.walk(path):
        yield pathlib.Path(dirpath), dirnames, filenames


def walk_py312(path):
    return path.walk()


walk = walk_py311 if sys.version_info < (3, 12) else walk_py312
