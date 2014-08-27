#!/bin/bash
VENV_BASE=${VENV_BASE:-.venv}
VENV_NAME=$(basename $PWD)
VENV_DIR=${VENV_BASE}/${VENV_NAME}
virtualenv -p /usr/bin/python2.7 $VENV_DIR
. $VENV_DIR/bin/activate
if [ -r /etc/mam_proxy.sh ]
then
    . /etc/mam_proxy.sh
    export http_proxy=$ui_http_proxy
    export https_proxy=$ui_http_proxy
    pip install -r requirements.txt
else
    pip install -r requirements.txt
fi
