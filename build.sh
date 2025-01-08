#!/usr/bin/env bash
set -o errexit

uv install
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate