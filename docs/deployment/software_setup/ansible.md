# Ansible

[Red Hat Ansible](https://www.ansible.com/) is configured on the management server (`galadriel`) for centralized configuration and automation on the cluster.

## Installation

If the instructions detailed on [Setting up the x86 hosts](../hardware_setup/x86hosts.md) were followed, Ansible should be installed from first boot on the management server.

If that is not the case, it can be installed through APT (instructions copied from the [official Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu), see there for more details):

```console
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo add-apt-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```

## Configuration

### Inventory and config

Ansible requires an [inventory of hosts](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) to work with networked devices.
A general configuration file also sits at [`/etc/ansible/ansible.cfg`](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html).
However, Ansible can be used to "bootstrap" itself from a default, vanilla installation; a playbook for this is provided in the [KTH-EXPECA/TestbedConfig repository](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/misc/playbooks/set_up_ansible_config.yaml).
Run it on the management host: `ansible-playbook set_up_ansible_config.yaml -K` (the `-K` flag allows to specify the `sudo` password interactively).


### SSH

Ansible requires a working SSH connection to the managed devices.
This should already be the case if the instructions for device provisioning detailed in [Setting up the Raspberry Pi 4B clients](../hardware_setup/raspberrypis.md) and [Setting up the x86 hosts](../hardware_setup/x86hosts.md) were followed.

If that is not the case, Ansible itself can be used to fix this using the `expeca_user_auth.yml` playbook on the [KTH-EXPECA/TestbedConfig repository](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/misc/playbooks/expeca_user_auth.yml).
This assumes you have some sort of SSH and `sudo` access on the remote devices, and fixes the user and SSH configuration on all devices:

1. It adds the `expeca` user, giving it full, password-less access to `sudo`.
   The public SSH keys of the team members are added to this user, enabling public-key authentication for SSH.

2. It configures the SSH server on every device to only allow public key authentication on port 22.

To execute this playbook, run `ansible-playbook expeca_user_auth.yml -K -k` from the management server; the `-K` and `-k` flags allow Ansible to ask for the `sudo` and SSH passwords respectively, in an interactive fashion.
