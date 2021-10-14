#!/bin/sh
exec pipenv run uvicorn \
    --log-level info \
    --root-path /api \
    --host 0.0.0.0 \
    --loop uvloop \
    main:app

