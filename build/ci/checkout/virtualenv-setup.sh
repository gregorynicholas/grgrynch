#!/usr/bin/env bash


export PATH="$PYENV_ROOT/bin:$PATH";
export REPO_ROOT="$(git rev-parse --show-toplevel)";

#@ see https://github.com/pyenv/pyenv-virtualenv
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv;
git clone https://github.com/yyuu/pyenv-pip-rehash.git $(pyenv root)/plugins/pyenv-pip-rehash;

#@ see https://github.com/jawshooah/pyenv-default-packages
git clone https://github.com/jawshooah/pyenv-default-packages.git $(pyenv root)/plugins/pyenv-default-packages;

pyenv rehash;
eval "$(pyenv init -)";
eval "$(pyenv virtualenv-init -)";
pyenv virtualenv 2.7.11 GRGRYNCH-2.7.11;
pyenv activate GRGRYNCH-2.7.11;
