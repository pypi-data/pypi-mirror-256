"Tests using the example extensions we registered in setup.py."

import kontakt
import kontakt.examples.extension

from helpers import EXTENSION_TYPES, EXTENSION_NAMESPACE


def test_list_extensions():
    actual = sorted(kontakt.list_extensions(EXTENSION_NAMESPACE))
    expected = sorted(EXTENSION_TYPES)
    assert actual == expected
