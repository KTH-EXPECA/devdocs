# Management Network Overview

This page details the current setup for the management network, used for the *alpha* version of the testbed.

**Please read this page carefully before making changes to the network infrastructure**


![](./assets/ManagementNetworkAlpha.png)

The testbed can be accessed from the internet at [`testbed.expeca.proj.kth.se`](ssh://testbed.expeca.proj.kth.se:2222) or [`130.237.53.70`](ssh://130.237.53.70:2222), on SSH port `2222`.

The management network is statically addressed using a `192.168.0.0/16` CIDR block.
We use sub-ranges under this block to semantically separate devices on the network:

- `192.168.0.[1-255]`: reserved for network infrastructure devices, such as routers, switches, and gateways.
- `192.168.1.[0-255]`: reserved for "core" functionality devices, such as `galadriel` and `elrond`.
- `192.168.2.[0-255]`: reserved for radio hosts.
- `192.168.3.[0-255]`: reserved for workload clients.
- `192.168.4.[0-255]`: reserved for Software-Defined Radios.
- `192.168.255.[0-254]`: reserved for external devices (e.g. personal laptops) connected to the network.
  *NOTE: This range is assigned dynamically by the router, using DHCP.*

## IP address bindings

| FQDN 	| IP 	| Function(s) 	|
|---	|---	|---	|
| `cirdan.expeca` 	| `192.168.0.1` 	| Gateway, NAT, firewall 	|
| `glorfindel.expeca` 	| `192.168.0.2` 	| Managed workload network switch 	|
| `thingol.expeca` 	| `192.168.0.3` 	| DNS server, NTP server, VPN gateway 	|
| `olwe.expeca` 	| `192.168.0.4` 	| VPN gateway 	|
| `galadriel.expeca` 	| `192.168.1.1` 	| Ainur host 	|
| `elrond.expeca` 	| `192.168.1.2` 	| Cloudlet 	|
| `fingolfin.expeca` 	| `192.168.2.1` 	| SDR host 	|
| `finarfin.expeca` 	| `192.168.2.1` 	| SDR host 	|
| `workload-client-[00-12].expeca` 	| `192.168.3.[0-12]` 	| Workload client 	|

<!-- ## Physical Setup

![](./assets/AlphaHardwareSetup_Annotated.png)

|  	| Device 	| Role 	| FQDN 	| IP 	| Network<br>Services 	|
|-	|-	|-	|-	|-	|-	|
| **1** 	| Cisco RV160 Router 	| Ingress Router 	| cirdan.expeca 	| 192.168.1.1 	| NAT, 	|
| **2** 	| Intel NUC8i7HNK 	| Management 	| galadriel.expeca 	| 192.168.1.2 	| DHCP, DNS, NTP |
| **3** 	| DELL Optiplex 7060 	| Cloudlet 	| elrond.expeca 	| 192.168.1.4 	| - |
| **4** 	| DELL Optiplex 9020 	| DB/Storage 	| celeborn.expeca 	| 192.168.1.3  | - |
| **5** 	| Custom Build 1 	| Radio Host 1 	| fingolfin.expeca 	| 192.168.1.51 	| - 	|
| **6** 	| Custom Build 2 	| Radio Host 2 	| finarfin.expeca 	| 192.168.1.52 	| - 	|
| **7** 	| NETGEAR JGS524v2 Switch 	| Management<br>Network Switch 	| - 	| - 	| - 	|
| **8** 	| 13x Raspberry Pi 4B 	| Workload<br>Clients 	| workload-client-[00:12].expeca 	| 192.168.1.1[00:12] 	| - 	|
| **9** 	| Cisco SG220-50 Switch	| Workload<br>Network Switch 	| glorfindel.expeca 	| 192.168.1.5 	| - 	| -->
