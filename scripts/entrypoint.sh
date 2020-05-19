#!/bin/sh

python -m flask db upgrade

exec "$@"