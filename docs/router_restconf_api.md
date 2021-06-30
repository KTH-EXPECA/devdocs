# Router RESTCONF API Overview

This is a brief overview of the RESTCONF API of the Cisco RV160 VPN router.
This API does not seem to follow the standards for RESTCONF I've found online:

- It sits behind port `443` listening on `/api`.
- It only responds to special `Accept` headers:
  
    - `application/vnd.yang.api+json` when querying the API itself.
    - `application/vnd.yang.datastore+json` when querying collections such as `running` or `startup`.
    - `application/vnd.yang.data+json` when checking/setting the values for a specific configuration such as `ciscosb-lan-dhcp:static-dhcp`.

- The Ansible RESTCONF modules do not seem to be compatible with it.

``` bash
$ curl -H "Accept: application/vnd.yang.api+json" \
  -k https://192.168.1.1:443/api \
  -u "expeca:expeca" | python3 -m json.tool
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4842  100  4842    0     0  23970      0 --:--:-- --:--:-- --:--:-- 23852
{
    "api": {
        "version": "0.5",
        "config": {},
        "running": {},
        "startup": {},
        "operational": {},
        "operations": {
            "ciscosb-certs:generate-cert": "/api/operations/ciscosb-certs:generate-cert",
            "ciscosb-certs:generate-csr": "/api/operations/ciscosb-certs:generate-csr",
            "cisco-email:test-connectivity": "/api/operations/cisco-email:test-connectivity",
            "ciscosb-file:file-download": "/api/operations/ciscosb-file:file-download",
            "ciscosb-file:file-upload": "/api/operations/ciscosb-file:file-upload",
            "ciscosb-file:file-copy": "/api/operations/ciscosb-file:file-copy",
            "ciscosb-file:file-list": "/api/operations/ciscosb-file:file-list",
            "ciscosb-file:file-delete": "/api/operations/ciscosb-file:file-delete",
            "fw-port-forwarding-rules:delete-upnp-rule": "/api/operations/fw-port-forwarding-rules:delete-upnp-rule",
            "fw-session-timeout:clear-connections": "/api/operations/fw-session-timeout:clear-connections",
            "ciscosb-image:check-latest-version": "/api/operations/ciscosb-image:check-latest-version",
            "ciscosb-interfaces:reset-counters": "/api/operations/ciscosb-interfaces:reset-counters",
            "ciscosb-interfaces:reset-wifi-counters": "/api/operations/ciscosb-interfaces:reset-wifi-counters",
            "ciscosb-interfaces:refresh-counters": "/api/operations/ciscosb-interfaces:refresh-counters",
            "ciscosb-lan-dhcp:dhcp-release-binding": "/api/operations/ciscosb-lan-dhcp:dhcp-release-binding",
            "ciscosb-qos-policy:reset-qos-statistics": "/api/operations/ciscosb-qos-policy:reset-qos-statistics",
            "ciscosb-routing:update-routes": "/api/operations/ciscosb-routing:update-routes",
            "ciscosb-switch-qos:reset-switch-qos-statistics": "/api/operations/ciscosb-switch-qos:reset-switch-qos-statistics",
            "ciscosb-syslog:query-syslog": "/api/operations/ciscosb-syslog:query-syslog",
            "ciscosb-syslog:query-syslog-current-page": "/api/operations/ciscosb-syslog:query-syslog-current-page",
            "ciscosb-sys:asd-ping-request": "/api/operations/ciscosb-sys:asd-ping-request",
            "ciscosb-sys:asd-ping-response": "/api/operations/ciscosb-sys:asd-ping-response",
            "ciscosb-sys:clock-read-calendar": "/api/operations/ciscosb-sys:clock-read-calendar",
            "ciscosb-sys:clock-check-dst": "/api/operations/ciscosb-sys:clock-check-dst",
            "ciscosb-sys:clock-update-calendar": "/api/operations/ciscosb-sys:clock-update-calendar",
            "ciscosb-sys:clock-set-calendar": "/api/operations/ciscosb-sys:clock-set-calendar",
            "ciscosb-sys:system-reboot": "/api/operations/ciscosb-sys:system-reboot",
            "ciscosb-sys:system-factory-reset": "/api/operations/ciscosb-sys:system-factory-reset",
            "ciscosb-usb:usb-check-attached": "/api/operations/ciscosb-usb:usb-check-attached",
            "ciscosb-usergroup:import-users": "/api/operations/ciscosb-usergroup:import-users",
            "ciscosb-utl:utility-ping-request": "/api/operations/ciscosb-utl:utility-ping-request",
            "ciscosb-utl:utility-ping-response": "/api/operations/ciscosb-utl:utility-ping-response",
            "ciscosb-utl:utility-traceroute-request": "/api/operations/ciscosb-utl:utility-traceroute-request",
            "ciscosb-utl:utility-traceroute-response": "/api/operations/ciscosb-utl:utility-traceroute-response",
            "ciscosb-utl:utility-dnslookup": "/api/operations/ciscosb-utl:utility-dnslookup",
            "ciscosb-utl:utility-testcables": "/api/operations/ciscosb-utl:utility-testcables",
            "ciscosb-utl:utility-blinkled": "/api/operations/ciscosb-utl:utility-blinkled",
            "ciscosb-utl:pkt-capture-request": "/api/operations/ciscosb-utl:pkt-capture-request",
            "ciscosb-utl:pkt-capture-response": "/api/operations/ciscosb-utl:pkt-capture-response",
            "ciscosb-utl:is-port-available": "/api/operations/ciscosb-utl:is-port-available",
            "ciscosb-vpn-ipsec:s2s-connect": "/api/operations/ciscosb-vpn-ipsec:s2s-connect",
            "ciscosb-vpn-ipsec:s2s-disconnect": "/api/operations/ciscosb-vpn-ipsec:s2s-disconnect",
            "ciscosb-vpn-ipsec:c2s-disconnect": "/api/operations/ciscosb-vpn-ipsec:c2s-disconnect",
            "ciscosb-vpn-ipsec:teleworker-vpn-client-connect": "/api/operations/ciscosb-vpn-ipsec:teleworker-vpn-client-connect",
            "ciscosb-vpn-ipsec:teleworker-vpn-client-disconnect": "/api/operations/ciscosb-vpn-ipsec:teleworker-vpn-client-disconnect",
            "ciscosb-vpn-l2tp:l2tp-disconnect": "/api/operations/ciscosb-vpn-l2tp:l2tp-disconnect",
            "openvpn:openvpn-disconnect": "/api/operations/openvpn:openvpn-disconnect",
            "openvpn:generate-openvpn-client-template": "/api/operations/openvpn:generate-openvpn-client-template",
            "ciscosb-vpn-pptp:pptp-disconnect": "/api/operations/ciscosb-vpn-pptp:pptp-disconnect",
            "ciscosb-wan-ip:release-ip": "/api/operations/ciscosb-wan-ip:release-ip",
            "ciscosb-wan-ip:renew-ip": "/api/operations/ciscosb-wan-ip:renew-ip",
            "ciscosb-wan-ip:connect": "/api/operations/ciscosb-wan-ip:connect",
            "ciscosb-wan-ip:disconnect": "/api/operations/ciscosb-wan-ip:disconnect",
            "rt:fib-route": "/api/operations/rt:fib-route",
            "sys:set-current-datetime": "/api/operations/sys:set-current-datetime",
            "sys:system-restart": "/api/operations/sys:system-restart",
            "sys:system-shutdown": "/api/operations/sys:system-shutdown"
        },
        "rollbacks": {}
    }
}
```

