# Setting up the x86 hosts

All x86 hosts run [Ubuntu Server 20.04 LTS](https://releases.ubuntu.com/20.04/), and as such can be provisioned using [cloud-init](https://cloudinit.readthedocs.io/en/latest/).
In the following, we will set up a network-local HTTP server that will serve instance metadata to the hosts as they are booting up for the first time.

## The metadata server

[Cloud-init](https://cloudinit.readthedocs.io/en/latest/) can be configured to fetch host metadata and user data on first boot from a plain HTTP server (see [here](https://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html) and [here](https://opensource.com/article/20/5/create-simple-cloud-init-service-your-homelab)).
Configuration for the hosts can be found on the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig) repository.

### Prerequisites

1. The metadata server should be reachable through the network by the machine being instantiated, for instance by deploying it on a device connected to the management network switch.
    Make sure to write down the IP address of the device running the server (on Ubuntu and Arch Linux, you can figure out the IP address of the local computer through the `ip addr show` command).
2. For the following instructions, Docker should be installed on the device hosting the metadata server.
    However, this is only for convenience, as the metadata server just needs to be a barebones HTTP server - this can also be achieved through the Python 3 web server module for instance (i.e. `python3 -m http.server ...`).
3. Make sure there are no firewall rules blocking access to the port we will be using to serve metadata on the device hosting the metadata server container.
    On Ubuntu, the commands for letting traffic through the firewall are (replace `$PORT` with the desired port number):

        # check status of the default "uncomplicated firewall" 
        $ sudo ufw status
        Status: active

        # if the output of the previous command is "active", add a rule to allow external connections on TCP port $PORT
        $ sudo ufw allow $PORT/tcp
        Rule added
        Rule added (v6)

### Deploy a metadata server using Docker

1. Clone the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig) repository:

        git clone git@github.com:KTH-EXPECA/TestbedConfig.git

2. Serve metadata using the official NGINX Docker container image.
    Replace `$MDATADIR` with the directory containing metadata for the desired instance, and `$PORT` with the desired port on which to listen:

        docker run --rm -it -p $PORT:80 -v /path/to/TestbedConfig/$MDATADIR:/usr/share/nginx/html:ro nginx:latest

3. Make sure the files are accessible from the network by visiting the IP address of the metadata server host from a web browser (don't forget to include the port in the URL).

    - This can also be tested on out the command line using `wget` or `curl` (replace `$ADDR` with the IP of the metadata server host and `$PORT` with the TCP port on which it is listening):

            wget $ADDR:$PORT/meta-data

            curl -X GET $ADDR:$PORT/meta-data

### Preparing the install media

1. Obtain a copy of the Ubuntu Server 20.04 LTS install image [from the official website.](https://releases.ubuntu.com/20.04/)
2. If instantiating a physical device, prepare a bootable USB with this image.

    - Easiest way to do this is probably using [Ventoy](https://www.ventoy.net). Read the [Getting started](https://www.ventoy.net/en/doc_start.html) documentation to quickly get a bootable USB up and running.
    - Alternatively, use tools like [Rufus](https://rufus.ie/en_US/), [Unetbootin](https://unetbootin.github.io/), or plain-old [command line](https://wiki.archlinux.org/title/USB_flash_installation_medium).

### Instantiate an x86 host with cloud-init and the metadata server

1. Boot into the bootloader of the previously prepared installation media, but don't boot into the installer itself yet.
2. Edit the installer kernel command line to point it towards the previously prepared metadata server:

    - At the bootloader main menu, select `Install Ubuntu Server` and press `e`.
    - Edit the line

            linux /casper/vmlinuz quiet ---

    to read

            linux /casper/vmlinux quiet autoinstall ds=nocloud-net;s=http://$ADDR:$PORT/ ---

    replacing `$ADDR` and `$PORT` with the address and port of the metadata server.

3. Press `F10` to boot. The installer will now connect to the metadata server and set up the host based on the metadata obtained.

## meta-data and user-data files for the hosts

### Management Server

### Database & Storage Server

### Cloudlet
