# Running The Test Scripts For Checking the Library Functionality

!!! info "What you will need"

    * Pico H or Pico W running the Test Server
    * Windows or Linux PC

## Overview

This library contains a number of tests, designed to be run under the [PyTest](https://docs.pytest.org/en/7.2.x/contents.html) harness. Some tests also require the [requests](https://requests.readthedocs.io/en/latest) library to be installed, and will also require network access.

All tests should follow the standard PyTest rules for test discovery so that running

```
$ py.test
```

will run all tests.

Each test is standalone, so that running

```
$ py.test simple_get.py
```

inside the `tests` folder should run the desired tests. Specific tests can also be run programmaticaly through this module. Consult the PyTest documentation for details.

## Running the Tests

!!! Note "Check the Test Assumptions"

    These tests assume the Pico H/W is running on the standard Leeds Beckett micro-controller development board. In some cases the tests will work on a bare Pico H/W: or an alternative

