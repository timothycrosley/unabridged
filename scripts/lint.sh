#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports unabridged/
poetry run isort --check --diff unabridged/ tests/
poetry run black --check unabridged/ tests/
poetry run flake8 unabridged/ tests/
poetry run safety check
poetry run bandit -r unabridged/
