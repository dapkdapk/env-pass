#!/bin/bash

poetry install
poetry run black .
poetry run isort .
poetry run pytest
poetry build
poetry config pypi-token.pypi $PYPI_TOKEN
poetry publish --build
