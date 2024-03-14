#!/usr/bin/env bash

black ./src --check
if [[ $? -ne 0 ]]; then
    exit 1
fi

mypy ./src
if [[ $? -ne 0 ]]; then
    exit 1
fi

flake8 ./src
if [[ $? -ne 0 ]]; then
    exit 1
fi
