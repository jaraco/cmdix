from __future__ import unicode_literals

import unittest

from .. import lib
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_showbanner(self):
        lib.showbanner(width=70)


if __name__ == '__main__':
    unittest.main()
