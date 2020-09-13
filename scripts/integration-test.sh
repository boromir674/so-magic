#!/usr/bin/env bash


MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ENV_NAME="integration-env"
ENV_PATH=$MY_DIR/../$ENV_NAME

which conda
if [[ $? != 0 ]]; then
  export PATH=$PATH:$CONDA_EXE
  which conda
  if [[ $? != 0 ]]; then
    echo "CONDA NOT FOUND"
    echo '------------ INSTALLING CONDA -------------'
    chmod +x scripts/install_anaconda.sh
    scripts/install_anaconda.sh
    if [[ $(echo "$HOME") ]]; then
      echo "\$HOME variable is populated, so probably we are running on a 'local' machine";
    else
      HOME=/home/travis
      echo "Assuming we are running on travis CI; setting variable HOME=$HOME"
    fi
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
conda create -p $ENV_PATH -y
echo '------------ ACTIVATING ENV -------------'
conda activate $ENV_PATH

echo '------------ INSTALLING PYTHON DEPS -------------'
python -m pip install -U pip
python -m pip install -U wheel
python -m pip install -r requirements/base.txt
python -m pip install -r requirements/dev.txt

echo '------------ INSTALLING SO_MAGIC FROM TEST-PYPI -------------'
# use this command because test pypi absolutely not guarantees that it can satsify dependencies (--no-deps flag) by
# looking for the packages in the index, simply because they might not exist
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps so_magic

echo "SUCCESS!!!"
echo "Successfully installed the library emnulating the real 'pip install' scenario using the test-pypi server."
