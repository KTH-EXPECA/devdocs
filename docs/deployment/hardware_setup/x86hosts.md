# Setting up the x86 hosts

To provision the x86 hosts we use [Ubuntu Server autoinstall](https://ubuntu.com/server/docs/install/autoinstall), available from [Ubuntu Server 20.04 LTS](https://releases.ubuntu.com/20.04/) on.
This uses a custom configuration of [cloud-init](https://cloudinit.readthedocs.io/en/latest/) to automate the install of Ubuntu Server on the target machine and to configure it on first boot.

## The autoinstall configuration files

For in-depth details on the autoinstall configuration file format, see [here](https://ubuntu.com/server/docs/install/autoinstall-reference) and [here](https://ubuntu.com/server/docs/install/autoinstall-reference).
It follows a similar structure as a generic cloud-config YAML file, with some caveats.
The file *must* be a plain text file named `user-data` (without any filetype extension), and it *must* begin with a magic comment, `#cloud-config` (note that there should be ***no*** space after the `#`), followed by a single top-level key `autoinstall`.
The `autoinstall` key contains all the configuration directives detailed in the aforementioned links, e.g.:

```yaml
#cloud-config
autoinstall:
  version: 1
  identity: { ... }
  ...
```

For more details, on the autoinstall configuration files, please see the extensively documented files for the hosts that can be found on the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/cloud-init) repository.


## Providing the autoinstall configuration at install time

The easiest way to provide this autoinstall configuration file to the Ubuntu Server installer is over the network, through a plain HTTP metadata server (see [here](https://ubuntu.com/server/docs/install/autoinstall-quickstart), [here](https://cloudinit.readthedocs.io/en/latest/topics/datasources/nocloud.html), and [here](https://opensource.com/article/20/5/create-simple-cloud-init-service-your-homelab)).
As mentioned before, configuration files for the hosts can be found on the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/cloud-init) repository.

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

4. Ubuntu Server autoinstall expects three files to be accessible on the HTTP server: `user-data`, `vendor-data`, and `meta-data`.
    `user-data` corresponds to the previously discussed autoinstall configuration file, whereas `vendor-data` and `meta-data` correspond to files providing instance metadata we will not be using.
    However, these files need to be present even if empty, otherwise the autoinstall will fail.

### Deploy a metadata server using Docker

1. Clone the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig) repository:

        git clone git@github.com:KTH-EXPECA/TestbedConfig.git

2. Move into the `cloud-init` directory inside the repo:

        cd TestbedConfig/cloud-init

3. Inside this directory you will find subdirectories for each of the x86 management hosts (`cloudlet`, `database_server`, `management_server`) as well as a shell script `serve_cloud_init.sh` to automate serving of metadata.
    The script takes one of the aforementioned subdirectories and a port as arguments and sets up an NGINX web server serving metadata:

        ./serve_cloud_init.sh <directory> <port>

    For instance, to serve metadata for the `cloudlet` on port 80, one would do:

        ./server_cloud_init.sh ./cloudlet 80

4. To instead do this manually:
   
    - Serve metadata using the official NGINX Docker container image.
        Replace `$MDATADIR` with the directory containing metadata for the desired instance, and `$PORT` with the desired port on which to listen:

            docker run --rm -it -p $PORT:80 -v /path/to/TestbedConfig/cloud-init/$MDATADIR:/usr/share/nginx/html:ro nginx:latest

        Again, for example to serve metadata for the `cloudlet` on port 80, one would do:

            docker run --rm -it -p 80:80 -v /path/to/TestbedConfig/cloud-init/cloudlet:/usr/share/nginx/html:ro nginx:latest

    - Make sure the files are accessible from the network by visiting the IP address of the metadata server host from a web browser (don't forget to include the port in the URL).

    - This can also be tested on out the command line using `wget` or `curl` (replace `$ADDR` with the IP of the metadata server host and `$PORT` with the TCP port on which it is listening):

            wget $ADDR:$PORT/user-data

            curl -X GET $ADDR:$PORT/user-data

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

            linux /casper/vmlinux quiet autoinstall ds=nocloud-net\;s=http://$ADDR:$PORT/

    replacing `$ADDR` and `$PORT` with the address and port of the metadata server.

    *Note the escaped `;`, i.e. `\;`.*
    *This is only needed because GRUB interprets `;` as a command delimiter; in other setups (for instance when installing on a virtual machine) escaping `;` might not be necessary.*

3. Press `F10` to boot. The installer will connect to the metadata server and begin installation of the host based on the metadata obtained.
    Note that the install is not necessarily *fully* automatic, as there might be some sections in the autoinstall configuration files directly specified as interactive.
    In particular, storage setup usually needs special attention and is often specified as interactive.
    See the configuration files for details.

4. Once installation is finished, the installer will prompt to reboot.
    However, there seems to be a bug in the Ubuntu Server installer which causes it to crash at this point.
    Instead, when the reboot prompt appears, switch to TTY2 (`ALT + F2`) and reboot manually: `sudo reboot`.

5. The host will reboot and perform some final configuration of first boot, after which it will be ready to be used.
