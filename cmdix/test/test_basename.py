from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_basename(self):
        out = self.runcommandline('basename foo/bar/biz')[0]
        assert out == 'biz\n'
