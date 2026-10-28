#!/bin/bash

poetry install
poetry run black .
poetry run isort .
poetry run pytest
poetry build
