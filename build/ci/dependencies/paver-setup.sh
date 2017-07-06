#!/usr/bin/env bash


export PATH="$PYENV_ROOT/bin:$PATH";
export REPO_ROOT="$(git rev-parse --show-toplevel)";

pyenv exec pip install pip --upgrade --quiet;
pyenv exec pip install --disable-pip-version-check --verbose -r $REPO_ROOT/build/pip-paver-deps.txt;
pyenv exec pip install --disable-pip-version-check --verbose -r $REPO_ROOT/build/pip-paver.txt;
pyenv rehash;
