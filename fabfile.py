# vim: fileencoding=utf-8

__author__ = 'mirko'

import json
import logging

import nose
from fabric.api import *
import requests


UPDATES_URL = "https://updates.jenkins-ci.org/update-center.json?id=default"
HUSCHTEGUZZEL_URL = "https://huschteguzzel.de/hudson/"

require("huschteguzzel_shell_user")
env.hosts = ["huschteguzzel.de"]
env.user = env.huschteguzzel_shell_user

logging.basicConfig(level=logging.INFO)
logging.getLogger("dicttoxml").setLevel(logging.WARNING)

@task
def apt_get_update():
    sudo("apt-get update")


@task
def apt_get_upgrade():
    sudo("apt-get -q -y upgrade")


@task
def upgrade():
    execute(apt_get_update)
    execute(apt_get_upgrade)


@task
def jenkins_restart():
    """
    Restarts Jenkins
    """
    sudo("/etc/init.d/jenkins restart")

@task
def jenkins_update_center():
    require("jenkins_user")
    require("jenkins_token")
    auth = (env.jenkins_user, env.jenkins_token)
    raw = requests.get(UPDATES_URL).content
    json_text = raw.split('\n')[1]
    json.loads(json_text)
    reply = requests.post(HUSCHTEGUZZEL_URL + 'updateCenter/byId/default/postBack', data=json_text, auth=auth)
    if not reply.ok:
        abort("updates upload not ok {}".format(reply.text))
    logging.info('applied updates json')


def convert_updated_plugins_to_xml(plugins):
    plugins_xml = [u"<root>"]
    for plugin in plugins:
        name = plugin["name"]
        version = plugin["version"]
        installed = plugin["installed"]["version"]
        plugins_xml.append(u"""<{name} plugin="{name}@{version}"><installed plugin="{name}@{installed}"/></{name}>""".format
                           (name=name, version=version, installed=installed))
    plugins_xml.append(u"</root>")
    return u"".join(plugins_xml)


@task
def jenkins_update_plugins():
    """
    Updates jenkins plugins.
    """
    require("jenkins_user")
    require("jenkins_token")

    auth = (env.jenkins_user, env.jenkins_token)
    #execute(jenkins_update_center)
    reply = requests.get(
        HUSCHTEGUZZEL_URL +
        "updateCenter/site/default/api/json?pretty=true&depth=2&tree=updates[name,version,installed[shortName,version]]", auth=auth)
    if not reply.ok:
        abort("Could not get api")
    plugins_json = reply.content
    plugins = json.loads(plugins_json)["updates"]
    logging.info("outdated_plugins: {}".format(plugins))
    plugins_xml = convert_updated_plugins_to_xml(plugins)
    logging.info("plugins_xml: {}".format(plugins_xml))
    reply = requests.post(HUSCHTEGUZZEL_URL + "pluginManager/prevalidateConfig", data=plugins_xml, auth=auth)
    if not reply.ok:
        abort("Could not prevalidateConfig {}".format(reply.content))
    logging.info("Outdated plugins: {}".format(json.loads(reply.content)))
    return
    reply = requests.post(HUSCHTEGUZZEL_URL + "pluginManager/installNecessaryPlugins", data=plugins_xml, auth=auth)
    if not reply.ok:
        abort("Could not install plugins {}".format(reply.content))
    logging.info("pluginManager/installNecessaryPlugins: {}".format(reply.status_code))


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
