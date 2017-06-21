#!/usr/bin/env bash

function check_available() {
  local name="$1"
  local command="$2"
  echo -n "$name..."
  $($command 2&> /dev/null)
  echo "ok"
}

function check_file_or_die() {
  if [ ! -f "$1" ]; then
    echo "File not found: $1"
    echo "Cannot continue :-("
    exit 1
  fi
}

function get_realpath() {
  if [ "$(uname -s)" == "Darwin" ]; then
    local queue="$1"
    if [[ "${queue}" != /* ]] ; then
      # Make sure we start with an absolute path.
      queue="${PWD}/${queue}"
    fi
    local current=""
    while [ -n "${queue}" ]; do
      # Removing a trailing /.
      queue="${queue#/}"
      # Pull the first path segment off of queue.
      local segment="${queue%%/*}"
      # If this is the last segment.
      if [[ "${queue}" != */* ]] ; then
        segment="${queue}"
        queue=""
      else
        # Remove that first segment.
        queue="${queue#*/}"
      fi
      local link="${current}/${segment}"
      if [ -h "${link}" ] ; then
        link="$(readlink "${link}")"
        queue="${link}/${queue}"
        if [[ "${link}" == /* ]] ; then
          current=""
        fi
      else
        current="${link}"
      fi
    done
    echo "${current}"
  else
    readlink -f "$1"
  fi
}

function install_dependencies_darwin() {
  if [ -x '/opt/local/bin/port' ]; then
    echo "Getting dependencies with MacPorts."
    sudo port install git sqlite3 opencv +python27 py27-virtualenv
  elif [ -x '/usr/local/bin/brew' ]; then
    echo "Getting dependencies with Brew."
    echo "Todo"
  else
    echo "Could not find MacPorts or Brew in standard locations, aborting."
  fi
}

function install_dependencies_linux() {
  if [ -x '/usr/bin/apt' ]; then
    echo "Getting dependencies with Apt."
    sudo apt-get install git libopencv-dev python-opencv \
      sqlite3 python-setuptools libpython2.7-dev python-pip virtualenv
  elif [ -x '/usr/bin/yum' ]; then
    echo "Getting dependencies with Yum."
    sudo yum install git libopencv-dev python-opencv sqlite3 \
      python-setuptools libpython2.7-dev python-pip virtualenv
  else
    echo "Could not find Apt or Yum in standard locations, aborting."
  fi
}
