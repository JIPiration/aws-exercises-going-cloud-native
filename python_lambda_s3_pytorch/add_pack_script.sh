#!/bin/bash

install_packages () {
  pip install -r /host/requirements.txt
}

gather_pack () {
  cd /home
  rm -rf lambdapack
  mkdir lambdapack
  cd lambdapack

  # Copy python pakages from virtual enviroment
}

