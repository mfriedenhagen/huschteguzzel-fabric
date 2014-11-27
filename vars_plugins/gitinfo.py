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
import getpass
import subprocess

class VarsModule(object):

    """
    Loads variables for groups and/or hosts
    """

    def __init__(self, inventory):
        """ constructor """
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()


    def get_host_vars(self, host, vault_password=None):
        """ Get host specific variables. """
        if VarsModule.info is None:
            info = {}
            info["revision"] = subprocess.check_output(("git", "rev-parse", "--short", "--porcelain", "HEAD")).strip()
            info["branch"] = [branch for branch in subprocess.check_output(("git", "branch")).strip().split("\n") if branch.startswith("*")][0][2:]
            info["status"] = subprocess.check_output(("git", "status", "--porcelain")).strip() and "MODIFIED" or "UNMODIFIED"
            info["user"] = getpass.getuser()
            VarsModule.info = info
        host.set_variable('gitinfo', VarsModule.info)
VarsModule.info = None
