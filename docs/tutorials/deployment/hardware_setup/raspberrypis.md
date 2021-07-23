# Setting up the Raspberry Pi 4B clients

The easiest way to deploy an identical initial configuration to each of the 13 Raspberry Pi 4B clients is by completing the [initial steps](#initial-deployment-configuration) on one of the devices and then [cloning the SD-card to obtain 13 copies of the configuration.](#cloning-the-configuration)
To avoid issues with mismatched SD-card sizes when cloning, make sure to perform the initial setup on a Raspberry Pi with an SD-card of the smallest size available.
That is, if you for instance have both 32 and 64 GB cards, perform the setup on a 32 GB card.
This way, the cards can still be cloned even when the storage sizes do not match.

## Initial deployment configuration

The initial, barebones configuration only considers getting the Raspberry Pi up and running connected to the network.
Provisioning of the final configuration will be handled over the network with Ansible.

### Install Ubuntu Server

Follow the instructions on the [official Ubuntu website](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) to install Ubuntu Server in **headless** mode.

- Skip the *Install a desktop step*. We do not need a graphical interface, and installing and configuring one would just be a waste of resources and time.

- For using SSH you might have to create an empty file named `ssh` in the main boot directory

After installation, boot the device and either log into it physically or remote in over SSH to continue.

### Enable the USB Ethernet adapter

Edit the `/etc/netplan/50-cloud-init.yaml` file and add the following to networks -> ethernets:

``` text
...
eth1:
    dhcp4: true
    optional: true
...
```

And then apply the change by running `sudo netplan apply`

### Configure the `ubuntu` user for remote access

By default, the Ubuntu Server installation comes with a single `ubuntu` user.
We will prepare this user for full provisioning over Ansible.

1. Verify that the password is set to `ubuntu`:

    ``` console
    $ sudo passwd ubuntu
    ...
    New password: 
    Retype new password: 
    passwd: password updated successfully
    ```

2. Configure and enable the SSH server.
      1. Open `/etc/ssh/sshd_config` with a text editor like `vim` and make sure `Port` is set to `22` and `PasswordAuthentication` to `yes`.
      2. Enable the SSH server:

        ``` console
        $ sudo systemctl enable ssh
        ...
        $ sudo systemctl restart ssh
        ...
        ```

At this point, the Raspberry Pi is ready for full provisioning and configuration over the network with Ansible.
[Clone the configuration to the remaining Pis](#cloning-the-configuration), connect them to the management network using the USB adapter, and then [provision them using Ansible](#final-configuration-using-ansible).

### Cloning the configuration

1. Shut down the Raspberry Pi and extract the microSD card.
2. Insert the microSD card into your device.
3. Depending on your OS, proceed with the corresponding steps and then return here:

    - [Linux](#cloning-the-sd-card-on-linux) (Preferred)
    - [Mac OS X](#cloning-the-sd-card-on-mac-os-x)

4. At this point, the new microSD card contains an exact clone of the original configuration. Unmount and remove it, and reinsert it into the Raspberry Pi.
    <!-- Note: There might be some additional steps required if the sizes of the SD cards are different. -->

5. Finally, make sure device-specific details are modified on the Pi itself.

    In particular, make sure to change the hostname to an appropriate one.
    This can be done through the `hostnamectl` command, e.g.:

    ``` console
    sudo hostnamectl set-hostname expeca-rpi-1
    ```

#### Cloning the SD card on Linux

The easiest way to obtain a completely identical bootable configuration from a single fully configured Raspberry Pi is through the command line on a Linux device:

1. Figure out the device ID of the card using `lsblk`.
    For example:

    ``` console
    $ lsblk
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    ...
    sda           8:0    1  28,9G  0 disk 
    └─sda1        8:1    1  28.9G  0 part /run/media/user/KINGSTON
    ```

    In this case, the microSD card has been assigned the device ID `/dev/sda`.

2. Clone the raw contents of the microSD card (this includes filesystem structure and bootable sectors) to somewhere on your hard drive using `cat`:

    ``` console
    cat /dev/sdX > /path/to/somewhere/sdcard.img
    ```

    `/dev/sdX` here should be replaced with the device ID from the previous step.

    Alternatively, to be able to track progress, install `pv` (`sudo apt install pv`) and use it instead:

    ``` console
    pv /dev/sda > /path/to/somewhere/sdcard.img
    ```

3. Once cloning is done, unmount and remove the microSD card from the computer and insert the new microSD card the configuration is going to be copied to.
4. Clone the contents of the image we made in step 4 to the new microSD card. Note that this will completely overwrite the existing filesystem structure on the card.

    To do this, repeat step 3 to verify the device ID of the card, and then execute:

    ``` console
    cat /path/to/somewhere/sdcard.img | sudo dd of=/dev/sdX
    ```

    Alternatively, using `pv`:

    ``` console
    cat /path/to/somewhere/sdcard.img | sudo pv /dev/sdX
    ```

    Once this finishes, make sure the filesystem buffers are flushed and synchronized by running `sync` (this will potentially take a minute or two).

5. [Return to the general cloning instructions.](#cloning-the-configuration)

#### Cloning the SD card on Mac OS X

1. Figure out the device ID of the card using:

    ``` console
    diskutil list
    ```

    DeviceID is `rdisk4` in the below example. Here `r` denotes raw contents.

    ``` console
    $> ~ % diskutil list
    /dev/disk0 (internal):
    ...
    /dev/disk3 (synthesized):
    ...
    /dev/disk4 (external, physical):
    _:      TYPE NAME                    SIZE            IDENTIFIER
    0:      FDisk_partition_scheme        *62.1 GB        disk4
    1:      Windows_FAT_32 ⁨boot         268.4 MB         disk4s1
    2:      Linux                        61.8 GB            disk4s2
    ```

2. Clone the raw contents of the microSD card (this includes filesystem structure and bootable sectors) to somewhere on your hard drive. This might take some time.

    ``` console
    sudo dd if=/dev/<diskX> of=/Users/<username>/Desktop/Rpi.dmg bs=1m
    ```

3. Unmount SD card

    ``` console
    sudo diskutil unmountDisk /dev/<diskX>
    ```

4. Once cloning is done, unmount and remove the microSD card from the computer and insert the new microSD card the configuration is going to be copied to.
5. Clone the image contents after finding the correct device ID (refer to step 2). This might take some time.

    ``` console
    sudo dd if=/Users/<username>/Desktop/Rpi.dmg of=/dev/<rdiskX> bs=1m
    ```

6. If the above step shows a "Resource busy" error, unmount (only) the subvolumes and retry.

    ``` console
    $ sudo diskutil unmountDisk /dev/disk4s1
    ...
    $ sudo diskutil unmountDisk /dev/disk4s2
    ...
    ```

7. [Return to the general cloning instructions.](#cloning-the-configuration)

## Final configuration using Ansible

Once the Raspberry Pi clients have been prepared and connected to the network, we can easily configure them in parallel using Ansible.
The following instructions must be followed from `galadriel`.

**Prerequisite**: The static DHCP bindings of the management network need to have been configured. <!-- TODO: Add link!! -->

1. If it's not already present, clone the `KTH-EXPECA/TestbedConfig` repository and `cd` into it:

    ``` console
    $ git clone git@github.com:KTH-EXPECA/TestbedConfig.git
    ...
    $ cd TestbedConfig
    ```

    If you've previously cloned this repository, make sure it's updated to the latest revision.

    ``` console
    $ cd TestbedConfig
    ./TestbedConfig
    $ git pull
    ...
    ```

2. Make sure the newly prepared Raspberry Pis are visible to `galadriel`:

    ``` console
    $ ansible all -i '<ip addresses>' -m ping --user ubuntu -k -K
    ... 
    ```

    Replace `<ip addresses>` with the IPs of the new Raspberry Pis, end with a comma.
    E.g. if Raspberry Pis 3, 4, and 5 were reprovisioned, the command would read:

    ``` console
    $ ansible all -i '192.168.1.103,192.168.1.104,192.168.1.105,' -m ping --user ubuntu -k -K
    ... 
    ```

    Again, note the comma at the end of the list of IP addresses.

    The `-k -K` flags will instruct Ansible to ask for passwords; simply input `ubuntu` as preconfigured.

3. Run the `ansible/provision_raspberry_pis.yml` playbook.
    This playbook does a number of things:
    1. Creates the `expeca` user, which will be used as administration account going forward, and adds the necessary SSH keys to it.
    2. Configures SSH to only allow public-key authentication.
    3. Deletes the `ubuntu` user as it will not be used anymore.
    4. Configures the system, installing necessary software and overclocking the CPU.
    5. Finally, reboots the devices.

    To run the playbook, execute:

    ``` console
    $ ansible-playbook -i '<ip addresses>' ansible/provision_raspberry_pis.yml -k -K
    ...
    ```

    Again, replace `<ip addresses>` with the IPs of the new Raspberry Pis, end with a comma.
