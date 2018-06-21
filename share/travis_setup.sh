#!/bin/bash
set -evx

mkdir ~/.rapidcore

# safety check
if [ ! -f ~/.rapidcore/.rapid.conf ]; then
  cp share/rapid.conf.example ~/.rapidcore/rapid.conf
fi
