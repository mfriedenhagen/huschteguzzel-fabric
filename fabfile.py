# vim: fileencoding=utf-8

__author__ = 'mirko'

import logging
import subprocess

import nose
from fabric.api import *
import jenkins_support
import hooks

require("jenkins_shell_user", used_for="accessing the host with sudo-rights.")
env.hosts = ["huschteguzzel.de"]
env.user = env.jenkins_shell_user

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger("dicttoxml").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("paramiko").setLevel(logging.WARNING)


def revision():
    if revision.rev is None:
        revision.rev = subprocess.check_output(("git", "rev-parse", "--short", "--porcelain", "HEAD")).strip()
    return revision.rev
revision.rev = None

def loggit(phase):
    rev = revision()
    def f():
        logging.info("%s: '%s' on '%s' (%s)", phase, env.command, env.host, rev)
    return f
myhook = hooks.add_hooks(pre=loggit("pre"), post=loggit("post"))


@task
@myhook
def apt_get_update():
    """
    apt-get update -qq
    """
    run("sudo /usr/bin/apt-get update -q")


@task
@myhook
def apt_get_upgrade():
    """
    apt-get upgrade -q -y
    """
    run("sudo /usr/bin/apt-get upgrade -q -y")


@task
@myhook
def upgrade():
    """
    apt-get -q update && apt-get -q -y upgrade
    """
    execute(apt_get_update)
    execute(apt_get_upgrade)


@task
@myhook
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
