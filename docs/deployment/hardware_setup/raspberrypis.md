# Setting up the Raspberry Pi 4B clients

The easiest way to deploy an identical initial configuration to each of the 13 Raspberry Pi 4B clients is by completing the [initial steps](#initial-deployment-configuration) on one of the devices and then [cloning the SD-card to obtain 13 copies of the configuration.](#cloning-the-configuration)

## Initial deployment configuration

Follow the instructions on the [official Ubuntu website](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) to install Ubuntu Server in **headless** mode.

- Skip the *Install a desktop step*. We do not need a graphical interface, and installing and configuring one would just be a waste of resources and time.

- For using SSH you might have to create an empty file named `ssh` in the main boot directory

After installation, boot the device and either log into it physically or remote in over SSH to finalize the configuration.
See [this website](https://www.virtuability.com/posts/2020/08/get-started-with-ubuntu-20.04-on-raspberry-pi-4/) for instructions and tips for the following steps.

1. Set an appropriate hostname through the `hostnamectl` command, e.g.:

        sudo hostnamectl set-hostname expeca-rpi-1

2. Install `docker` and `docker-compose`:

    a. Refresh the repositories and make sure the system is fully upgraded.

        sudo apt update && sudo apt upgrade -y

    b. Install prerequisite software.

        sudo apt install -y \
            apt-transport-https \
            ca-certificates \
            curl \
            gnupg-agent \
            software-properties-common

    c. Add the Docker APT repository GPG key to the system.

        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    d. Add the Docker APT repository to the system software sources.

        sudo add-apt-repository \
            "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) \
            stable"

    e. Refresh the repositories and install docker and docker-compose.

        sudo apt update && \
        sudo apt install \
            docker-ce \
            docker-ce-cli \
            containerd.io \
            docker-compose

3. Make sure Python 3 is installed (it *should* be installed by default), along with necessary additional packages.

        sudo apt install -y python3 python3-pip python3-virtualenv

4. Install additional packages we might need.

        sudo apt install -y build-essential wget curl

5. Add additional groups and users.
   In the following, I (Manuel) will use my username (`molguin`) and SSH public key as examples; you should repeat the steps with your own username and SSH public key as well.
   For documentation of what SSH keys are and how to create and use them, refer to [this website](https://wiki.archlinux.org/title/SSH_keys).

    a. Make sure the necessary groups exist (you only need to do this once):

        $ sudo getent group sudo || sudo groupadd sudo
        ...
        $ sudo getent group docker || sudo groupadd docker
        ...
        $ sudo getent group wheel || sudo groupadd wheel
        ...

    c. Add a user with administrative privileges (you can replace the string after the `-c` flag with your own name when creating your own account).

        sudo useradd -m -c "Manuel Olguín Muñoz" -G sudo,wheel,docker molguin

    d. Set a password for the user account (for initial configuration of my `molguin` account, please just set the password to `molguin` as well).

        sudo passwd molguin

    e. Change into the newly created account.

        su molguin 

    f. Make sure the user can execute commands as an administrator.
    The following command should always return `root`:

        $ sudo whoami
        [sudo] password for molguin:
        root

    g. Make sure the SSH configuration folder exists for the user.

        mkdir -p ~/.ssh

    h. Insert the user's SSH public key into `~/.ssh/authorized_keys`.
    The following corresponds to my personal SSH public key, please include this one when creating my account (you can copy and paste the command).

        echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDUxwXjt0xpEXO2pOL5O+pkyqW8LH7oo1qJg9x+gtL8NwYBL2XUQ/HzHdXMF4p1ZBncLFWMIQYwb6+LPMWYD9nPLXA2umzF9Cp2TwOXaNibCGGV0GPraOC8FjHICop1fXgAeBHW4IiA5pvdujJNPnbIcEqqHPkYxpvbk2wCX4k2Vilxicg4ls23zWlmMJ4RJyYVu0ezVFv7ordGZEI5bpAFgMYNXtvoGEy/4U2zDX8fIQiTu62cOlloNqCb/QGJJ/XHsNE86TIWH8Gk4UPN7lk6omBOPdYb3YgGR/M6HsPxNwKQBVhN8DXXno8iBMsIahIAfkGwwHmB9EuomqxIt228a/ttOzZ8dx7sy5MK1u3mikJFkH+nypuZXD21hZUz3A8XDAXAJIuLbff4Mtdzsx6iBijKbxsGun3oHlQ6+8dDS9BnK+Ws25Bi0LQHvHKSc19mIMHpLElThn1B59h74B4W0pd0RvBWuuqdA01TqLYpUObJFSSwHJuTTCb27cW4zQE= molguin@kth.se" >> ~/.ssh/authorized_keys

    i. Log out of the new user account, back into the default `ubuntu` user.

        exit

6. After all user accounts have been created, you should log out of the `ubuntu` user and log back in with your own account.

7. Delete the default `ubuntu` user account.

        sudo userdel -r ubuntu

8. Configure SSH. Edit the OpenSSH server configuration file at `/etc/ssh/sshd_config` using `sudo` with either `vim` or `nano`, changing the following settings (only relevant lines are shown below).

        # ...
        Port 22
        # ...
        PubkeyAuthentication yes
        # ...
        PasswordAuthentication no
        PermitEmptyPasswords no
        ChallengeResponseAuthentication no
        # ...
        UsePAM yes
        
        AllowAgentForwarding yes
        AllowTCPForwarding yes
        # ...
        X11Forwarding no
        # ...
        TCPKeepAlive yes
        # ...

    **Note that if you are connected over SSH and you mess up the configuration somehow, this could lock you out of the Raspberry Pi, so double check the config file!**
    In particular, the above configuration disables "normal" password authentication - which is unsafe - and only allows authentication using SSH keys, so you should probably make sure your SSH key is working before applying these changes.

    After you are done editing the file, and you're certain everything is correct, enable and restart the SSH server (this will probably ask for a confirmation):

        sudo systemctl enable ssh.service && \
            sudo systemctl restart sshd && \
            sudo systemctl restart ssh && \

9. Verify that everything works by logging out and logging back in over SSH.

10. Enable overclocking.
    Edit the `/boot/config.txt` and `/boot/firmware/usercfg.txt` file with the following values:
    
    Note: the first file, `/boot/config.txt` might have deprecated.

        ...
        over_voltage=6
        arm_freq=2000
        force_turbo=1
        gpu_freq=600
        ...

11. Finally, verify that everything works once again by rebooting and then checking the core frequency and the temperature.

        # Install `vcgencmd` if not available
        sudo pip3 install setuptools
        sudo pip3 install vcgencmd
        sudo apt install libraspberrypi-bin
        
        # check core frequency in Hz, should return frequency(48)=2000478464 (2GHz)
        $ sudo vcgencmd measure_clock arm
        frequency(48)=2000478464

        # check SOC temperature, should ideally be below 50C
        $ sudo vcgencmd measure_temp
        temp=43.8'C

        # You can also check the complete configuration using the below command 
        
        $ sudo vcgencmd get_config int


### Cloning the configuration

1. Shut down the Raspberry Pi and extract the microSD card.
2. Insert the microSD card into your device.
3. Depending on your OS, proceed with the corresponding steps and then return here:

    - [Linux](#cloning-the-sd-card-on-linux) (Preferred)
    - [Mac OS X](#cloning-the-sd-card-on-mac-os-x)

4. At this point, the new microSD card contains an exact clone of the original configuration. Unmount and remove it, and reinsert it into the Raspberry Pi. 

    Note: There might be some additional steps required if the size of the clone SD card and cloned SD card are different.
    
5. Finally, make sure device-specific details are modified on the Pi itself.

    In particular, make sure to change the hostname to an appropriate one.
    This can be done through the `hostnamectl` command, e.g.:

        sudo hostnamectl set-hostname expeca-rpi-1

#### Cloning the SD card on Linux

The easiest way to obtain a completely identical bootable configuration from a single fully configured Raspberry Pi is through the command line on a Linux device:

1. Figure out the device ID of the card using `lsblk`.
    For example:

        $ lsblk
        NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
        ...
        sda           8:0    1  28,9G  0 disk 
        └─sda1        8:1    1  28.9G  0 part /run/media/user/KINGSTON

    In this case, the microSD card has been assigned the device ID `/dev/sda`.

2. Clone the raw contents of the microSD card (this includes filesystem structure and bootable sectors) to somewhere on your hard drive using `cat`:

        cat /dev/sdX > /path/to/somewhere/sdcard.img

    `/dev/sdX` here should be replaced with the device ID from the previous step.

    Alternatively, to be able to track progress, install `pv` (`sudo apt install pv`) and use it instead:

        pv /dev/sda > /path/to/somewhere/sdcard.img

3. Once cloning is done, unmount and remove the microSD card from the computer and insert the new microSD card the configuration is going to be copied to.
4. Clone the contents of the image we made in step 4 to the new microSD card. Note that this will completely overwrite the existing filesystem structure on the card.

    To do this, repeat step 3 to verify the device ID of the card, and then execute:

        cat /path/to/somewhere/sdcard.img | sudo dd of=/dev/sdX

    Alternatively, using `pv`:

        cat /path/to/somewhere/sdcard.img | sudo pv /dev/sdX

    Once this finishes, make sure the filesystem buffers are flushed and synchronized by running `sync` (this will potentially take a minute or two).

5. [Return to the general cloning instructions.](#cloning-the-configuration)

#### Cloning the SD card on Mac OS X

1. Figure out the device ID of the card using:

        diskutil list

	DeviceID is `rdisk4` in the below example. Here `r` denotes raw contents.

        $  ~ % diskutil list
        /dev/disk0 (internal):
        ...
        /dev/disk3 (synthesized):
        ...
        /dev/disk4 (external, physical):
        _:		TYPE NAME					SIZE			IDENTIFIER
        0:		FDisk_partition_scheme		*62.1 GB		disk4
        1:		Windows_FAT_32 ⁨boot		 268.4 MB		 disk4s1
        2:		Linux						61.8 GB			disk4s2

2. Clone the raw contents of the microSD card (this includes filesystem structure and bootable sectors) to somewhere on your hard drive. This might take some time.

        sudo dd if=/dev/<diskX> of=/Users/<username>/Desktop/Rpi.dmg bs=1m

3. Unmount SD card

        sudo diskutil unmountDisk /dev/<diskX>

4. Once cloning is done, unmount and remove the microSD card from the computer and insert the new microSD card the configuration is going to be copied to.
5. Clone the image contents after finding the correct device ID (refer to step 2). This might take some time.

        sudo dd if=/Users/<username>/Desktop/Rpi.dmg of=/dev/<rdiskX> bs=1m

6. If the above step shows a "Resource busy" error, unmount (only) the subvolumes and retry.

        sudo diskutil unmountDisk /dev/disk4s1
        sudo diskutil unmountDisk /dev/disk4s2

7. [Return to the general cloning instructions.](#cloning-the-configuration)