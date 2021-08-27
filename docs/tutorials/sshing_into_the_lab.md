# Accessing the lab remotely

## Overview

- The ingress router `cirdan` listens for incoming SSH connections to the testbed on the address [`testbed.expeca.proj.kth.se`](ssh://testbed.expeca.proj.kth.se:2222), port `2222`.

    - You can also use the testbed WAN IP address directly, `130.237.53.70`.

- All incoming connections are forwarded to `galadriel`.
- Remote SSH access to `galadriel` is *only* permitted through public-key authentication.
- From `galadriel`, access to every other host on the network is possile, again exclusively through public-key authentication (make sure to forward your SSH agent when connecting).

## Prerequisite: SSH keys

To access the lab remotely you will need a private-public SSH key pair.
If you do not already have one, you can generate one following the instructions [here](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

After generating the keys, your public key needs to be added to the cluster by someone with administrative privileges.

**NOTE:** Never share your *private* key --- only your *public* key is safe to distribute.

## Logging in to the management host (`galadriel`)

1. If you haven't done so yet, initialize your SSH agent and add your key to it:

    ``` console
    $ eval "$(ssh-agent -s)"
    > Agent pid <some number>

    $ ssh-add ~/.ssh/<your private key>
    Identity added: <your private key>
    ```

2. Add the following configuration to the SSH config file (usually at `.ssh/config`, see below if you don't have access to such a configuration):

    ``` text
    Host ExPECA # or whatever other name you wish to use to refer to this config
        Hostname        testbed.expeca.proj.kth.se  # alternatively, use the IP directly: 130.237.53.70
        Port            2222
        IdentityFile    ~/.ssh/your_private_key # replace with your private key file name
        User            expeca  # alternatively, replace with your username
        ForwardAgent    yes # required for pivoting into other hosts
    ```

3. SSH into the management host:

    ``` console
    $ ssh ExPECA  # or whatever name you chose for the configuration above.
    ...
    expeca@galadriel:~$
    ```

### Logging in without a configuration file

If for some reason you can't write to the `.ssh/config` file, you can specify all options for the connection on the command line like so:

``` console
# -A enables SSH agent forwarding
# -p specifies the target port
# replace ~/.ssh/your_private_key with the path to your private key
# optional: replace testbed.expeca.proj.kth.se with 130.237.53.70
# optional: replace expeca with your username on galadriel

$ ssh -A -p 2222 -i ~/.ssh/your_private_key expeca@130.237.53.70 
...
expeca@galadriel:~$
```

### Pivoting into other hosts from `galadriel`

Once logged in to `galadriel`, if you forwarded your SSH agent correctly, you should be able to pivot into any of the other hosts.

1. Check that your agent has been forwarded:

    ``` console
    expeca@galadriel:~$ ssh-add -l
    # should output a list of available ssh keys
    ```

    If the above command does not output any keys, the probable causes are two:

    1. Your SSH agent was not correctly forwarded when initiating the connection.
        Make sure you added the `ForwardAgent` option in `.ssh/config` and/or specify `-A` on the command line.
    2. Your SSH agent was correctly forwarded but your key has not been added to it.
        Make sure to run `ssh-add <your private key>` before initiating the connection.

2. Pivot into another host, making sure to forward your agent again to have access to your keys on the new host too. Also, note that on all hosts other than `galadriel`, there only exists a single user account `expeca`.

    ``` console
    # replace elrond with your host of choice
    expeca@galadriel:~$ ssh -A expeca@elrond 
    ...
    expeca@elrond:~$ 
    ```

## A note on user accounts on `galadriel`

Every user with access to `galadriel` technically has access to two user accounts on the system:

- A personal account using the same username as their KTH account.
- The `expeca` account, a special shared account for management of the cluster.

*Please* be careful when executing commands on the `expeca` account, as that is the account we use for general management of the cluster.
In particular, avoid changing things like environment variables and Python interpreters on the `expeca` user as Ansible depends on those.
