# Releases

All releases should be on [PyPi](https://pypi.org/project/lbutils-mp/), and also published on [GitHub](https://github.com/dlove24/lbutils). A full log of the changes can be found in the source, or on GitHub: what follows is a summary of key features/changes.

## 2023-04-16: lbutils 0.2.5

### New

* Added package and class structure diagrams to the
documentation to make navigating the code easier.
* Added additional checks to ensure more consistency
in the documentation.

### Changed

* Updated the type signature of the library methods to make
static type checking easier. Also added `mypy` to the commit 
hook to enforce type checking, and updated the documentation
to reflect the types of the module attributes in use more
consistently.

## 2023-04-16: lbutils 0.2.4

### New

* Add a user `origin` to the `Canvas` library, which is assumed to be under the users control. This
makes it easier for the user to specify a 'drawing origin' for the drawing primitives
* The `Pixel` class now has an `offset` for Cartesian co-ordinate offsets, and a `offset_polar` for Polar
co-ordinate offsets. With the changes to the drawing primitives, this should make it easier to make
small changes between calls to drawing primitives.

### Changed

* Changed the API of the drawing primitives to allow the user to either use the internal `cursor` by default: or to use an ad-hoc `start` co-ordinate.
* Removed the use of Boolean flags in the API, to make the intent of the API clearer to readers of the code. 
This is now also checked by `ruff` and enforced on code commit.

## 2023-04-14: lbutils 0.2.3

### Changed

* Re-organise the `Canvas` library to use the internal `cursor` for the text routines. This makes the
management of the writing routines the responsibility of the `Canvas` itself, and not the user
of the `Canvas` (preserving encapsulation).
* Directly expose the `cursor` attributes as a helper for `Canvas` to make the movement of the
`cursor` a little easier.

## 2023-04-14: lbutils 0.2.2

### Changed

* Use the new graphics API for the OLEDrgb pmod example

## 2023-04-14: lbutils 0.2.1

### Changed

* Link I2C driver infrastructure to the build

## 2023-04-14: lbutils 0.2.0

### New

* Rewritten graphics API, with support for abstract drawing and fonts
* Pmod library for support of the Diligent OLEDrgb pmod, using the new graphics library
* Helper libraries for network set-up on the Pico W
* Support libraries for font, pixel and colours

### Changed

* Move to Read The Docs as the offical documentation repository
* Use 'mkdocs' to build the documentation for the library
* Move to using 'ruff' instead of 'flake8' as the lint and code sanity checker.

## 2023-03-29: lbutils 0.1.1

### New

- Decimal and hexadecimal display drivers for a seven segment display

## Pre-Release: lbutils 0.1.2

### Changed

- Documentation moved from `pdoc3` back to `pdoc` as the offical generator
