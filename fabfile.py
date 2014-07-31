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

logging.basicConfig(level=logging.DEBUG)

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
    postback = HUSCHTEGUZZEL_URL + 'updateCenter/byId/default/postBack'
    auth = (env.jenkins_user, env.jenkins_token)
    reply = requests.post(postback, data=json_text, auth=auth)
    if not reply.ok:
        abort("updates upload not ok {}".format(reply.text))
    logging.info('applied updates json')

@task
def jenkins_update_plugins():
    """
    Updates jenkins plugins.
    """
    require("jenkins_user")
    require("jenkins_token")
    auth = (env.jenkins_user, env.jenkins_token)
    #execute(jenkins_update_center)
    reply = requests.get(HUSCHTEGUZZEL_URL + "pluginManager/api/json?depth=1", auth=auth)
    if not reply.ok:
        abort("Could not get api")
    plugins_json = reply.content
    plugins = json.loads(plugins_json)
    outdated_plugins = []
    for plugin in plugins['plugins']:
        if plugin["hasUpdate"]:
            outdated_plugins.append(plugin["shortName"])
    logging.info("outdated_plugins: {}".format(outdated_plugins))
    reply = requests.get(HUSCHTEGUZZEL_URL + "pluginManager/api/xml?depth=2", auth=auth)
    if not reply.ok:
        abort("Could not get XML {}".format(reply.content))
    plugins_xml = reply.content
    reply = requests.post(HUSCHTEGUZZEL_URL + "pluginManager/prevalidateConfig", data=plugins_xml, auth=auth)
    if not reply.ok:
        abort("Could not prevalidateConfig {}".format(reply.content))
    logging.info("Outdated plugins: {}".format(reply.content))
    return
    reply = requests.post(HUSCHTEGUZZEL_URL + "pluginManager/installNecessaryPlugins", data=plugins_xml, auth=auth)
    if not reply.ok:
        abort("Could not install plugins {}".format(reply.content))
    logging.info(reply.content)
    return


@task(default=True)
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
