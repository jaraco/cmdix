
from distutils.core import setup
import pycoreutils


setup(
    name = "pycoreutils",
    version = pycoreutils.__version__,
    description = "Python version of GNU coreutils"
    classifiers = [
        "Development Status :: 3 - Alpha",
    ],
    license = "MIT",
    url = "http://hanz.nl",
    author = "Hans van Leeuwen",
    author_email = "hanz@hanz.nl",
    scripts = [
        "pycoreutils",
    ],
    packages = [
        "pycoreutils",
    ],
)

