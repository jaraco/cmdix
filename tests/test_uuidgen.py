from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_uuidgen(self):
        # Make sure uuid1() generates UUIDs that are actually version 1.
        for uuid in [self.runcommandline('uuidgen')[0] for i in range(10)]:
            ell = uuid.rstrip().split('-')

            # Check uuid-length
            assert len(uuid) == 37

            # Check if uuid ends with \n
            assert uuid.endswith('\n')

            # Check split
            assert len(ell) == 5

            # Check if every character is hex
            for x in ell:
                for c in x:
                    assert 0 <= int(c, 16) <= 15
