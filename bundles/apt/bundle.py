files = {}
_sources_list_d_prefix = "etc/apt/sources.list.d/"
for f in ("jenkins.list", "webupd8team-java-precise.list",):
    files["/{}{}".format(_sources_list_d_prefix, f)] = {
        'owner': 'root',
        'group': 'root',
        'mode': '0644',
        'source': "{}{}".format(_sources_list_d_prefix, f)
    }

del(f)
del(_sources_list_d_prefix)

actions = {
    'apt_update': {
        'cascade_skip': False,
        'interactive': True,
        'command': "apt-get update",
    },
}

