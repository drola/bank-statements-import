import unittest

from freezegun import freeze_time

from dh2ofx import dh2ofx
from fixtures import delavska_hranilnica_transactions_export, test_dh2ofx_ofx


class DH2OFXTestCase(unittest.TestCase):
    @freeze_time('2022-12-27T10:43:23.361564', tz_offset=0)
    def test_dh2ofx(self):
        with open(test_dh2ofx_ofx, 'rt') as f:
            self.assertEqual(f.read(),
                             dh2ofx(delavska_hranilnica_transactions_export))


if __name__ == '__main__':
    unittest.main()
