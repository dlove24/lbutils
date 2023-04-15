# Releases

All releases should be on [PyPi](https://pypi.org/project/lbutils-mp/), and also published on [GitHub](https://github.com/dlove24/lbutils). A full log of the changes can be found in the source, or on GitHub: what follows is a summary of key features/changes.

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
