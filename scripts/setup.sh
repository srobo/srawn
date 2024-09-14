#!/usr/bin/env bash

set -e

python3 -m venv venv

venv/bin/pip install -r requirements.txt

yarn install
