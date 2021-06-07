# Setting up the Raspberry Pi 4B clients

The easiest way to deploy an identical initial configuration to each of the 13 Raspberry Pi 4B clients is by completing the [initial steps](#initial-deployment-configuration) on one of the devices and then [cloning the SD-card to obtain 13 copies of the configuration.](#cloning-the-configuration)
To avoid issues with mismatched SD-card sizes when cloning, make sure to perform the initial setup on a Raspberry Pi with an SD-card of the smallest size available.
That is, if you for instance have both 32 and 64 GB cards, perform the setup on a 32 GB card.
This way, the cards can still be cloned even when the storage sizes do not match.

## Initial deployment configuration

Follow the instructions on the [official Ubuntu website](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) to install Ubuntu Server in **headless** mode.

- Skip the *Install a desktop step*. We do not need a graphical interface, and installing and configuring one would just be a waste of resources and time.

- For using SSH you might have to create an empty file named `ssh` in the main boot directory

After installation, boot the device and either log into it physically or remote in over SSH to finalize the configuration.
See [this website](https://www.virtuability.com/posts/2020/08/get-started-with-ubuntu-20.04-on-raspberry-pi-4/) for instructions and tips for the following steps.

1. Set an appropriate hostname through the `hostnamectl` command, e.g.:

        sudo hostnamectl set-hostname workload-client-01

2. Install `docker` and `docker-compose`:

    1. Refresh the repositories and make sure the system is fully upgraded.

            sudo apt update && sudo apt upgrade -y

    2. Install prerequisite software.

            sudo apt install -y \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg-agent \
                software-properties-common

    3. Add the Docker APT repository GPG key to the system.

            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    4. Add the Docker APT repository to the system software sources.

            sudo add-apt-repository \
                "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
                $(lsb_release -cs) \
                stable"

    5. Refresh the repositories and install docker and docker-compose.

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

5. Add the special `expeca` user we will use for deployment and management.
    Since the Raspberry Pis are only intended as remote clients, the `expeca` user will be the only user account on them, and it will have full password-less sudo access.
    To ensure that the systems are secure in this setup, we will only allow SSH access using [Public Key authentication](https://wiki.archlinux.org/title/SSH_keys).

    1. Make sure the necessary user groups exist:

            $ sudo getent group sudo || sudo groupadd sudo
            ...
            $ sudo getent group docker || sudo groupadd docker
            ...
            $ sudo getent group wheel || sudo groupadd wheel
            ...

    2. Add the `expeca` user account:

            sudo useradd -m -c "EXPECA" -G sudo,wheel,docker expeca

    3. Allow the `expeca` user to execute any command with sudo without having to enter a password.

            $ sudo -i

            $ echo "expeca ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/90-expeca

            $ exit

    4. Make sure the SSH configuration folder exists for the user and that it has the right permissions.

            $ sudo mkdir -p /home/expeca/.ssh

            $ sudo chown expeca /home/expeca/.ssh

            $ sudo chmod 700 /home/expeca/.ssh

    5. Insert the SSH public keys into `/home/expeca/.ssh/authorized_keys`.
        These keys correspond to the keys for the members of the team; Vishnu, Samie, Neel, and Manuel:

            $ sudo -i

            $ cat <<EOT >> /home/expeca/.ssh/authorized_keys
            ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC9BlYPQYi4ZRaSJjvCMX0y2cPx2TQbUfTG+DTthAKeV/B/kaNQ6+smYOAQuJ+ai0Z+U+Ihf2r3guF7c/eo8xUWnG7p41jZ0MPqa5HjuUWUkC2p52OVn5y5Zbvdp0QOECjdU1+jBlAebFjEeEKy/ArwnTdM1WHh7uyA9Y8hMEMkQNJPEjKQSd9sWczN+NXqTs8KblcihRrbu9D+qkl39gnCXagvdPKPBeNxHk8XvUrEuSMqLoEzLNr8p0RXKRTtQGAMUna4sfJFajau+m1LyOxLuT6DbXwZdybXSxY+2sfrC+F5IwdzEWI6puxE9OkrcZHPjLKioeIS6IGFkHhNxylYyKb7mlpcieH2yxZQ0bBfbo/KMsh4ozb9N7JVzL4az2ij4zSJLVSHnBSddlW1edOzY6jQyfxHZSaVgZJe/inOW9i05wqJ1biT8EIG4qyqLFPvCNolAASmLR14DAegUMsVVSi/mg7n3sHnjoqDKwtw47G/DmZn1H/oPlzzF29B2Hk= vnmo@vnmo-mbp
            ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCkSZ/0ZPfq/zUzLObaqSRHd1SM4HeqqZjt73b7JAx/m6iJNrGT5mlNZToA22q+Xhdr4Wj2xAQT/YI2jKkpYQfSL6EKrHX6I9jbg86EZX3jHT4t6E1zu58EQJHi5Ll7bWKxy2Uw4i2k44OkyHGKFlWXGJAp6njKqxcu7Df4WkJNIFt6SH7qH7W/lkjq6+Z74uefe5jh5QwU/2ow48aID/wvMWENROYgvjAVndBu6cNH4Dm+nYYN5Y7F/N8qGu+n+cXPvpHCPnU2Hwg2peVPGzSNmCpsz79kclcYEoUnb+LB94xxRXziOkxWeuzSICKWaHnlB/DwKEiajBmW8yky09NZz819yB1zem8VSuehLGSRyPCa2pwx3RycBt7D/auEOFh/AJKG+2GNKa8dzScM0sq+t/OcAZCl2n1pjtVd6B5FcTwaQjgBjCRenmIVhcvt5rA+nGaoA2pTE2+trVDflRIIjiLWQpde4QokjlIFNfHPxhEYorHNPYf1ayruiv6Gvrs= ssmos@Samies-MacBook-Pro-KTH.local
            ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMnVLjPX1cOaERQ0sjqpiHFXTSorSpTtW7JJTl/hEqKS neelabhro16171@iiitd.ac.in
            ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDUxwXjt0xpEXO2pOL5O+pkyqW8LH7oo1qJg9x+gtL8NwYBL2XUQ/HzHdXMF4p1ZBncLFWMIQYwb6+LPMWYD9nPLXA2umzF9Cp2TwOXaNibCGGV0GPraOC8FjHICop1fXgAeBHW4IiA5pvdujJNPnbIcEqqHPkYxpvbk2wCX4k2Vilxicg4ls23zWlmMJ4RJyYVu0ezVFv7ordGZEI5bpAFgMYNXtvoGEy/4U2zDX8fIQiTu62cOlloNqCb/QGJJ/XHsNE86TIWH8Gk4UPN7lk6omBOPdYb3YgGR/M6HsPxNwKQBVhN8DXXno8iBMsIahIAfkGwwHmB9EuomqxIt228a/ttOzZ8dx7sy5MK1u3mikJFkH+nypuZXD21hZUz3A8XDAXAJIuLbff4Mtdzsx6iBijKbxsGun3oHlQ6+8dDS9BnK+Ws25Bi0LQHvHKSc19mIMHpLElThn1B59h74B4W0pd0RvBWuuqdA01TqLYpUObJFSSwHJuTTCb27cW4zQE= molguin@kth.se
            EOT

            $ exit
    
    6. Make sure the `authorized_keys` file is owned by the `expeca` user and that it has correct permissions:

            $ sudo chown expeca /home/expeca/.ssh/authorized_keys

            $ sudo chmod 644 /home/expeca/.ssh/authorized_keys

6. At this point you should make sure the configuration for the new `expeca` user is correct by attempting to SSH into the Raspberry Pi using your private key:

            ssh -i .ssh/$YOUR_PRIVATE_KEY -oPasswordAuthentication=no -oPubkeyAuthentication=yes expeca@$RPI_ADDRESS 

    After login, make sure `expeca` can execute commands without asking for a password: `sudo whoami` should immediately return `root`.

7. If the previous step was succesful, proceed with the following steps *as the `expeca` user*.
    Otherwise, review step 5 to make sure the configuration is absolutely correct (in particular, the permissions for the `.ssh/` directory and the `.ssh/authorized_keys` file can be tricky to get right).

8.  Delete the default `ubuntu` user account (again, you'll need to log out from your initial command line and log in again as the `expeca` user).

        sudo userdel -r ubuntu

9.  Configure SSH:

        $ sudo -i 

        $ cat <<EOT > /etc/ssh/sshd_config
        Include /etc/ssh/sshd_config.d/*.conf
        Port 22
        PermitRootLogin no
        StrictModes yes
        PubkeyAuthentication yes
        # To disable tunneled clear text passwords, change to no here!
        PasswordAuthentication no
        PermitEmptyPasswords no
        ChallengeResponseAuthentication no
        UsePAM yes
        AllowAgentForwarding yes
        AllowTcpForwarding yes
        X11Forwarding yes
        PrintMotd no
        PrintLastLog yes
        TCPKeepAlive yes
        # Allow client to pass locale environment variables
        AcceptEnv LANG LC_*
        # override default of no subsystems
        Subsystem	sftp	/usr/lib/openssh/sftp-server
        EOT

        $ exit

    **Note that if you are connected over SSH and you mess up the configuration somehow, this could lock you out of the Raspberry Pi, so double check the config file!**

    After you are done editing the file, and you're certain everything is correct, enable and restart the SSH server (this will probably ask for a confirmation):

        sudo systemctl enable ssh.service && sudo systemctl restart ssh

10. Verify that everything works by logging out and logging back in over SSH.

11. Enable overclocking.
    Edit the `/boot/config.txt` and `/boot/firmware/usercfg.txt` files with the following values:
    
    *Note: the first file, `/boot/config.txt`, might be deprecated in Ubuntu 20.04*

        ...
        over_voltage=6
        arm_freq=2000
        force_turbo=1
        gpu_freq=600
        ...

12. Finally, verify that everything works once again by rebooting and then checking the core frequency and the temperature.

    1. Install `vcgencmd` if it's not available:

            $ which vcgencmd 
            vcgencmd not found

            $ sudo apt update && sudo apt install python3-setuptools libraspberrypi-bin -y

            $ sudo pip3 install vcgencmd

    2. Check the core frequency, it should return `frequency(48)=2000478464` (2GHz):

            $ sudo vcgencmd measure_clock arm
            frequency(48)=2000478464

    3. Check SOC temperature, should ideally be below 50C:
        
            $ sudo vcgencmd measure_temp
            temp=43.8'C

    4. You can also check the complete configuration using the below command 
        
            $ sudo vcgencmd get_config int


### Cloning the configuration

1. Shut down the Raspberry Pi and extract the microSD card.
2. Insert the microSD card into your device.
3. Depending on your OS, proceed with the corresponding steps and then return here:

    - [Linux](#cloning-the-sd-card-on-linux) (Preferred)
    - [Mac OS X](#cloning-the-sd-card-on-mac-os-x)

4. At this point, the new microSD card contains an exact clone of the original configuration. Unmount and remove it, and reinsert it into the Raspberry Pi.
    Note: There might be some additional steps required if the sizes of the SD cards are different (TODO).
    
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

        $> ~ % diskutil list
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