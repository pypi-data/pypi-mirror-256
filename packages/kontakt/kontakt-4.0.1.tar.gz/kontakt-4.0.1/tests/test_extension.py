from pathlib import Path

import kontakt
from kontakt.examples.extension import ExampleExtension, ExampleExtensionError

from helpers import EXTENSION_NAMESPACE

# TODO: Many of these tests would work for configurable extensions as well. Should we include them?


def test_kind_attribute(extension_type):
    name, extension_type = extension_type

    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        ExampleExtensionError,
        "flavor",
        42,
    )

    assert extension.kind() == ExampleExtension.kind()


def test_name_attribute(extension_type):
    name, extension_type = extension_type

    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        ExampleExtensionError,
        "flavor",
        42,
    )

    assert extension.name == name


def test_dirpath_attribute(extension_type):
    name, extension_type = extension_type

    assert Path(extension_type.dirpath()).resolve() == (Path(kontakt.__file__).parent / "examples").resolve()


def test_version_property(extension_type):
    name, extension_type = extension_type

    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        ExampleExtensionError,
        "flavor",
        42,
    )

    assert extension.version() == "1.0.0"


def test_description_defaults_to_class_name_without_docstring():
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        "blue",
        ExampleExtensionError,
        "blueberry",
        42,
    )

    actual = extension.describe()

    expected = kontakt.examples.extension.Blue.__name__

    assert actual == expected


def test_description_defaults_to_docstring_if_available():
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        "red",
        ExampleExtensionError,
        "raspberry",
        42,
    )

    actual = extension.describe()

    expected = kontakt.examples.extension.Red.__doc__

    assert actual == expected


def test_extensions_can_override_description():
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        "green",
        ExampleExtensionError,
        "apple",
        42,
    )

    actual = extension.describe()

    expected = kontakt.examples.extension.Green("apple", 42, "green").describe()

    assert actual == expected
