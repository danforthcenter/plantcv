#!/usr/bin/env bash

set -e

source scripts/common.sh
HERE_DIR="$(get_realpath $(dirname $(dirname "$0")))"

echo "------------------------------- PlantCV Env Setup -------------------------------"

VENV_PATH=$HERE_DIR/venv
if [ ! -d "$VENV_PATH" ]; then
  os_type=`uname -s`
  if [ "Darwin" = "$os_type" ]; then
    install_dependencies_darwin
  else
    install_dependencies_linux
  fi

  virtualenv --python=python2.7 $VENV_PATH

  if [ "Darwin" = "$os_type" ]; then
    echo "Only MacPorts for now. Need TODO on Brew"
    echo 'export PYTHONPATH=/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages' >> $VENV_PATH/bin/activate
  else
    echo 'export PYTHONPATH=/usr/lib/python2.7/dist-packages' >> $VENV_PATH/bin/activate
  fi
  
  source $VENV_PATH/bin/activate
  pushd $HERE_DIR
  pip install -r requirements.txt
  python setup.py install
  echo -n "Installation test..."
  python -c 'import plantcv'
  echo 'ok'
  deactivate
  popd
  
  echo "Installation complete."
else
  echo "Apparently already installed (Venv in $VENV_PATH)"
fi
echo
echo "Usage:"
echo "cd $HERE_DIR"
echo "source $VENV_PATH/bin/activate"
echo "python"
echo ">>> import plantcv"
echo
