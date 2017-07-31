#!/bin/bash -x

# Download and install miniconda
sudo apt-get update
if [[ "$TRAVIS_PYTHON_VERSION" == "2.7" ]]; then
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
else
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda install numpy scipy astropy scikit-learn pandas
conda info -a
# Clone master into 'tmp' and copy the scoring and base scripts
git clone https://github.com/GOTO-OBS/goto-vegas.git tmp
cp tmp/score.py score.py
#cp tmp/classifier/base.py classifier/base.py
