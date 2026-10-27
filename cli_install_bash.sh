#!/usr/bin/env bash

poetry install --no-cache --only main
poetry build
pip install --upgrade dist/env_pass-$(poetry version -s)-py3-none-any.whl --force-reinstall