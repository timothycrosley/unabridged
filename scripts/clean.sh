#!/bin/bash
set -euxo pipefail

poetry run isort unabridged/ tests/
poetry run black unabridged/ tests/
