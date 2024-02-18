from pathlib import Path

import kontakt

from helpers import EXTENSION_TYPES, EXTENSION_NAMESPACE


def test_list_dirpaths():
    actual = kontakt.list_dirpaths(EXTENSION_NAMESPACE)
    expected = {name: Path(kontakt.__file__).parent.resolve() for name in EXTENSION_TYPES}
    assert actual == expected
