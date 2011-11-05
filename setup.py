
from distutils.core import setup
import pycoreutils

# Use README.txt + a list of available commands as long_description
long_description = ''.join(open("README.txt").readlines())

setup(
    name = "pycoreutils",
    version = pycoreutils.__version__,
    description = "Coreutils in Pure Python",
    long_description = long_description,
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    license = "MIT",
    url = "http://pypi.python.org/pypi/pycoreutils",
    author = "Hans van Leeuwen",
    author_email = "hansvl@gmail.com",
    scripts = ["scripts/pycoreutils"],
    packages = [
        "pycoreutils",
        "pycoreutils.command",
        "pycoreutils.test"
    ],
)

