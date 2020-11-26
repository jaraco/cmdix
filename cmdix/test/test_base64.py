from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_base64_decode(self):
        self.createfile('foo', content='SGF2ZSBhIGxvdCBvZiBmdW4uLi4K')
        output = self.runcommandline('base64 -d foo')[0]
        assert output == 'Have a lot of fun...\n'

    def test_base64_encode(self):
        self.createfile('foo', size=50)
        output = self.runcommandline('base64 -w 30 foo')[0]
        expected = (
            'MDAwMDAwMDAwMDAwMDAwMDAwMDAwMD\n'
            'AwMDAwMDAwMDAwMDAwMDAwMDAwMDAw\n'
            'MDAwMDA=\n'
        )
        assert output == expected
