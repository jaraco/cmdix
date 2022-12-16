from cmdix import lib
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_showbanner(self):
        lib.showbanner(width=70)
