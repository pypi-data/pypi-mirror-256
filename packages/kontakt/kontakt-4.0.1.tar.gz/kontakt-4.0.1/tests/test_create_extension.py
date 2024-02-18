"Tests using the example extensions we registered in setup.py."

import kontakt
import kontakt.examples.extension
import pytest

from helpers import EXTENSION_NAMESPACE


def test_raises_correct_exception_when_no_extension_exists():
    with pytest.raises(kontakt.examples.extension.ExampleExtensionError):
        kontakt.create_extension(
            namespace=EXTENSION_NAMESPACE,
            name="no-such-extension",
            exception_type=kontakt.examples.extension.ExampleExtensionError,
        )


def test_creates_correct_type_of_extension(extension_type):
    name, extension_type = extension_type

    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        kontakt.examples.extension.ExampleExtensionError,
        "flavor",
        42,
    )

    assert isinstance(extension, extension_type)


def test_forwards_positional_arguments(extension_type):
    name, extension_type = extension_type
    flavor = f"{name} flavored"
    size = 42
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        kontakt.examples.extension.ExampleExtensionError,
        flavor,
        size,
    )

    assert extension.flavor == flavor
    assert extension.size == size


def test_forwards_keyword_arguments(extension_type):
    name, extension_type = extension_type
    flavor = f"{name} flavored"
    size = 42
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        kontakt.examples.extension.ExampleExtensionError,
        flavor=flavor,
        size=size,
    )

    assert extension.flavor == flavor
    assert extension.size == size


def test_forwards_mixed_positional_and_keyword_arguments(extension_type):
    name, extension_type = extension_type
    flavor = f"{name} flavored"
    size = 42
    extension = kontakt.create_extension(
        EXTENSION_NAMESPACE,
        name,
        kontakt.examples.extension.ExampleExtensionError,
        flavor,
        size=size,
    )

    assert extension.flavor == flavor
    assert extension.size == size


def test_raises_type_error_when_passed_unknown_keyword_argument(extension_type):
    name, extension_type = extension_type
    with pytest.raises(TypeError):
        kontakt.create_extension(
            EXTENSION_NAMESPACE,
            name,
            kontakt.examples.extension.ExampleExtensionError,
            "raspberry",
            azimuth=123,
        )


def test_raises_type_error_when_passed_too_many_positional_arguments(extension_type):
    name, extension_type = extension_type
    with pytest.raises(TypeError):
        kontakt.create_extension(
            EXTENSION_NAMESPACE,
            name,
            kontakt.examples.extension.ExampleExtensionError,
            "raspberry",
            123,
            "kromulent",
        )


def test_raises_type_error_when_passed_too_few_positional_arguments(extension_type):
    name, extension_type = extension_type
    with pytest.raises(TypeError):
        kontakt.create_extension(
            EXTENSION_NAMESPACE,
            name,
            kontakt.examples.extension.ExampleExtensionError,
            "raspberry",
        )
