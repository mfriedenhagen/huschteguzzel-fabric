import getpass
try:
    import keyring
except ImportError:
    keyring = None
import os

class VarsModule(object):

    """
    Loads variables for groups and/or hosts
    """

    def __init__(self, inventory):
        """ constructor """
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()


    def run(self, host, vault_password=None):
        """ For backwards compatibility, when only vars per host were retrieved
            This method should return both host specific vars as well as vars
            calculated from groups it is a member of """
        return {}


    def get_host_vars(self, host, vault_password=None):
        """ Get host specific variables. """
        user = os.environ.get("ANSIBLE_USER")
        if VarsModule.sudo_password is None and user is not None and keyring is not None:
            VarsModule.sudo_password = keyring.get_password("ANSIBLE_PASSWORD", user + "@huschteguzzel.de")
        if VarsModule.sudo_password is None:
            VarsModule.sudo_password = getpass.getpass(prompt="sudo password")
        host.set_variable('ansible_sudo_pass', VarsModule.sudo_password)


    def get_group_vars(self, group, vault_password=None):
        """ Get group specific variables. """
        return {}
VarsModule.sudo_password = None
