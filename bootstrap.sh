#!/bin/bash
set -e

deactivate || echo "not yet activate"

python3 -m venv ./env
source env/bin/activate

python3 -m pip install -r requirements.txt
