#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt >/dev/null 2>&1
pytest -q tests/test_outputs.py
