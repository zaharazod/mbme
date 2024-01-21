from unittest import TestCase, main
from awa.util import (
    AttrDict,
    DottedAttrDict,
    MissingAttrDict,
    EphemeralAttrDict,
    EphemeralChain,
    FalseChain,
    ConfigFile,
    FALSE,
)

class TestAttrDict(TestCase):
    def test_thing(self):
        self.assertEqual(1, 1, 'test')


if __name__ == '__main__':
    main()
