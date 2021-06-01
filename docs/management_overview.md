# Management Network and Hardware Overview

This page details the current setup for the management network, used for the *alpha* version of the testbed.

## Physical Setup

![](../../assets/AlphaHardwareSetup_Annotated.png)

|  	| Device 	| Role 	| FQDN 	| IP 	| Services 	|
|-	|-	|-	|-	|-	|-	|
| **1** 	| Cisco RV160 Router 	| Ingress Router 	| cirdan.expeca.org 	| 192.168.1.1 	| NAT, DHCP 	|
| **2** 	| Intel NUC8i7HNK 	| Management 	| galadriel.expeca.org 	| 192.168.1.100 	| Ansible, NTP, DNS 	|
| **3** 	| DELL Optiplex 7060 	| Cloudlet 	| elrond.expeca.org 	| 192.168.1.102 	| - 	|
| **4** 	| DELL Optiplex 9020 	| DB/Storage 	| celeborn.expeca.org 	| 192.168.1.101 	| Fluentd, Database (WIP) 	|
| **5** 	| Custom Build 1 	| Radio Host 1 	| fingolfin.expeca.org 	| 192.168.1.51 	| - 	|
| **6** 	| Custom Build 2 	| Radio Host 2 	| finarfin.expeca.org 	| 192.168.1.52 	| - 	|
| **7** 	| NETGEAR JGS524v2 Switch 	| Management<br>Network Switch 	| - 	| - 	| - 	|
| **8** 	| 13x Raspberry Pi 4B 	| Workload<br>Clients 	| workload-client-[01:13].expeca.org 	| 192.168.1.2[00:12] 	| - 	|

## Network Setup

<img src="../../assets/WorkloadNetworkAlpha.png" width="450">
