#!/bin/sh

# Reformat the code into the correct style
black .

# Check the code for obvious errors/style 
# violations
flake8

# Check the documentation for sanity and conformance
# to the house style
docformatter --in-place --config ./pyproject.toml .

