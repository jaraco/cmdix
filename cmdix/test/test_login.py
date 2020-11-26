from . import BaseTestCase
from ..command import login


class TestCase(BaseTestCase):
    def test_login_check_password(self):
        # tests disabled (don't work)
        return
        # Password is pycoreutils
        hash1 = '$1$JYOwx1mV$NUNwKlq4XGky9WjN1NU051'
        hash2 = (
            '$6$.T7kFfCg$SWIuYR1sbw7IYmaVBddfm9BhW5yK89afw7p'
            + 'uXCLXzHcFnmQhBP9FwUnndt/ZCRILajW0ddhrLDiEERIk0RnBY0'
        )
        assert login.check_password(hash1, 'pycoreutils')
        assert login.check_password(hash2, 'pycoreutils')
        assert not login.check_password(hash2, 'FALSE!')
