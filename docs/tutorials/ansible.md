# Ansible

We use [Red Hat Ansible](https://www.ansible.com/) for centralized configuration of the testbed from `galadriel`.
This page presents an overview and "crash course" in using it on the ExPECA testbed; for more details, head to the [official documentation](https://docs.ansible.com/).

## Containerized Setup

In order to avoid issues with mismatching software versions and configurations, we have a containerized setup for general usage of Ansible on the testbed.
It consists of a Docker image containing Ansible, required Ansible Galaxy collections, and the necessary configuration for use on the testbed (`ansible.cfg` and the [inventory](#the-inventory)).
This Docker image can be found as [expeca/ansible](https://hub.docker.com/r/expeca/ansible) on [Docker Hub](https://hub.docker.com).

### Usage

In the `ansible` subdirectory of the [`KTH-EXPECA/TestbedConfig`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible) repository you will find a script named [`activate_config_env`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible/activate_config_env) which can be `source`'d to activate a "virtual environment" under which all Ansible commands will be run inside the container:

1. Navigate to the `ansible` subdirectory of the [`KTH-EXPECA/TestbedConfig`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible) repository.
2. Source the `activate_config_env` script:

    ``` bash
    $ source activate_config_env
    INFO: Activating config container environment.
    (config) $
    ```

3. All Ansible commands in this mode run inside the container, by default against the static Ansible configuration and inventory stored inside it.
   However, the commands also mount the current directory inside the container, allowing the running of playbooks, roles, and even specifying custom temporary configurations and inventories, as long as these files reside in the current directory or a subdirectory thereof. Examples:

    ```bash
    # simply runs the ping module against the elrond host 
    # defined in the container inventory
    (config) $ ansible elrond -m ping
    INFO: Running Ansible in config container!
    ------------------------------------------
    elrond | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python3"
        },
        "changed": false,
        "ping": "pong"
    }

    # runs the configure_auth.yml playbook, which resides under the current
    # directory OUTSIDE of the container, by mounting it inside.
    # the playbook is still run against the container inventory though.
    (config) $ ansible-playbook configure_auth.yml 
    INFO: Running Ansible in config container!
    ------------------------------------------

    PLAY [Update auth for the expeca user] *********************************************************

    TASK [Gathering Facts] *************************************************************************
    ok: [elrond]
    ok: [celeborn]
    ok: [galadriel]
    ...

    # overrides the inventory built into the container by specifying the
    # -i flag, in order to -- for instance -- test a new host config.
    # note that the new inventory must be located under the current directory
    # or inside a subfolder of it, and the path to it specified relatively.
    (config) $ ansible-playbook -i custom_inventory/hosts.yml configure_auth.yml 
    INFO: Running Ansible in config container!
    ------------------------------------------

    PLAY [Update auth for the expeca user] *********************************************************

    TASK [Gathering Facts] *************************************************************************
    ok: [elrond]
    ok: [celeborn]
    ok: [galadriel]
    ...
    ```

4. The config environment also provides a `config-container-cmd` to run arbitrary commands inside the continer:

    ``` bash
    (config) $ config-container-cmd bash
    INFO: Running command in config container!
    ------------------------------------------
    root@galadriel:/opt/workdir#
    ```

5. When finished using the config environment, you can exit it by running `deactivate_config_env`:

    ``` bash
    (config) $ deactivate_config_env
    INFO: Deactivating config container environment.
    $ 
    ```

#### Inner workings of the environment

The `activate_config_env` file is a Bash/Zsh source file which defines aliases for the Ansilbe CLI commands, as well as a function `deactivate_config_env` which resets everything to the state it was before entering the environment.
The defined aliases replace the normal Ansible commands with commands which:

1. Pull the required Docker image, if needed.
2. Run the container in the following manner:

    ``` bash
    docker run --rm -it --network host -e SSH_AUTH_SOCK=/ssh-agent \
      -v ${SSH_AUTH_SOCK}:/ssh-agent:rw -v \${PWD}:/opt/workdir:rw ${IMAGE}
    ```

    Explanation:

      - `--network host`: use the host network interfaces directly.
      - `-e SSH_AUTH_SOCK=/ssh-agent -v ${SSH_AUTH_SOCK}:/ssh-agent:rw`: forwards the host SSH-agent to the container.
          This is of course necessary to allow Ansible inside the container to authenticate agains the testbed hosts.
      - `-v \${PWD}:/opt/workdir:rw` mounts the current working directory inside the container, to allow access to playbooks, roles, and custom configurations without having to rebuild the container.

3. Finally, run the requested command inside the container.

### Updating the setup

In case the static Ansible configuration/inventory inside the container needs to be updated, simply make any required modifications in the `ansible` subdirectory of the [`KTH-EXPECA/TestbedConfig`](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/ansible) repository.
Then, use the provided `Makefile` to build and push the container image to Docker Hub:

``` bash
$ cd TestbedConfig/ansible

# make your changes
# then build and push using GNU Make

$ make ansible-container
... 
```

## Bare-bones 

A bare-bones setup should only be used when strictly needed, prefer to use the containerized deployment described above to avoid configuration mismatch issues.

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

The management network configuration [is directly tied to our Ansible inventory.](./adding_dhcp_dns_bindings.md)
In particular, **hostnames, DHCP bindings, and DNS records** are assigned directly from Ansible host aliases and host/group variables defined in the inventory.
This means that any substantial change in the structure of the inventory, modification of host aliases, or change in any of the relevant host/group variables, will **probably require rebuilding of the management network**.
For more details, see [here](./adding_dhcp_dns_bindings.md).


### Playbooks

The YAML files under `ansible/` correspond to [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) for different tasks.
Most of these are written following the structure [here](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html); that is, the actual Tasks to be performed are actually parameterized and defined in Roles.
These Roles are contained in the `roles/` directory.
Each subdirectory corresponds to a role with a matching name.
Again, [read this page](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) for more details on the usage of Roles in Playbooks.
