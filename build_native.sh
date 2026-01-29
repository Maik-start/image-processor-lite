#!/usr/bin/env bash
set -euo pipefail
PYTHON=${1:-"$(which python3)"}
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR/imgprocessor/visual_analysis"
"$PYTHON" setup_native.py build_ext --inplace
echo "Built native extension in $(pwd)" 
