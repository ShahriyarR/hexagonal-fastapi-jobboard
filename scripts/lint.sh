#!/usr/bin/env bash

set -e
set -x

flake8 src
black src tests --check --diff
isort src tests --check --diff