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
            "action:restart_jenkins",
        ]
    },
    '/etc/nginx/sites-available/default': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': 'etc/nginx/sites-available/default',
        'triggers': [
            "action:reload_nginx"
        ]
    },
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
    "restart_jenkins": {
        "command": "service jenkins restart",
        "triggered": True,
    },
    "reload_nginx": {
        "command": "service nginx reload",
        "triggered": True
    }
}