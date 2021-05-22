#!/usr/bin/env bash

# a version string possibly following semantic versioning
# eg 0.5.1, 1.3.2
VERSION_OF_INTEREST=$1

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# TODO dynamically decide on environment name
ENV_NAME="integration-env-5"
ENV_PATH=$MY_DIR/../$ENV_NAME

if [[ "$HOME" ]]; then
  echo "\$HOME variable is already populated.";
else
  HOME=/home/travis
fi


if [[ $(which conda) ]]; then
  echo '------------ CONDA IS ALREADY INSTALLED -------------'
else
  export PATH=$PATH:$HOME/miniconda/bin/
  if [[ $(which conda) ]]; then
    echo '------------ CONDA IS ALREADY INSTALLED -------------'
  else
    echo "CONDA NOT FOUND"
    echo '------------ INSTALLING CONDA -------------'
    chmod +x scripts/install_anaconda.sh
    scripts/install_anaconda.sh
    export CONDA_EXE=$HOME/miniconda/bin/conda
    export PATH=$PATH:$HOME/miniconda/bin/
  fi
fi

set -e
which conda

echo '------------ CREATING ENV -------------'
# TODO check if environment with path ENV_PATH exists in the list of conda environments
# if yes than do not create an environment with the -p flag
# if no use the beloow command
conda create -p "$ENV_PATH" -y python=3.8

printf "\n ---- SOURCING ----\n"
FILE_TO_SOURCE="$HOME/miniconda/etc/profile.d/conda.sh"
if [[ ! -f $FILE_TO_SOURCE ]]; then
  # file does not exist
  # we try our luck with this simple workaround
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
else
  source "$HOME/miniconda/etc/profile.d/conda.sh"
fi

printf "\n ---- HASHING ----\n"
hash -r
printf "\n ---- CONDA CONFIG ----\n"
conda config --set always_yes yes --set changeps1 no
printf "\n ---- CONDA UPDATE ----\n"
conda update -q conda

# Useful for debugging any issues with conda
conda info -a


echo '------------ ACTIVATING ENV -------------'
# TODO check if environment with path ENV_PATH exists in the list of conda environments
# if yes then do 'conda create'
# if no then do 'conda activate $ENV_PATH'
conda activate "$ENV_PATH"
#conda activate

echo '------------ INSTALLING DEPS -------------'
if [[ $(uname -s) == Darwin ]]; then  # we are on macOS
  echo "We are on macOS: skipping apt-get install command"
else  # we assume we are on linux
  sudo apt-get install --yes gcc gfortran python3-dev liblapack-dev cython libblas-dev
fi
#sudo apt-get install --yes python3-scipy
echo '------------ INSTALLING PYTHON DEPS -------------'
python3 -m pip install -U pip
python3 -m pip install -U wheel
conda install somoclu --channel conda-forge

# TODO
# If we install from testpypi then absolutely install the base and dev requirements
# if we are installing from pypi experiment with both options both locally and on ci and then decide on code
python3 -m pip install -r requirements/base.txt
python3 -m pip install -r requirements/dev.txt

echo '------------ INSTALLING SO_MAGIC FROM TEST-PYPI -------------'
# use the --no-deps flag, because test pypi absolutely not guarantees that it can satisfy dependencies by
# looking for the packages in the index, simply because they might not exist

# TODO dynamically decide to use pypi or testpypi
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps so_magic=="$VERSION_OF_INTEREST"
#python -m pip install so_magic==$VERSION_OF_INTEREST

python3 -c 'import so_magic'

echo "Successfully installed the library emnulating the real 'pip install' scenario using the test-pypi server."
python3 -m pip install pytest pytest-cov
python3 -m pytest "$MY_DIR"/../tests -vv --cov
echo "Successfully installed ran the test suite (unit-tests) that are bundled with the distribution (package) against the 'so-magic' library installed in the system"

echo "SUCCESS!!!"
