# Time synchronization

Time synchronization within the cluster is achieved through the [Network Time Protocol (NTP)](http://www.ntp.org/).

## Setting up the NTP server

An Ansible Playbook YAML file for automatic set-up of the NTP server can be found in the [KTH-EXPECA/TestbedConfig](https://github.com/KTH-EXPECA/TestbedConfig/tree/master/services/ntp/playbooks/set_up_ntp.yml) repository.
Run it by executing `ansible-playbook set_up_ntp.yml` on the command line.

The playbook contains two plays:

1. First it sets up an NTP server running on Docker, using the [cturaa/ntp](https://hub.docker.com/r/cturra/ntp) container image.
   This image binds to port `123:123/udp` to provide time services to network-local clients, while at the same time synchronizing upstream with Google's time servers.

2. Next, all hosts on the network are configured to synchronize to the NTP server.
   This is achieved through configuration of `systemd`'s built-in time-synchronization daemon, `timesyncd`.
   In practical terms, this play writes a configuration file at `/etc/systemd/timesyncd.conf` and then restarts `timesyncd`.

## Debugging

Use Ansible together with the `ntpdate` command to check the synchronization status across the cluster:

```console
$ ansible all -a 'ntpdate -q thingol.expeca'
192.168.1.102 | CHANGED | rc=0 >>
server 192.168.1.100, stratum 2, offset -0.000110, delay 0.02621
21 Jun 17:10:21 ntpdate[109322]: adjust time server 192.168.1.100 offset -0.000110 sec
...
```

If `ntpdate` instead outputs the following, it is likely that the clock is not yet synchronized:

```console
$ ansible all -a 'ntpdate -q thingol.expeca'
192.168.1.102 | CHANGED | rc=0 >>
server 192.168.1.100, stratum 2, offset -0.000110, delay 0.02621
21 Jun 17:10:21 ntpdate[109322]: no server suitable for synchronization found
...
```

In this case, wait a while before retrying, and the problem should sort itself out.
