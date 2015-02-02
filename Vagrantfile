# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.proxy.http     = "http://10.0.2.2:3128"
  config.proxy.https    = "http://10.0.2.2:3128"
  config.proxy.no_proxy = "localhost,127.0.0.1"
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "wheezy-amd64"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 8086, host: 8086
  config.vm.network "forwarded_port", guest: 8083, host: 8083
  config.vm.hostname = 'huschteguzzel.de'
  config.vm.provider "virtualbox" do |vb|
    # Don't boot with headless mode
    vb.gui = false 
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "site.yml"
    # Run commands as root.
    ansible.verbose = 'vvvv'
    ansible.sudo = true
  end
end
