import kontakt
from kontakt.config_options import Option, build_default_config
from kontakt.examples.configurable_extension import (Printer,
                                                     RendererExtensionError)

from helpers import CONFIGURABLE_EXTENSION_NAMESPACE


def test_config_options():
    extension = kontakt.create_extension(
        CONFIGURABLE_EXTENSION_NAMESPACE,
        "printer",
        RendererExtensionError,
    )

    actual = list(extension.config_options())
    expected = [Option(("font", "size"), "Font size", 42), Option(("font", "family"), "Font family", "serif")]
    assert actual == expected


def test_construct_object():
    extension = kontakt.create_extension(
        CONFIGURABLE_EXTENSION_NAMESPACE,
        "printer",
        RendererExtensionError,
    )

    config = build_default_config(extension.config_options())

    actual = extension.construct(config, model="PrinterCo")
    expected = Printer(font_size=42, font_family="serif", model="PrinterCo")
    assert actual == expected
