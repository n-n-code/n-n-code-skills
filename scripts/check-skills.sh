#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if command -v python3 >/dev/null 2>&1; then
  python_cmd="python3"
elif command -v python >/dev/null 2>&1 &&
  python -c 'import sys; raise SystemExit(0 if sys.version_info.major == 3 else 1)' >/dev/null 2>&1; then
  python_cmd="python"
else
  printf '%s\n' 'check-skills: Python 3 is required for structural validation' >&2
  exit 1
fi

exec "$python_cmd" "$script_dir/check_skills.py"
