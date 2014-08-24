files = {
    '/etc/nginx/sites-available/default': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': 'etc/nginx/sites-available/default',
        'triggers': [
            "svc_systemv:nginx:reload"
        ]
    },
    '/etc/nginx/%s.crt' % node.hostname: {
        'owner': 'root',
        'group': 'root',
        'mode': '0444',
        'source': 'etc/nginx/%s.crt' % node.hostname,
        'content_type': 'text',
        'triggers': [
            "svc_systemv:nginx:reload"
        ]
    },
    '/etc/nginx/%s.key' % node.hostname: {
        'owner': 'root',
        'group': 'root',
        'mode': '0400', # key *must not* be readable!
        'content_type': 'text',
        'source': 'etc/nginx/%s.key' % node.hostname,
        'triggers': [
            "svc_systemv:nginx:reload"
        ]
    },
}

svc_systemv = {
    'nginx': {'running': True},
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
