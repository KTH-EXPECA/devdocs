# Deploying a workload to the Testbed

*This documentation is a work-in-progress and subject to change.*

To deploy software to the testbed, we use a custom-built software framework called `Ainur` which automates:

1. The establishment of physical layer links.
2. The configuration of network layer components (networks and IP address ranges).
3. Finally, deploys the workload to the corresponding hosts in a containerized fashion.

In this page we will document the end-to-end procedure to writing a configuration for `Ainur` for automated experimentation.

## Physical layer configuration

TODO

## Network layer configuration

TODO

## Workload configuration

### Preparation

`Ainur` builds around Docker Swarm for containerized software deployment and orchestration.
As such, your first step into understanding how to write the configuration section for software deployment will be to read through the official Docker documentation for Swarm mode.
In particular, I suggest you first read through documentation in the following order:

1. [Docker Swarm mode overview.](https://docs.docker.com/engine/swarm/)
2. [Swarm mode key concepts.](https://docs.docker.com/engine/swarm/key-concepts/)
3. The [swarm mode tutorial.](https://docs.docker.com/engine/swarm/swarm-tutorial/)
   You can also, if you wish, try to follow the tutorial.
   However, you will not have to deal directly with a lot of the concepts explained there (for instance, you won't have to build the Swarm, as that is handled by `Ainur`)
4. Finally, [Deploy a stack to a swarm.](https://docs.docker.com/engine/swarm/stack-deploy/)
   In practice, `Ainur` builds up the whole infrastructure of the Docker Swarm from the physical layer up, and leaves workload management to the user (i.e. you).
   This means that the software deployment configuration simply consists of a `docker stack deploy`-compatible YAML document.

### Test on AWS

In order to prepare and test the configuration to run on the actual testbed, we will first run a small test on the AWS deployment.
For this test you will have to configure a small, 2-host Docker Swarm yourselves and deploy the workload on top of it; for the real deployment on the testbed, you will only have to provide the configuration file and `Ainur` will handle Swarm configuration for you.

#### Configuring the Swarm

##### Initialize the Swarm

1. Log into the `x86` AWS instance.
2. Make sure everything is up to date: `sudo apt update && sudo apt upgrade -y`
3. Initialize a Swarm with the `x86` instance as its manager:

    ``` bash
    $ docker swarm init --advertise-addr 172.31.100.125 --listen-addr 172.31.100.125 --data-path-addr 172.31.100.125
    Swarm initialized: current node (<node id>) is now a manager.

    To add a worker to this swarm, run the following command:

    docker swarm join --token SWMTKN-1-<random token> 172.31.100.125:2377

    To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
    ```

   Note: You should verify that `172.31.100.125` corresponds to the private IP address of the `x86` host through the AWS management console.

   Copy and save the token string (the section of text beginning with `SWMTKN-1-`) somewhere, as we will need it later.

##### Add the second node to the Swarm

1. Log into the `ARM64` AWS instance.
2. Make sure everything is up to date: `sudo apt update && sudo apt upgrade -y`
3. Connect this host to the Swarm we previously initialized:

    ``` bash
    $ docker swarm join --token SWMTKN-1-<random token> 172.31.100.125:2377
    Node joined the swarm as a worker.
    ```

   `SWMTKN-1-<random token>` corresponds to the token we saved earlier.

##### Add the necessary node labels

On the testbed, we use "node labels" to identify nodes in the Swarm and orchestrate the deployment of software to specific hosts.
We will need to set up the same labels on the AWS deployment in order to be able to correctly test our configuration.

1. Log back into the `x86` AWS instance.
   This instance is the Swarm manager and is the only one that can change properties such as node labels.
2. List the nodes in the Swarm, and take note of their identifiers (first column of the output): `docker node ls`
   You should be able to identify which node corresponds to the `x86` instance (it will have a `MANAGER STATUS` of `Leader`) and the `ARM64` instance.
3. Add a `type` label with value `cloudlet` to the `x86` instance node: `docker node update --label-add type=cloudlet <x86 node identifier>`
4. Add a `type` label with value `client` to the `ARM64` instance node: `docker node update --label-add type=client <ARM64 node identifier>`

The Swarm is now ready.

#### Write a deployment configuration file

To deploy your workload on the Swarm, you will have to write a so-called `docker-compose`-file.
A `docker-compose` file corresponds to a YAML document describing the containers to be run and how they are interconnected (as well as other things such as shared storage and so on).
You can study the full specification of `docker-compose` [files here.](https://docs.docker.com/compose/compose-file/compose-file-v3/), and [step through a tutorial on how these work in Swarm mode here.](https://docs.docker.com/engine/swarm/stack-deploy/)

Nelow you can see a simple example `docker-compose` file used to deploy a test workload to the testbed Swarm:

``` yaml
---
version: "3.9"
  services:
    server:
      image: expeca/primeworkload:server
      hostname: "server.{{.Task.Slot}}"
      environment:
        PORT: 5000
      deploy:
        replicas: 3
        placement:
          max_replicas_per_node: 3
          constraints:
          - "node.labels.type==cloudlet"
  
    client:
      image: expeca/primeworkload:client
      environment:
        SERVER_ADDR: "server.{{.Task.Slot}}"
        SERVER_PORT: 5000
      deploy:
        replicas: 3
        placement:
          max_replicas_per_node: 1
          constraints:
          - "node.labels.type==client"
        restart_policy:
          condition: on-failure
      depends_on:
      - server
...
```

In play English, the above `docker-compose` does the following:

1. Sets up three copies of the `expeca/primeworkload:server` container on nodes tagged `type=cloudlet`; since there is only a single cloudlet on the testbed currently, this means all three copies will run on the same host.
   Each copy of the server container is given a different hostname depending on its copy index (i.e. first copy is `server.1`, second is `server.2`, and final is `server.3`).
   Finally, the server software inside the container is given a single parameter `PORT` as an [environment variable](https://www.askpython.com/python/environment-variables-in-python) --- since the container is not being run "normally", this is the easiest way to pass parameters to replicatied copies of a service.
   ***YOU WILL HAVE TO MODIFY YOUR CODE TO ACCEPT CONNECTION PARAMETERS THIS WAY.***

2. Next, it sets up three copies of the `expeca/primeworkload:client` container on nodes tagged `type=client`; additionally, only one container is allowed to run per client.
   This means that this scenario needs three client hosts to run.
   Each copy of this container is once again passed parameters as environment variables; note in particular the `SERVER_ADDR` parameter --- this is once a again a dynamic parameter which will be assigned a different value per replicated copy.
   It will result in copy 1 of the client connecting to `server.1`, copy 2 to `server.2`, and copy 3 to `server.3`.
   Finally, we specify a `restart_policy` indicating if and when to restart the container; `on-failure` indicates that copies should only be restarted if the code fails.
   Other options are `any`, in which case containers are always restarted when they shut down; and `none`, in which containers are never restarted.

Your task now will be to 1. modify your code to accept parameters as environment variables and 2. write a similar configuration file, considering the limitations of the AWS test Swarm (2 nodes).
You can use the below skeleton as a starting point:

``` yaml
---
version: "3.9"
  services:
    controller:
      image: <your controller image>
      hostname: "controller.{{.Task.Slot}}"
      environment:
        PORT: <your port>
      deploy:
        replicas: 1
        placement:
          constraints:
          - "node.labels.type==cloudlet"
  
    plant:
      image: <your plant image>
      environment:
        CONTROLLER_ADDRESS: "controller.{{.Task.Slot}}"
        CONTROLLER_PORT: <your port>
      deploy:
        replicas: 1
        placement:
          max_replicas_per_node: 1
          constraints:
          - "node.labels.type==client"
        restart_policy:
          condition: on-failure
      depends_on:
      - server
...
```

Once you have done both things, we can progress on to deploying the workload on the AWS test environment.

#### Deploying workload on AWS Swarm

1. Log into the `x86` host.
2. Make sure the Swarm is healthy: `docker node ls`.
   You should see both nodes reporting OK statuses.
3. Deploy your `docker-compose` file as a Docker Swarm Service Stack:

    ``` bash
    $ docker stack deploy --compose-file docker-compose.yml InvertedPendulum
    Creating network InvertedPendulum_default
    Creating service InvertedPendulum_controller
    Creating service InvertedPendulum_plant
    ```
4. Check that it is running: `docker stack services InvertedPendulum`.
   You should see both services report `1/1` replicas running if everything went smoothly.
   Note: it can take a while for the services to start up, as they might have to pull the container images from Docker Hub, so have some patience.

5. You can check that the containers are running in the correct nodes by running `docker ps` on both the `x86` and `ARM64` hosts --- you should see one copy of the corresponding container running on each.
6. To check the logs of the controller: `docker service logs InvertedPendulum_controller`.
   And of the plant: `docker service logs InvertedPendulum_plant`.
7. Finally, to bring the stack down: `docker stack rm InvertedPendulum`.

Once the setup is working on AWS we can move on to deploying on the testbed.

## Deployment on the testbed through Ainur

### Log into Galadriel using the provided SSH keys

Your username is `project2021`.
No password is needed to login, only the SSH key.

Note that SSH is listening on a non-default port, `2222/tcp`, and that you will NEED to forward your SSH keys (using the `-A` flag).

``` bash
ssh -A -i .ssh/project_rsa project2021@testbed.expeca.proj.kth.se -p 2222
```

Alternatively, you can put this configuration into your `~/.ssh/config` file for persistent configuration:

``` ssh
...

Host testbed.expeca.proj.kth.se
    Hostname testbed.expeca.proj.kth.se
    Port 2222
    IdentityFile ~/.ssh/project_rsa
    User project2021
    ForwardAgent yes
```

Then, you can just do

``` bash
ssh testbed.expeca.proj.kth.se
```

### Clone your fork of Ainur

Note that you will need to use branch `dev_merge`.

``` bash
$ git clone <your Ainur fork>
...
$ cd Ainur
~/Ainur
$ git checkout dev_merge
Switched to branch dev_merge. 
```

### Prepare the Python environment and install necessary packages

``` bash
$ virtualenv --python=python3.8 venv
...
$ source venv/bin/activate

$ pip install -U pip -Ur requirements.txt
...
```

### Make sure all the hosts have your Docker images

I created a script to automatically pull your Docker images on all the hosts at once.
You can run it like so:

``` bash
$ python pull_image.py <image_name>
...
```

### Run your workload

Go!

### Collect your data

Once the workload has finished (or timed out), collected data can be found under `/opt/expeca/experiments/<experiment name>`.
If you get a permission denied error when trying to access the files, just use `sudo` (you will not be asked for a password).
