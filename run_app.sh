#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  python3 launch_voice_memo.py
elif command -v python >/dev/null 2>&1; then
  python launch_voice_memo.py
else
  echo "Python 3 is required but was not found."
  exit 1
fi
