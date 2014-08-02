#!/bin/sh
venv=`basename $PWD`
virtualenv -p /usr/bin/python2.7 .venv/$venv
. .venv/${venv}/bin/activate
pip -q install -r requirements.txt
