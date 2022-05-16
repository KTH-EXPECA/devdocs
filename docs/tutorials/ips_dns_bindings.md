# Setting IP addresses and DNS bindings

## IP addresses

The management network is *statically* addressed (with the exception of a small block of addresses from `192.168.254.0` to `192.168.254.254`, which are dynamically assigned by the router).
IP addresses are set from the Ansible inventory using the [`static_management_net.yml`](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/static_management_net.yml) playbook.

See [our overview page for the management network](../technical_documents/management_overview.md) for details on the current setup.
Don't forget to update this page any time changes to the network are made.

## DNS

DNS is handled by a BIND9 (a.k.a. `named`) server instance running as a container on `thingol`.
These bindings are set from the Ansible inventory; in particular, see the [inventory](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/inventory/hosts.yml) and [`all` group variable files](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/inventory/group_vars/all.yml)

Run the [set_up_bind9_dns.yml](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/set_up_bind9_dns.yml) playbook on the DNS host to update the BIND9 configuration.
Note that this playbook merely generates all the necessary configurations for the server and outputs them to `/opt/bind9`.
After running, `cd` into this directory and check the files.
If everything looks correct, perform the following steps from the `/opt/bind9` directory to finalize configuration:

```bash
# temporarily stop systemd-resolved
$ sudo systemctl stop systemd-resolved

# delete the stale /etc/resolv.conf file
$ sudo rm /etc/resolv.conf

# overwrite the default systemd resolved.conf file with the newly generated one
$ sudo cp /opt/bind9/resolved.conf /etc/systemd/resolved.conf

# restart systemd-resolved
$ sudo systemctl start systemd-resolved

# symlink /etc/resolv.conf to systemd-resolved
$ sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf

# start the bind9 server
$ docker-compose up -d --force-recreate

# verify that /etc/resolv.conf has localhost and the network address of the dns server as dns
$ cat /etc/resolv.conf
# This file is managed by man:systemd-resolved(8). Do not edit.
#
# This is a dynamic resolv.conf file for connecting local clients directly to
# all known uplink DNS servers. This file lists all configured search domains.
#
# Third party programs must not access this file directly, but only through the
# symlink at /etc/resolv.conf. To manage man:resolv.conf(5) in a different way,
# replace this symlink by a static file or a different symlink.
#
# See man:systemd-resolved.service(8) for details about the supported modes of
# operation for /etc/resolv.conf.

nameserver 127.0.0.1
nameserver 192.168.0.3  # example
search expeca

# verify that systemd-resolved is using the local container as DNS server
$ sudo systemd-resolved --status
Global
       LLMNR setting: no                  
MulticastDNS setting: no                  
  DNSOverTLS setting: no                  
      DNSSEC setting: yes                 
    DNSSEC supported: yes                 
         DNS Servers: 127.0.0.1           
Fallback DNS Servers: 127.0.0.1           
          DNS Domain: ~.
...
Link 2 (eth0)
      Current Scopes: DNS        
DefaultRoute setting: yes        
       LLMNR setting: yes        
MulticastDNS setting: no         
  DNSOverTLS setting: no         
      DNSSEC setting: yes        
    DNSSEC supported: yes        
  Current DNS Server: 192.168.0.3
         DNS Servers: 192.168.0.3
          DNS Domain: expeca

# finally, test internal and external DNS resolution using dig
# note the SERVER section, should be 127.0.0.1#50 when digging from the DNS host
$ dig galadriel.expeca
...
;; ANSWER SECTION:
galadriel.expeca.	900	IN	A	192.168.1.1

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
...

$ dig kth.se
...
;; ANSWER SECTION:
kth.se.			5360	IN	A	130.237.28.40

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1)
...
```

### A note on changing the host on which the DNS server runs

To migrate the DNS server from one host to another, perform the following steps in order.

1. Modify the inventory and [set_up_bind9_dns.yml](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/set_up_bind9_dns.yml) playbook (and associated role) with the necessary variables.
2. Follow the steps above to bring up a copy of the DNS server on the **new** DNS server host.
3. Once the new DNS server is up, run the [`static_management_net.yml`](https://github.com/KTH-EXPECA/TestbedConfig/blob/master/ansible/static_management_net.yml) playbook.
   This will update the registered DNS server on all the hosts.
4. Make sure hosts are using the new DNS server instead of the old one using `dig`.
5. If everything looks fine, bring down the old DNS server container (`docker kill bind9_dns_server && docker rm bind9_dns_server` on the old DNS host).
6. Update the LAN configuration on the Cisco router to distribute the address of the new DNS server to DHCP clients as well.