## Reading the running/startup configuration

To read the (full) running or startup configurations, query the corresponding endpoint with a `GET` request. Make sure to include the `?deep` URL parameter at the end to get the full tree, and pipe the output to a pager or VIM to be able to scroll through and search through it. Note also the `Accept` header.

Example:

``` bash
curl -H "Accept: application/vnd.yang.datastore+json" \
  -k https://192.168.1.1:443/api/startup?deep \
  -u "expeca:expeca" | python3 -m json.tool | vim -
```

## Reading a specific configuration section

To read a specific configuration section, query the corresponding configuration endpoint with a `GET` request, appending the name of the target section. Again, make sure to include the `?deep` URL parameter at the end to get the full tree, and pipe the output to a pager or VIM. Note the `Accept` header.

Example (to read static DHCP mappings):

``` bash
curl -H "Accept: application/vnd.yang.data+json" \
  -k https://192.168.1.1:443/api/startup/ciscosb-lan-dhcp:static-dhcp?deep \
  -u "expeca:expeca" | python3 -m json.tool | vim -
```

## Editing a specific configuration section

Edits can only be done on the running configuration, and there are three modes of operation when editing configuration sections:

- HTTP Method `POST`: Creates a new configuration, should fail if configuration already exists.
- HTTP Method `PUT`: Creates a new configuration or replaces an existing one. Use with caution.
- HTTP Method `PATCH`: Merges the new configuration with the existing one. Useful for adding items to lists, for instance.

Payload for any of these operations should be a JSON object matching the target configuration, and `Accept` and `Content-Type` headers need to be set to `application/vnd.yang.data+json`. Disable SSL certificate checking. Return code is most often `204` for succesful requests.

Easiest way of doing this is through the Ansible `uri` module, which automatically converts any object inside the `body` key to a valid JSON:

``` yaml
- name: Append to running DHCP mappings using RESTCONF
  uri:
    url: "https://192.168.1.1:443/api/running/ciscosb-lan-dhcp:static-dhcp"
    method: PATCH
    force_basic_auth: yes
    user: expeca
    password: expeca
    body_format: json
    body:
      ciscosb-lan-dhcp:static-dhcp:
        entry:
          - name: Test-Binding
            ip-address: 1.2.3.4
            mac: "00:00:00:00:00:00"
            enabled: true
    headers:
      Accept: application/vnd.yang.data+json
      Content-Type: application/vnd.yang.data+json
    status_code: "{{ range(200, 300, 1) | list }}" # accept all codes from 200 to 299
    validate_certs: no
```

## Saving the running configuration

After modifying the running configuration, it needs to be copied to the startup configuration (as otherwise it will reset on reboot). This is performed by issuing a `POST` request to a special endpoint `/api/config/_copy-running-to-startup` (there is also a `/api/running/_copy-running-to-startup` endpoint which probably also works, but I have not tried it).

Again, the easiest way to do this is through the `uri` module:

``` yaml
- name: Trigger copy running router configuration to startup configuration
  uri:
    url: "https://192.168.1.1:443/api/config/_copy-running-to-startup"
    method: POST
    force_basic_auth: yes
    user: expeca
    password: expeca
    headers:
      Accept: application/vnd.yang.data+json
      Content-Type: application/vnd.yang.data+json
    body_format: json
    status_code: "{{ range(200, 300, 1) | list }}" # accept all codes from 200 to 299
    validate_certs: no
```
