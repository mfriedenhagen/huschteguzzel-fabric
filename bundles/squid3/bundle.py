files = {
    '/etc/squid3/squid.conf': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': 'etc/squid3/squid.conf',
        'triggers': [
            "svc_upstart:squid3:reload"
        ]
    },
}

svc_upstart = {
    'squid3': {'running': True},
}
