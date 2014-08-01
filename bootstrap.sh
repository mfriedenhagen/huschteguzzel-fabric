#!/bin/sh
venv=huschteguzzel-fabric
virtualenv -p /usr/bin/python2.7 .venv/$venv
. .venv/${venv}/bin/activate
pip -q install -r requirements.txt
