from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_base64_decode(self, capsys):
        self.createfile('foo', content='SGF2ZSBhIGxvdCBvZiBmdW4uLi4K')
        self.runcommandline('base64 -d foo')
        assert capsys.readouterr().out == 'Have a lot of fun...\n'

    def test_base64_encode(self, capsys):
        self.createfile('foo', size=50)
        self.runcommandline('base64 -w 30 foo')
        expected = (
            'MDAwMDAwMDAwMDAwMDAwMDAwMDAwMD\n'
            'AwMDAwMDAwMDAwMDAwMDAwMDAwMDAw\n'
            'MDAwMDA=\n'
        )
        assert capsys.readouterr().out == expected
