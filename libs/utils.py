# vim: fileencoding=utf-8

def apt_sources(*sources):
    """
    Returns a dictionary with apt sources files.
    """
    files = {}
    _sources_list_d_prefix = "etc/apt/sources.list.d/"
    for f in sources:
        files["/{}{}".format(_sources_list_d_prefix, f)] = {
            'owner': 'root',
            'group': 'root',
            'mode': '0644',
            'source': "{}{}".format(_sources_list_d_prefix, f)
        }
    return files
