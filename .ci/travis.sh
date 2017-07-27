#!/bin/bash -x

# Download Conda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

# Install Conda
conda config --set always_yes yes
conda update -q conda
conda info -a
conda create --yes -n py python=$PYTHON_VERSION
source activate py
conda install numpy scipy scikit-learn

# Download training set
python scripts/download_training_set.py
export TRAINING_SET_URI=""

# Download
