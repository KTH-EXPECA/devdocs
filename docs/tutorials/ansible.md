# Ansible

We use [Red Hat Ansible](https://www.ansible.com/) for centralized configuration of the testbed from `galadriel`.
This page presents an overview and "crash course" in using it on the ExPECA testbed; for more details, head to the [official documentation](https://docs.ansible.com/).

## Installation

Ansible should be installed from first boot on `galadriel`.
If this is not the case, or if for some reason it needs to be reconfigured, installation is straightforward --- simply install the `ansible` package through `apt`:

``` console
sudo apt install ansible
```

Alternatively, since it is built on Python, Ansible can be run from a local virtual environment.
Simply create the environment (make sure it is a Python3+ environment) inside the `ansible` subdirectory of the `KTH-EXPECA/TestbedConfig` repository, activate it, then use `pip` to install Ansible:

``` console
$ cd ansible/
./ansible/
$ python3 -m virtualenv --python=python3 ./venv 
created virtual environment CPython3.9.6.final.0-64 in 152ms
...
$ . venv/bin/activate
(venv) $ pip install -U ansible
Collecting ansible
  Downloading ansible-4.3.0.tar.gz (35.1 MB)
...
```

## Usage

Our Ansible configuration is fully contained inside the `ansible` subdirectory of the `KTH-EXPECA/TestbedConfig` repository; it is not installed system-wide, mostly for portability reasons.
Thus, whenever using Ansible, whether through ad-hoc commands or using playbooks, you will need to specify the correct configuration.
This can be done in two ways:

1. The easiest way is to `cd` into the `ansible` subdirectory of the `KTH-EXPECA/TestbedConfig` repository.
  Running Ansible from this directory will cause it to automatically detect the corresponding configuration, i.e.:

    ``` console
    $ cd TestbedConfig/ansible
    TestbedConfig/ansible
    $ ansible all -m ping
    ...
    ```

2. Alternatively, or if for some reason you need to run it from a different directory, you can explicitly tell Ansible which configuration file to use through the `ANSIBLE_CONFIG` environment variable.

      - You can set this variable by specifying it before the command to run on the command line:

        ``` console
        $ ANSIBLE_CONFIG=~/TestbedConfig/ansible/ansible.cfg ansible all -m ping
        ...
        ```

      - If you wish to run multiple commands, it might also be easier to `export` the variable:

        ``` console
        $ export ANSIBLE_CONFIG=~/TestbedConfig/ansible/ansible.cfg
        $ ansible all -m ping
        ...
        $ ansible-playbook example_playbook.yml
        ...
        ```

        This way, the variable will be set to the correct value until you log out.

## Configuration structure

We use an Ansible configuration directory structure which somewhat follows the [official guidelines detailed here.](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
It looks like this:

``` text
ansible/
├── ansible.cfg
├── inventory/
│   ├── hosts.yml
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── clients.yml
│   │   └── radiohosts.yml
│   └── host_vars/
│       ├── celeborn.yml
│       ├── elrond.yml
│       ├── finarfin.yml
│       ├── fingolfin.yml
│       ├── galadriel.yml
│       ├── workload-client-00.yml
│       ├── ...
│       └── workload-client-12.yml
├── <playbook1>.yml
├── ...
├── <playbookN>.yml
└── roles/
    ├── <role1>/
    │   ├── tasks/
    │   │   └── main.yml
    │   ├── vars/
    │   │   └── main.yml
    │   └── ...
    ├── <role2>/
    ├── ...
    └── <roleN>/
```

### The inventory

The [Ansible inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) for the testbed is contained under `inventory/`
It is structured in the following manner:

- `inventory/hosts.yml` contains the base structure of the hosts of the network.
  No variables are set here, only the host names and groups.
- `inventory/group_vars` contains the common and/or default variables for each host group.
  Each file corresponds to the group with the same name in the `hosts.yml` file.
  The most interesting of these files is the one corresponding to the `all` group, which contains defaults and common variables for *all* the hosts.
- Finally, `inventory/host_vars` contains one YAML file per host in the configuration.
  These files contain Ansible variables specific to each host in the testbed, some of which may override the inherited variables from the corresponding group.

#### Important note about the inventory

The management network configuration [is directly tied to our Ansible inventory.](/tutorials/adding_dhcp_dns_bindings/)
In particular, **hostnames, DHCP bindings, and DNS records** are assigned directly from Ansible host aliases and host/group variables defined in the inventory.
This means that any substantial change in the structure of the inventory, modification of host aliases, or change in any of the relevant host/group variables, will **probably require rebuilding of the management network**.
For more details, see [here](/tutorials/adding_dhcp_dns_bindings/).


### Playbooks

The YAML files under `ansible/` correspond to [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) for different tasks.
Most of these are written following the structure [here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html); that is, the actual Tasks to be performed are actually parameterized and defined in Roles.
These Roles are contained in the `roles/` directory.
Each subdirectory corresponds to a role with a matching name.
Again, [read this page](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) for more details on the usage of Roles in Playbooks.
