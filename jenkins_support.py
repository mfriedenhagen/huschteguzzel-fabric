# vim: fileencoding=utf-8
import json
import logging

from items import jenkins
from fabric.decorators import task
from fabric.operations import require, sudo
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
    require("jenkins_user")
    require("jenkins_token")
    sudo("/etc/init.d/jenkins restart")
    auth = (env.jenkins_user, env.jenkins_token)


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