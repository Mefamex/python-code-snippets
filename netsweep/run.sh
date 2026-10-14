#!/usr/bin/env bash
# netsweep quick launcher.
# Usage:  ./run.sh [options]   (options are passed to main.py)
cd "$(dirname "$0")" || exit 1
exec python3 main.py "$@"
