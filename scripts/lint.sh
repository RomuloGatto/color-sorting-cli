#! /bin/bash

./venv/bin/pip install mypy pylint flake8 black isort --upgrade
./venv/bin/mypy harmony --show-error-codes || exit
./venv/bin/pylint harmony || exit
./venv/bin/ruff harmony tests || exit
./venv/bin/black harmony tests --check || exit
./venv/bin/isort harmony tests --check-only --profile black || exit