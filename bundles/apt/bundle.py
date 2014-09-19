files = {}

files.update(repo.libs.utils.apt_sources("jenkins.list", "webupd8team-java-precise.list"))

actions = {
    'apt_update': {
        'cascade_skip': False,
        'interactive': True,
        'command': "apt-get update",
    },
}

