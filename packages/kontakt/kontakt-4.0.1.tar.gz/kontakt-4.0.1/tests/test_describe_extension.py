"Tests using the example extensions we registered in setup.py."

import kontakt
import kontakt.examples.extension
import pytest

from helpers import EXTENSION_NAMESPACE


def test_raises_correct_exception_when_no_extension_exists():
    with pytest.raises(kontakt.examples.extension.ExampleExtensionError):
        kontakt.describe_extension(
            namespace=EXTENSION_NAMESPACE,
            name="no-such-extension",
            exception_type=kontakt.examples.extension.ExampleExtensionError,
        )


def test_description_defaults_to_class_name_without_docstring():
    actual = kontakt.describe_extension(
        EXTENSION_NAMESPACE,
        "blue",
        kontakt.examples.extension.ExampleExtensionError,
    )

    expected = kontakt.examples.extension.Blue.__name__

    assert actual == expected


def test_description_defaults_to_docstring_if_available():
    actual = kontakt.describe_extension(
        EXTENSION_NAMESPACE,
        "red",
        kontakt.examples.extension.ExampleExtensionError,
    )

    expected = kontakt.examples.extension.Red.__doc__

    assert actual == expected


def test_extensions_can_override_description():
    actual = kontakt.describe_extension(
        EXTENSION_NAMESPACE,
        "green",
        kontakt.examples.extension.ExampleExtensionError,
    )

    expected = kontakt.examples.extension.Green.describe()

    assert actual == expected
