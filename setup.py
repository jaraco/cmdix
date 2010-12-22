
from distutils.core import setup
import pycoreutils

setup(
    name = "pycoreutils",
    version = pycoreutils.__version__,
    description = "Python port of GNU coreutils",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    license = "MIT",
    url = "http://hanz.nl",
    author = "Hans van Leeuwen",
    author_email = "hanz@hanz.nl",
    py_modules = ["pycoreutils"],
    scripts = ['sh.py'],
)

