# vim: fileencoding=utf-8
import json
import logging
import time
from fabric.decorators import task
from fabric.operations import require, sudo
from fabric.state import env
from fabric.utils import abort
import requests

__author__ = 'mirko'

UPDATES_URL = env.get("jenkins_updates_url", "https://updates.jenkins-ci.org/update-center.json?id=default")
JENKINS_URL = env.get("jenkins_url", "https://huschteguzzel.de/hudson/")

LOG = logging.getLogger("jenkins_support")


class JenkinsUpdatePlugins(object):
    def __init__(self, root_url, user, password):
        self.root_url = root_url
        self.auth = (user, password)
        self.plugins_xml = None

    @staticmethod
    def _convert_updated_plugins_to_xml(plugins):
        plugins_xml = [u"<root>"]
        for plugin in plugins:
            name = plugin["name"]
            version = plugin["version"]
            installed = plugin["installed"]["version"]
            plugins_xml.append(
                u"""<update plugin="{name}@{version}"><installed plugin="{name}@{installed}"/></update>""".format
                (name=name, version=version, installed=installed))
        plugins_xml.append(u"</root>")
        return u"".join(plugins_xml)

    def get_updated_plugins_metadata(self):
        LOG.info("get_updated_plugins_metadata")
        reply = self._get(
            "updateCenter/site/default/api/json?depth=2&tree=updates[name,version,installed[shortName,version]]")
        if not reply.ok:
            abort("Could not get updates from updateCenter: {}".format(reply.status_code))
        plugins_json = reply.content
        plugins = json.loads(plugins_json)["updates"]
        LOG.debug("outdated_plugins: {}".format(plugins))
        self.plugins_xml = self._convert_updated_plugins_to_xml(plugins)

    def prevalidate_configuration(self):
        reply = self._post("pluginManager/prevalidateConfig", self.plugins_xml)
        if not reply.ok:
            abort("Could not prevalidateConfig {}".format(reply.content))
        LOG.info("Outdated plugins: {}".format(json.loads(reply.content)))

    def install_necessary_plugins(self):
        reply = self._post("pluginManager/installNecessaryPlugins", self.plugins_xml)
        if not reply.ok:
            abort("Could not install plugins {}".format(reply.content))
        LOG.info("pluginManager/installNecessaryPlugins: {}".format(reply.status_code))

    def wait_for_installation_of_plugins(self):
        """
        Waits 60 seconds for all plugin downloads to succeed.
        """
        i = 0
        outstanding_jobs = [True, ]  # initial non-empty value, so we enter the loop at least once
        while i < 12 and outstanding_jobs:
            reply = self._get("updateCenter/api/json?depth=1")
            if not reply.ok:
                abort("Could not get info from updateCenter: {}".format(reply.content))
            outstanding_jobs = [
                job for job in json.loads(reply.content)["jobs"]
                if job["type"] == "InstallationJob" and not job["status"]["success"]
            ]
            LOG.info("outstanding download jobs for plugins: {}".format(outstanding_jobs))
            i += 1
            time.sleep(5)

    def _post(self, path, data):
        url = self.root_url + path
        LOG.info("_post: {}".format(url))
        return requests.post(url, data=data, auth=self.auth)

    def _get(self, path):
        url = self.root_url + path
        LOG.info("_get: {}".format(url))
        return requests.get(url, auth=self.auth)


@task
def update_center():
    """
    Updates plugin information from UPDATES_URL.
    """
    require("jenkins_user")
    require("jenkins_token")
    auth = (env.jenkins_user, env.jenkins_token)
    LOG.info("jenkins_update_center: UPDATES_URL={}".format(UPDATES_URL))
    raw = requests.get(UPDATES_URL).content
    json_text = raw.split('\n')[1]
    json.loads(json_text)
    post_back_url = JENKINS_URL + 'updateCenter/byId/default/postBack'
    LOG.info("jenkins_update_center: post_back_url={}".format(post_back_url))
    reply = requests.post(post_back_url, data=json_text, auth=auth)
    if not reply.ok:
        abort("updates upload not ok {}".format(reply.text))
    LOG.info('applied updates json')


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
    j = JenkinsUpdatePlugins(JENKINS_URL, env.jenkins_user, env.jenkins_token)
    j.get_updated_plugins_metadata()
    LOG.info("plugins_xml: {}".format(j.plugins_xml))

@task
def update_plugins():
    """
    Updates jenkins plugins.
    """
    require("jenkins_user")
    require("jenkins_token")
    j = JenkinsUpdatePlugins(JENKINS_URL, env.jenkins_user, env.jenkins_token)
    j.get_updated_plugins_metadata()
    LOG.info("plugins_xml: {}".format(j.plugins_xml))
    if j.plugins_xml != "<root></root>":
        j.prevalidate_configuration()
        j.install_necessary_plugins()
        j.wait_for_installation_of_plugins()
        LOG.info("Ready for restart")
    else:
        LOG.info("No updated plugins found")