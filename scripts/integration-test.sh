#!/usr/bin/env bash

VERSION_OF_INTEREST=$1

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ENV_NAME="integration-env"
ENV_PATH=$MY_DIR/../$ENV_NAME

if [[ $(echo "$HOME") ]]; then
  echo "\$HOME variable is already populated.";
else
  HOME=/home/travis
fi

which conda
if [[ $? != 0 ]]; then
  export PATH=$PATH:$HOME/miniconda/bin/
  which conda
  if [[ $? != 0 ]]; then
    echo "CONDA NOT FOUND"
    echo '------------ INSTALLING CONDA -------------'
    chmod +x scripts/install_anaconda.sh
    scripts/install_anaconda.sh
    export CONDA_EXE=$HOME/miniconda/bin/conda
    export PATH=$PATH:$HOME/miniconda/bin/
  else
    echo '------------ CONDA IS ALREADY INSTALLED -------------'
  fi
else
  echo '------------ CONDA IS ALREADY INSTALLED -------------'
fi

set -e
which conda

echo '------------ CREATING ENV -------------'
conda create -p $ENV_PATH -y python=3.7

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
conda activate $ENV_PATH

echo '------------ INSTALLING DEPS -------------'
if [[ $(uname -s) == Darwin ]]; then  # we are on macOS
  echo "We are on macOS: skipping apt-get install command"
else  # we assume we are on linux
  sudo apt-get install --yes gcc gfortran python-dev liblapack-dev cython libblas-dev
fi
#sudo apt-get install --yes python3-scipy
echo '------------ INSTALLING PYTHON DEPS -------------'
python -m pip install -U pip
python -m pip install -U wheel
conda install somoclu --channel conda-forge
python -m pip install -r requirements/base.txt
python -m pip install -r requirements/dev.txt
echo '------------ INSTALLING SO_MAGIC FROM TEST-PYPI -------------'
# use the --no-deps flag, because test pypi absolutely not guarantees that it can satisfy dependencies by
# looking for the packages in the index, simply because they might not exist
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps so_magic==$VERSION_OF_INTEREST

python -c 'import so_magic'

echo "Successfully installed the library emnulating the real 'pip install' scenario using the test-pypi server."

python -m pytest $MY_DIR/../tests -vv --cov
echo "Successfully installed ran the test suite (unit-tests) that are bundled with the distribution (package) against the 'so-magic' library installed in the system"

echo "SUCCESS!!!"