# Fluent

We use containerised versions of [Fluentbit](https://fluentbit.io/) for logging and debugging. Fluentbit is the simpler version of [Fluentd](https://www.fluentd.org/) with much easier configurations. For instance, unlike Fluentd, the configuration of Fluentbit is a simple YAML file. For all the the anticipated tasks in the initial set-up, the capabilities of Fluentbit is sufficient.


## Configuration
We configure a fluentbit container in each of the workloads and clients to forward the standard input to the fluentbit container configured on the logging PC - `Celeborn`. Before forwarding, the client containers convert the unstructured logs -if any- to a structured JSON format. It also adds an additional key denoting the hostname. Currently, the hostname is the container hostname, but the idea is to pass the hostname of the client on which the container is running. The fluentbit container inside the logging PC is configured to collect the logs from all the clients and append it to a file created within the docker volume.

The files used for the configuration of the fluentbit container in `Celeborn` and the clients are given below separately. The contents of the file are self explanatory.

### Configuration in `Celeborn`
- docker-compose.yml
```` bash
version: "3.5"
services:
  fluentbit:
    #network_mode: host
    build:
      context: .
      dockerfile: ./Dockerfile
      #network: host
    ports:
      - "24224:24224"
      - "24224:24224/udp"
      - "24225:24225"
      - "24225:24225/udp"
    volumes:
      - /home/expeca/Fluent/${DIRNAME}:/fluent-bit/log:rw
        #Enable above  mapping to use Docker Mount
        #Enable below mapping and definition to use Docker Volumes
        #- fluentVol:/fluent-bit
#volumes: 
   #fluentVol:
        
````

- Dockerfile 
```` bash
FROM fluent/fluent-bit:1.8.7
#version tags  1.8.8 and latest has some known issues with rewrite_tag plugin,
ADD fluent-bit.conf /fluent-bit/etc/
````

- fluent-bit.conf 
```` bash
[SERVICE]
    log_level debug
    Parsers_File parsers.conf

[INPUT]
    Name forward
    Listen 0.0.0.0
    port 24225

[FILTER]
    Name rewrite_tag
    Match *
    Rule $source ^stdout$ misc true
    # True is not necessay. Needs to correct and make it to false. 
    # Also this has some dependency and error with fluent:latest version.
    Emitter_Name MiscTagAdder

[FILTER]
    Name rewrite_tag
    Match *
    Rule $LogId ^([0-9]+)$ logId.$LogId true
    # True is not necessay. Needs to correct and make it to false. 
    # Also this has some dependency and error with fluent:latest version.
    Emitter_Name logIdTagAdder

#[FILTER]
#    Name record_modifier
#    Match *
#    Record hostname ${HOSTNAME}
#[FILTER]
#    Name parser
#    Match *
#    Key_Name log
#    Parser docker
#
#[OUTPUT]
#    Name stdout
#    Match *
#    Format json_lines
#
[OUTPUT]
    Name file
    Match logId.0
    File Logs_LogId_0.csv
    Format csv
    Path /fluent-bit/log/

[OUTPUT]
    Name file
    Match misc
    File Logs_Misc.log
    Path /fluent-bit/log/

````


### Configuration in the clients
- docker-compose.yml
```` bash
version: "3.5"
services:
  fluentbit_client:
    #network_mode: host
    #hostname: '{{.Node.Hostname}}'
    hostname: $HOSTNAME
    stdin_open: true
    tty: true
    build:
      context: .
      dockerfile: ./Dockerfile
      #network: host
    ports:
      - "24224:24224"
      - "24224:24224/udp"
      - "24225:24225"
      - "24225:24225/udp"
  ack:
    image: ubuntu
    command: [/bin/echo, "=========Fluent started for log forwarding========"]
    depends_on:
            - fluentbit_client
    logging:
      driver: fluentd
      options:
        tag: docker-ubuntu
````

- Dockerfile 
```` bash
FROM fluent/fluent-bit:latest
ADD fluent-bit.conf /fluent-bit/etc/
````

- fluent-bit.conf 
```` bash
[SERVICE]
    log_level debug
    Parsers_File parsers.conf

[INPUT]
    Name forward
    Listen 0.0.0.0
    port 24224

[FILTER]
    Name parser
    Match *
    Key_Name log
    Parser docker

[FILTER]
    Name record_modifier
    Match *
    Record hostname ${HOSTNAME}

[OUTPUT]
    Name forward
    Host 192.168.1.3
    Port 24225
    Match *
````

- parsers.conf 
```` bash
[PARSER]
    Name docker
    Format json
    Time_Key time
    Time_Format %Y-%m-%dT%H:%M:%S.%L
    Time_Keep On
    Decode_Field_As escaped_utf8 log
````

## Deployment

Creating the above files in the logging PC is straightforward and easy and it is only a matter of bringing up the docker-compose with the standard `docker-compose up` command from the correct directory. 
```` bash
docker-compose -f /home/expeca/Fluent/docker-compose.yml up --build --force-recreate -d
````
However, this assumes the presence of an updated environment file. Note that in the `docker-compose.yml` file, we used the environment variable `DIRNAME` to create a dynamic directory during the runtime to manage various logs. This environment variable will be taken from the default `.env` file kept in the same path as the compose file. This can be updated according to necessity. For instance, to save the logs in a directory structure based on current date-time, one can use the below command to update the environment file and run create the container.
```` bash
echo "DIRNAME=$(date +"%y-%m-%d-%H-%M-%S")" > .env && docker-compose -f /home/expeca/Fluent/FluentCeleborn/docker-compose.yml up --build --force-recreate -d
````

In case if one needs to see the logs live, the following `tail` command can be used.
```` bash
sudo tail -f <path-to-file>
````
Path to the file in case of a docker volume is /var/lib/docker/volumes/fluent_fluentVol/_data/log


However, doing this in the client is not so easy due to the number of clients. Hence, we use Ansible to copy the files to the respective locations in the clients. This is particularly useful when one has to make slight modifications to the files in each and every client. 

### Ad-hoc method
For the initial deployment, we use the Ansible ad-hoc commands to do these tasks as explained below. We start with creating a copy of the client files in the management PC -`Galadriel`- and use ad-hoc commands to copy this to the clients. This needs to be done from the proper Ansible directory. For more information, refer to the tutorial on Ansible.

- Create a directory `/home/expeca/Fluent` in the management PC containing the necessary fluent files for the clients.
- Copy the files to every client. For this we use the Ansible inventory group `workload`.
```` bash
ansible workload -m copy -a 'src=/home/expeca/Fluent dest=/home/expeca'
````
- Rebuild and start the containers. This needs to be done only after starting the fluent container in the server - `Celeborn`.
```` bash
ansible workload -a 'docker-compose -f Fluent/docker-compose.yml up --build --force-recreate -d'
````
- In case if one needs to test the logging, the following command can be used.
```` bash
ansible workload -a 'docker run --log-driver=fluentd -t ubuntu echo ">>>>>>>>>>>>>Testing a log message<<<<<<<<<<<<<"'
````
