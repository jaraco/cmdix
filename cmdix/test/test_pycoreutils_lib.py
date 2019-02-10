from __future__ import unicode_literals

from .. import lib
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_showbanner(self):
        lib.showbanner(width=70)
