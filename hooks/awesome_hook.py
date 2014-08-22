__author__ = 'mirko'

import logging


def node_apply_start(repo, node, interactive=False, **kwargs):
    logging.info("Starting apply on %s", node)


def action_run_start(repo, node, action, **kwargs):
    logging.info("Starting action %s on %s", action, node)


def node_run_start(repo, node, command, **kwargs):
    logging.info("Starting action %s on %s", command, node)


def run_start(repo, target, nodes, command, duration=None, **kwargs):
    logging.info("Starting action %s on %s of nodes %s", command, target, nodes)