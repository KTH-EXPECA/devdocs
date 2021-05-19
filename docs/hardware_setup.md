# Hardware Setup

## x86 Hosts and Virtual Machines

TODO

## Raspberry Pis

The easiest way to deploy an identical initial configuration to each of the 13 Raspberry Pi 4B clients is by completing the [initial steps](#initial-deployment-configuration) on one of the devices and then [cloning the SD-card to obtain 13 copies of the configuration.](#cloning-the-configuration)

### Initial deployment configuration



### Cloning the configuration

The easiest way to obtain a completely identical bootable configuration from a single fully configured Raspberry Pi is through the command line on a Linux device:

1. Shut down the Raspberry Pi and extract the microSD card.
2. Insert the microSD card into your Linux device.
3. Figure out the device ID of the card using `lsblk`.
    For example:

        $ lsblk
        NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
        ...
        sda           8:0    1  28,9G  0 disk 
        └─sda1        8:1    1  28.9G  0 part /run/media/user/KINGSTON

    In this case, the microSD card has been assigned the device ID `/dev/sda`.

4. Clone the raw contents of the microSD card (this includes filesystem structure and bootable sectors) to somewhere on your hard drive using `cat`:

        cat /dev/sdX > /path/to/somewhere/sdcard.img

    `/dev/sdX` here should be replaced with the device ID from the previous step.

    Alternatively, to be able to track progress, install `pv` (`sudo apt install pv`) and use it instead:

        pv /dev/sda > /path/to/somewhere/sdcard.img

5. Once cloning is done, unmount and remove the microSD card from the computer and insert the new microSD card the configuration is going to be copied to.
6. Clone the contents of the image we made in step 4 to the new microSD card. Note that this will completely overwrite the existing filesystem structure on the card.

    To do this, repeat step 3 to verify the device ID of the card, and then execute:

        cat /path/to/somewhere/sdcard.img | sudo dd of=/dev/sdX

    Alternatively, using `pv`:

        cat /path/to/somewhere/sdcard.img | sudo pv /dev/sdX

    Once this finishes, make sure the filesystem buffers are flushed and synchronized by running `sync` (this will potentially take a minute or two).

7. At this point, the new microSD card contains an exact clone of the original configuration. Unmount and remove it, and reinsert it into the Raspberry Pi.
8. Finally, make sure device-specific details are modified on the Pi itself.

    In particular, make sure to change the hostname to an appropriate one by editing `/etc/hostname` and `/etc/hosts`. For details on doing this, [see here](https://wiki.archlinux.org/title/Network_configuration#Set_the_hostname).

