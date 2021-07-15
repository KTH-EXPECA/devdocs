# Ansible

[Red Hat Ansible](https://www.ansible.com/) is configured on the management server (`galadriel`) for centralized configuration and automation on the cluster.

## Installation

If the instructions detailed on [Setting up the x86 hosts](../hardware_setup/x86hosts.md) were followed, Ansible should be installed from first boot on the management server.

If that is not the case, it can be installed through APT (instructions copied from the [official Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu), see there for more details):

``` bash
$ sudo apt update
$ sudo apt install software-properties-common
$ sudo add-apt-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```

## Configuration

### Inventory and config

Ansible requires an [inventory of hosts](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) to work with networked devices.
We use a somewhat complex inventory, located in the `ansible/inventory` directory of the [KTH-EXPECA](https://github.com/KTH-EXPECA/TestbedConfig) repository.
This inventory separates hosts into several groups, and specifies a bunch of host and group variables used by different plays and roles.

See:

- [`ansible/inventory/hosts.yml`](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/inventory/hosts.yml) for the actual hosts and group definitions.
- [`ansible/inventory/group_vars`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible/inventory/group_vars) for variables defined on a per-group basis.
- [`ansible/inventory/host_vars`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible/inventory/host_vars) for variables defined on a per-host basis.

Note that in case of conflict, host variables *override* group variables, and sub-group variables override super-group variabels.
We actually make active use of the latter behavior, in order to -- for instance -- define `cpu_arch: amd64` by default for *all* hosts, which we then override for the workload clients by defining `cpu_arch: arm64` in [`ansible/inventory/group_vars/clients.yml`](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/inventory/group_vars/clients.yml)


### SSH

Ansible requires a working SSH connection to the managed devices.
This should already be the case if the instructions for device provisioning detailed in [Setting up the Raspberry Pi 4B clients](../hardware_setup/raspberrypis.md) and [Setting up the x86 hosts](../hardware_setup/x86hosts.md) were followed.