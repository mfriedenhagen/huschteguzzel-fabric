files = {
    '/etc/motd': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': "etc/motd",
    },
    '/etc/default/jenkins': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': "etc/default/jenkins",
        'triggers': [
            "svc_systemv:jenkins:restart",
        ]
    },
    '/etc/nginx/sites-available/default': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': 'etc/nginx/sites-available/default',
        'triggers': [
            "svc_systemv:nginx:reload"
        ]
    },
}

svc_systemv = {
    'nginx': {'running': True},
    'jenkins': {'running': True},
}

symlinks = {
    "/etc/nginx/sites-enabled/default": {
        "group": "root",
        "owner": "root",
        "target": "/etc/nginx/sites-available/default",
        "needs": [
            "file:/etc/nginx/sites-available/default"
        ]
    },
}

actions = {
    'apt_update': {
        'cascade_skip': False,
        'command': "apt-get update",
    },
}