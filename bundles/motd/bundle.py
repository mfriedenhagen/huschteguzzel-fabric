files = {
    '/etc/motd': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': "etc/motd",
    },
}

actions = {
    'apt_update': {
        'cascade_skip': False,
        'command': "apt-get update",
    },
}
