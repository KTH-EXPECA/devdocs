# Hardware Inventory

## x86 Hosts

| Count 	| Device 	| Current Role 	| CPU Model 	| Number of Cores 	| Max. Turbo<br>Frequency 	| Total RAM 	| RAM Type 	| RAM Frequency 	| Storage 	|
|-	|-	|-	|-	|-	|-	|-	|-	|-	|-	|
| 1 	| Intel<br>NUC 	| Management<br>Server 	| Intel Core<br>i7-8705G 	| 4 (8 threads) 	| 3.1 GHz 	| 32 GB<br>(2 x 16 GB) 	| SO-DIMM<br>DDR4 	| 2400 MHz 	| 240 GB NVMe SSD 	|
| 1 	| DELL <br>Optiplex<br>7060 	| Workload<br>Cloudlet 	| Intel Core<br>i7-8700 	| 6 (12 threads) 	| 3.2 GHz 	| 32 GB<br>(4 x 8 GB) 	| DIMM<br>DDR4 	| 2666 MHz 	| 512 GB NVMe SSD 	|
| 1 	| DELL<br>Optiplex<br>9020 	| DB/Storage<br>Server 	| Intel Core<br>i7-4770 	| 4* (8 threads) 	| 3.4 GHz 	| 32 GB<br>(4 x 8 GB) 	| DIMM<br>DDR3 	| 1600 MHz 	| 250 GB SATA 2.5" SSD +<br>480 GB SATA 2.5" SSD 	|
| 2 	| Custom<br>Builds 	| Radio Hosts 	| Intel Core<br>i9-10980XE 	| 18 (36 threads) 	| 3.00GHz 	| 32 GB<br>(4 x 8GB) 	| DIMM<br>DDR4 	| 2666 MHz 	| 1 TB NVMe SSD 	|

*\* For some reason, Ubuntu recognizes it as having 8 **physical** cores instead of virtual ones. Could be due to the age of the processor.*

## ARM Hosts

| Count 	| Device 	| Current Role 	| CPU Model 	| Number of Cores 	| Max. Turbo<br>Frequency 	| Total RAM 	| RAM Type 	| RAM Frequency 	| Storage 	|
|-	|-	|-	|-	|-	|-	|-	|-	|-	|-	|
| 13 	| Raspberry Pi 4B 	| Workload Clients 	| Cortex-A72 (ARM v8) 	| 4 (4 threads) 	| 1.5 GHz** 	| 8 GB 	| LPDDR4 SDRAM 	| 3200 MHz 	| 32/64 GB microSD 	|

*\*\* Overclockable to 2 GHz with proper cooling.*

## Networking Equipment 

| Count 	| Device 	| Current Role 	| Ports 	|
|-	|-	|-	|-	|
| 1 	| Cisco RV160 Router 	| Ingress Router 	| 1x 1Gbps RJ-45 SFP Eth (WAN)<br>4x 1Gbps RJ-45 Eth 	|
| 1 	| NETGEAR JGS524v2 Switch 	| Management Network <br>Switch 	| 24x 1Gbps RJ-45 Eth 	|