#!/usr/bin/env bash
# Creates venv, installs requirements (fast path), and runs the fraud checker
set -e
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR/fraud"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# run the checker with provided image path from caller
if [ -z "$1" ]; then
  echo "Usage: ./run_setup_and_check.sh path/to/image.jpg"
  exit 1
fi
python run_fraud.py "$1"
