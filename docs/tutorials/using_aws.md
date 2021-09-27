# Using the AWS staging setup

In order to avoid testing new things on the "production" (i.e. *real*) testbed, we have a virtualized pseudo-clone of the testbed set up on Amazon Web Services.
This "staging" setup mimics the structure of the physical testbed and allows us to test things without fear of ruining anything.

The workflow for working on the staging setup looks like the following:

1. Bring up the AWS EC2 instances.
2. SSH into `galadriel` on the staging setup.
3. Do work.
4. Close the SSH connection to `galadriel`.
5. Bring down the AWS EC2 instances.

**Note:** We bring only bring instances up when we need to, to avoid unnecessary expenses.
**Please me sure to always bring down the staging testbed after you're done working.**

## Bringing up the staging setup

Bringing up the staging setup needs to be done from a computer with access to your private SSH key associated with the testbed.
Additionally, you need to have cloned the [`KTH-EXPECA/TestbedConfig`](http://github.com/KTH-EXPECA/TestbedConfig) repository, and either have set up Docker to use our [Ansible container](./ansible.md#containerized-setup), or have set up [bare-bones Ansible](./ansible.md#bare-bones).

### Using the Ansible container

This is the easiest way of interacting with the AWS setup:

1. `cd` into the `ansible` directory of the `KTH-EXPECA/TestbedConfig` repo.
2. Execute the `./manage_aws_staging.sh` shell script and choose the start action:

    ``` bash
    .../KTH-EXPECA/TestbedConfig/ansible $ ./manage_aws_staging.sh             
    INFO: Activating config container environment.
    INFO: Running Ansible in config container!
    ------------------------------------------
    Please select action to take (create/start/stop/terminate): start
    ...
    ```

3. Ansible will proceed to bring up the testbed, and will output the public address of `galadriel` when finished:

    ``` text
    ...
    [manage_aws : Output remote address]
    Remote connection address: <something>.eu-north-1.compute.amazonaws.com. Press any key to continue:
    ...
    ```

### Using bare-bones Ansible

1. `cd` into the `ansible` directory of the `KTH-EXPECA/TestbedConfig` repo.
2. Source the `staging_auth.env` file to register the necessary AWS keys: `source ./staging_auth.env`
3. Use the `manage_ec2_aws.yml` to bring up the testbed, together with the **special inventory** `inventory/hosts.staging.yml` (*note:* it's crucial that you specify the correct inventory here).
   When prompted, specify `start` as the action to perform:

    ``` console
    # We specify ANSIBLE_CONFIG here just as a precausion; no need to include it if Ansible doesn't complain when omitting it.

    $ ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory/hosts.staging.yml manage_ec2_aws.yml 
    Please select action to take (create/start/stop/terminate): start
    ```

4. Ansible will proceed to bring up the testbed, and will output the public address of `galadriel` when finished:

    ``` text
    ...
    [manage_aws : Output remote address]
    Remote connection address: <something>.eu-north-1.compute.amazonaws.com. Press any key to continue:
    ...
    ```

## SSHing to the staging setup

After bringing up the staging setup, you can SSH into `galadriel` using the address output by the `manage_ec2_aws.yml` playbook.
Note that you will need to specify the private key you use to remote into the testbed and enable SSH-agent forwarding (`-i` and `-A` flags respectively):

``` console
ssh -i .ssh/id_expeca_testbed -A expeca@<something>.eu-north-1.compute.amazonaws.com
```

Alternatively, you can add the following entry to your `.ssh/config`:

```text
Host *.eu-north-1.compute.amazonaws.com
    User expeca
    IdentityFile <your private key file>
    ForwardAgent yes
```

Opening an SSH connection to the staging testbed becomes simply a matter of running:

```console
ssh <something>.eu-north-1.compute.amazonaws.com
```

## Bringing down the staging setup

To bring down the staging setup, follow the same [instructions as for bringing it up](#bringing-up-the-staging-setup), but change the desired action to `stop`:

``` bash
.../KTH-EXPECA/TestbedConfig/ansible $ ./manage_aws_staging.sh             
INFO: Activating config container environment.
INFO: Running Ansible in config container!
------------------------------------------
Please select action to take (create/start/stop/terminate): stop
...
```

<!-- ``` console
# We specify ANSIBLE_CONFIG here just as a precausion; no need to include it if Ansible doesn't complain when omitting it.

$ ANSIBLE_CONFIG=ansible.cfg ansible-playbook -i inventory/hosts.staging.yml manage_ec2_aws.yml 
Please select action to take (create/start/stop/terminate): stop
``` -->

## Resetting the staging setup

In case of a major failure, the staging setup allows for easy re-provisioning of all the instances for clean start.
Note that this will return the instances to a base configuration, and any work done on them might be lost forever.

To reset the staging setup:

1. Select the `terminate` option to destroy the EC2 instances (note that this **will delete any stored data on them that doesn't correspond to the base setup**).
    You will be asked for confirmation 3 times!

    ``` bash
    .../KTH-EXPECA/TestbedConfig/ansible $ ./manage_aws_staging.sh             
    INFO: Activating config container environment.
    INFO: Running Ansible in config container!
    ------------------------------------------
    Please select action to take (create/start/stop/terminate): terminate
    ...
    ```

2. Select the `create` option to recreate the EC2 instances:
    
    ``` bash
    .../KTH-EXPECA/TestbedConfig/ansible $ ./manage_aws_staging.sh             
    INFO: Activating config container environment.
    INFO: Running Ansible in config container!
    ------------------------------------------
    Please select action to take (create/start/stop/terminate): create
    ...
    ```

3. After the instances come back up, they will be in an useable but *not* fully configured state yet.
4. [SSH into `galadriel`.](#sshing-to-the-staging-setup)
5. `cd` into `TestbedConfig/ansible`.
6. Update the repository with `git pull`.
7. Activate the Ansible virtual environment that is already there: `source venv/bin/activate`.
8. Run the `set_hostnames.yml` playbook to fix hostnames and host IP resolution on all instances (note the `-i inventory/hosts.staging.yml` flag):

    ``` console
    $ ansible-playbook -i inventory/hosts.staging.yml set_hostnames.yml
    ...
    ```

9. Run the `configure_docker_swarm.yml` playbook to bring up and re-configure the Docker swarm (again, note the `-i inventory/hosts.staging.yml` flag):

    ``` console
    $ ansible-playbook -i inventory/hosts.staging.yml configure_docker_swarm.yml
    ...
    ```

10. Delete `~/.ssh/known_hosts` as a precaution, as host RSA keys might have changed: `rm ~/.ssh/known_hosts`.
11. Reboot all instances except `galadriel` (once more, note the `-i inventory/hosts.staging.yml` flag):

    ``` console
    $ ansible -i inventory/hosts.staging.yml 'all:!galadriel' -m reboot --become
    ...
    ```

12. Reboot `galadriel`: `$ sudo reboot`.
    This will disconnect your current SSH session.

13. Finally, [reconnect to the staging testbed.](#sshing-to-the-staging-setup)
    Like before, host keys might have changed, and thus you might have to edit your local `.ssh/known_hosts` to delete old keys.
