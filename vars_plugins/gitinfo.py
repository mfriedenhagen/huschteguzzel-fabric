# (c) 2014, Mirko Friedenhagen <mfriedenhagen@gmail.com>
# (c) 2014, Serge van Ginderachter <serge@vanginderachter.be>
#
# This file is not part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import subprocess

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
        if VarsModule.revision is None:
            VarsModule.revision = subprocess.check_output(("git", "rev-parse", "--short", "--porcelain", "HEAD")).strip()
            VarsModule.branch = [branch for branch in subprocess.check_output(("git", "branch")).strip().split("\n") if branch.startswith("*")][0][2:]
            VarsModule.modified = subprocess.check_output(("git", "status", "--porcelain")).strip() and "MODIFIED" or "UNMODIFIED"
        host.set_variable('gitinfo_revision', VarsModule.revision)
        host.set_variable('gitinfo_branch', VarsModule.branch)
        host.set_variable('gitinfo_modified', VarsModule.modified)


    def get_group_vars(self, group, vault_password=None):
        """ Get group specific variables. """
        return {}
VarsModule.revision = None
VarsModule.branch = None
VarsModule.modified = None
