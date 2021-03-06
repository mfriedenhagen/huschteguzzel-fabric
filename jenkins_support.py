# vim: fileencoding=utf-8
import json
import logging

from items import jenkins
from fabric.decorators import task
from fabric.operations import require, sudo, run
from fabric.state import env
from fabric.utils import abort
import requests

__author__ = 'mirko'

UPDATES_URL = env.get("jenkins_updates_url", "https://updates.jenkins-ci.org/update-center.json?id=default")
JENKINS_URL = env.get("jenkins_url", "https://huschteguzzel.de/hudson/")

LOG = logging.getLogger("jenkins_support")

@task
def update_center():
    """
    Updates plugin information from UPDATES_URL.
    """
    jenkins.update_center_(UPDATES_URL, JENKINS_URL)


@task
def restart():
    """
    Restarts Jenkins
    """
    run("sudo /etc/init.d/jenkins restart")

@task
def list_jenkins_processes():
    """List all processes belonging to jenkins."""
    run("ps -Ujenkins ufww")

@task
def kill_periodic_jobs(grep_pattern="periodic"):
    """Kills running periodic jobs"""
    sudo("for i in `ps aux | grep java | grep %s | awk '{print $2}'`; do kill -9 $i; done" % grep_pattern)


@task
def show_outdated_plugins():
    """
    Shows all outdated plugins.
    """
    require("jenkins_user")
    require("jenkins_token")
    j = jenkins.JenkinsUpdatePlugins(JENKINS_URL, env.jenkins_user, env.jenkins_token)
    j.get_updated_plugins_metadata()
    LOG.info("plugins_xml: {}".format(j.plugins_xml))

@task
def update_plugins():
    """
    Updates jenkins plugins.
    """
    require("jenkins_user")
    require("jenkins_token")
    j = jenkins.JenkinsUpdatePlugins(JENKINS_URL, env.jenkins_user, env.jenkins_token)
    j.get_updated_plugins_metadata()
    LOG.info("plugins_xml: {}".format(j.plugins_xml))
    if j.plugins_xml != "<root></root>":
        j.prevalidate_configuration()
        j.install_necessary_plugins()
        j.wait_for_installation_of_plugins()
        LOG.info("Ready for restart")
    else:
        LOG.info("No updated plugins found")
