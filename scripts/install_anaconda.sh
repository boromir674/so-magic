#!/usr/bin/env bash

set -e

if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
else
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi

printf "\n ---- RUNNING mioniconda.sh ----\n"

HOME=/home/travis
bash miniconda.sh -b -p "$HOME/miniconda"

printf "\n ---- SOURCING ----\n"
source "$HOME/miniconda/etc/profile.d/conda.sh"

printf "\n ---- HASHING ----\n"
hash -r
printf "\n ---- CONDA CONFIG ----\n"
conda config --set always_yes yes --set changeps1 no
conda update -q conda

# Useful for debugging any issues with conda
conda info -a
