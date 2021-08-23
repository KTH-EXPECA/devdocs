# Workload Definition Schema

Testbed workloads are defined in YAML files containing information about the desired network configurations and computational workloads to be deployed.
This document describes the schema these files must follow, and will also serve as a guideline for the design and construction of the software necessary to parse these configurations.

## Example workload definition file

``` yaml
---
version: 1
workloads:
  wl1:
    client-device: generic
    num-clients: 3
    client-workload: cleave-client
    cloudlet-workload: cleave-backend
    network:
      base: wifi-ap
      client: wifi-native

client-workload-configs:
  cleave-client:
    image: cleave-plant:latest

backend-workload-configs:
  cleave-backend:
    image: cleave-controller:latest

radio-base-configs:
  wifi-ap:
    config-img: wifiap:latest
    params:
      ssid: testbed_wifi
      channel: auto

radio-client-configs:
  wifi-native:
    type: native
...
```

***Suggestion:*** Allow configuration in a single file OR in multiple files, for greater flexibility.

## Reference
