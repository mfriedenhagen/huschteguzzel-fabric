files = {
    '/etc/default/jenkins': {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': "etc/default/jenkins",
        'triggers': [
            "svc_systemv:jenkins:restart",
        ]
    },
}

#jenkins = {
#    "huschteguzzel": {
#        "jenkins_url": "https://huschteguzzel.de/hudson/"
#    }
#}

svc_systemv = {
    'jenkins': {'running': True},
}

