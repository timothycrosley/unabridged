#!/bin/bash
set -euxo pipefail

poetry run uvicorn unabridged.http:app
