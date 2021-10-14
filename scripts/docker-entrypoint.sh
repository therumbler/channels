#!/bin/sh
exec pipenv run uvicorn --log-level debug --root-path /api --host 0.0.0.0 main:app

