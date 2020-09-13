#!/usr/bin/env bash

set -e

python_version=$(python -c 'import sys; print(".".join(str(_) for _ in sys.version_info[:2]))')

if [[ $python_version == "2.7" ]]; then
  echo "Using legacy Python 2.7";
  MINICONDA_VERSION=2;
else
  echo "Not Python 2.7, so should be Python 3";
  MINICONDA_VERSION=3;
fi

echo "MINICONDA version: $MINICONDA_VERSION"

wget https://repo.continuum.io/miniconda/Miniconda$MINICONDA_VERSION-latest-Linux-x86_64.sh -O miniconda.sh;

printf "\n ---- RUNNING mioniconda.sh ----\n"

# shellcheck disable=SC2116
if [[ $(echo "$HOME") ]]; then
  echo "\$HOME variable is populated, so probably we are running on a 'local' machine";
else
  HOME=/home/travis
  echo "Assuming we are running on travis CI; setting variable HOME=$HOME"
fi

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
