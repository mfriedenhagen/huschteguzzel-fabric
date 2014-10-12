pkg_apt = {
    "postfix": { "installed": True },
}
files = {
    "/etc/postfix/main.cf": {
        "owner": "root",
        "group": "root",
        "mode": "0644",
        "source": "main.cf",
        "content_type": "text",
        "triggers": [
            "svc_systemv:postfix:restart",
        ]
    },
    "/etc/postfix/gitlabtest.com.regexp": {
        "owner": "root",
        "group": "root",
        "mode": "0644",
        "content_type": "text",
        "source": "gitlabtest.com.regexp",
    },
    "/etc/aliases": {
        "owner": "root",
        "group": "root",
        "mode": "0644",
        "content_type": "text",
        "source": "aliases",
        "triggers": [
            "action:recreate_aliases.db",
        ]
    },
}
actions = {
    'recreate_aliases.db': {
        'command': "newaliases",
        'triggered': True,
    },
}
svc_systemv = {
    "postfix": { "running": True },
}