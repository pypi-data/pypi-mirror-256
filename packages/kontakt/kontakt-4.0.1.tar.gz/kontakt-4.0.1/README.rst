=======
kontakt
=======

Foundation for adding extensibility to Python packages.

This provides an `Extension` base class and utilities for working with it. To create a new
type of extension, you'll first create a subclass of `Extension`. Then for each type of
your new extension, you'll inherit from your subclass. Finally, you'll register these
types of extension with `setuptools` through *entry points* in your `setup.py`.

See `kontakt.example` for a simple example.