#!/bin/sh
echo "removing files ..."


exec pipenv run uvicorn --host 0.0.0.0 main:app