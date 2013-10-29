c2c.recipe.pkgversions
======================

Recipe used to test the Debian package requirement.

This recipe requires that dpkg is in the path.

Example of use::

    [buildout]
    parts = ...
        pkgversions
        ...

    [pkgversions]
    recipe = c2c.recipe.pkgversions
    mapserver-bin = 6.0.3
    libproj0 = 4.8

This example tests that we have at least the version 6.0.3 of mapserver,
and the version 4.8 of proj.

No version mean no-test.

To just test that the package is installed use the version
``dev`` (minimal version) or ``installed`` (alias).

It the version is set to ``not-installed`` mean that
we want that the package isn't installed.
