pkg_apt = {
    "jenkins": { "installed": True },
    "oracle-java8-installer": { "installed": True },
    "oracle-java7-installer": { "installed": True },
}

files = {
    "/etc/default/jenkins": {
        "owner": "root",
        "group": "root",
        "mode": "0644",
        "source": "etc/default/jenkins",
        "triggers": [
            "svc_systemv:jenkins:restart",
        ]
    },
    "/var/lib/jenkins/.m2/settings.xml": {
        "owner": "jenkins",
        "group": "adm",
        "mode": "0640",
        "content_type": "text",
        "source": "m2/settings.xml",
    },
    "/var/lib/jenkins/.m2/toolchains.xml": {
        "owner": "jenkins",
        "group": "adm",
        "mode": "0640",
        "content_type": "text",
        "source": "m2/toolchains.xml",
    }
}

directories = {
    "/var/lib/jenkins/.m2": {
        "owner": "jenkins",
        "group": "adm",
        "mode": "0750",
        "needed_by": [
            "file:/var/lib/jenkins/.m2/toolchains.xml",
            "file:/var/lib/jenkins/.m2/settings.xml"
        ]
    }
}

svc_systemv = {
    "jenkins": { "running": True },
}

