__author__ = 'mirko'

from os.path import basename, exists, join
import subprocess
from bundlewrap.exceptions import BundleError
from bundlewrap.items import Item, ItemStatus
from bundlewrap.utils import LOG, cached_property, hash_local_file
from bundlewrap.utils.text import randstr
from bundlewrap.utils.text import mark_for_translation as _
from bundlewrap.utils.remote import PathInfo

class Sudoers(Item):
    """
    Uploads a sudoers snippet to `/etc/sudoers.d/`.
    """
    BUNDLE_ATTRIBUTE_NAME = "sudoers"
    DEPENDS_STATIC = []
    ITEM_ATTRIBUTES = {
        'source': None,
    }
    ITEM_TYPE_NAME = "sudoers"
    PARALLEL_APPLY = False
    REQUIRED_ATTRIBUTES = ['source']

    def fix(self, status):
        """
        Do whatever is necessary to correct this item.
        """
        LOG.debug("Processing file_name: %s", self.template)
        base_name = basename(self.template)
        tmp_name = join("/tmp", "{}.{}".format(base_name, randstr()))
        LOG.debug("Uploading temporary sudo-file: %s", tmp_name)
        self.node.upload(
            self.template,
            tmp_name,
            mode="0640",
            owner="root",
            group="root"
        )
        LOG.debug("Checking temporary sudo-file: %s", tmp_name)
        self.node.run("/usr/sbin/visudo -c -f {}".format(tmp_name))
        self.node.run("mv -f -- {} /etc/sudoers.d/{}".format(tmp_name, base_name))

    def get_status(self):
        """
        Returns an ItemStatus instance describing the current status of
        the item on the actual node. Must not be cached.
        """
        file_name = basename(self.template)
        target = join("/etc/sudoers.d", file_name)
        LOG.debug("target: %s", target)
        path_info = PathInfo(self.node, target)
        correct = True
        status_info = {'needs_fixing': [], 'path_info': path_info}
        local_sha1 = hash_local_file(self.template)
        if not path_info.exists:
            LOG.debug("%s does not exist", path_info)
            correct = False
            status_info['needs_fixing'].append(target)
        elif path_info.sha1 != local_sha1:
            LOG.debug("%s has different content %s != %s", path_info, path_info.sha1, local_sha1)
            correct = False
            status_info['needs_fixing'].append(target)
        elif path_info.group != "root" or path_info.owner != "root" or path_info.mode != "0640":
            LOG.debug("%s has different ownership %s:%s or mode% %s",
                path_info,
                path_info.owner,
                path_info.group,
                path_info.mode)
            correct = False
            status_info['needs_fixing'].append(target)
        return ItemStatus(
            correct=correct,
            info=status_info
        )

    @cached_property
    def template(self):
        data_template = join(self.item_data_dir, self.attributes['source'])
        if exists(data_template):
            return data_template
        return join(self.item_dir, self.attributes['source'])

    def test(self):
        if not exists(self.template):
            raise BundleError(_(
                "{item} from bundle '{bundle}' refers to missing "
                "file '{path}' in its 'source' attribute"
            ).format(
                bundle=self.bundle.name,
                item=self.id,
                path=self.template,
            ))
        try:
            subprocess.check_output(("/usr/sbin/visudo", "-c", "-f", self.template))
        except subprocess.CalledProcessError, e:
            raise BundleError(str(e))



