c2c.recipe.pkgversions
======================

Recipe used to test the Debian package requirement.

Example of use::

    [buildout]
    parts = ...
        pkgversions
        ...

    [pkgversions]
    recipe = c2c.recipe.facts
    mapserver-bin = 6.0.3
    libproj0 = 4.8

This example tests that we have at least the version 6.0.3 of mapserver,
and the version 4.8 of proj.
