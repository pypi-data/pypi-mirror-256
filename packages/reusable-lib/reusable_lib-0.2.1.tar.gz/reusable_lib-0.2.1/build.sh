#!/bin/bash
#
rm -rf dist
mkdir dist
python -m build
ls dist -l
python3 -m twine upload dist/*
