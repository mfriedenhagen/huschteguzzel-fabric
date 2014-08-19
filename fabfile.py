# vim: fileencoding=utf-8

__author__ = 'mirko'

import logging

import nose
from fabric.api import *
import jenkins_support

require("jenkins_shell_user", used_for="accessing the host with sudo-rights.")
env.hosts = ["huschteguzzel.de"]
env.user = env.jenkins_shell_user

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger("dicttoxml").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)

@task
def apt_get_update():
    """
    apt-get -q update
    """
    sudo("apt-get -q update")


@task
def apt_get_upgrade():
    """
    apt-get -q -y upgrade
    """
    sudo("apt-get -q -y upgrade")


@task
def upgrade():
    """
    apt-get -q update && apt-get -q -y upgrade
    """
    execute(apt_get_update)
    execute(apt_get_upgrade)


@task
def test(args=None):
    """
    Run all unit tests and doctests.

    Specify string argument ``args`` for additional args to ``nosetests``.
    """
    # Default to explicitly targeting the 'tests' folder, but only if nothing
    # is being overridden.
    tests = "" if args else " tests"
    default_args = "-sv --with-doctest --nologcapture --with-xunit %s" % tests
    default_args += (" " + args) if args else ""
    nose.core.run_exit(argv=[''] + default_args.split())
