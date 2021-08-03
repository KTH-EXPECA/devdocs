# Overview of the AWS EC2 staging setup

The AWS staging setup consists of (currently) 8 [EC2](https://aws.amazon.com/ec2) instances configured to mimic the structure of the real testbed.
These are deployed inside an [VPC](https://aws.amazon.com/vpc), connected to a particular custom subnet.
In order to use the same hostnames and FQDNs as in the real setup, we use private a hosted zone in [Route 53](https://aws.amazon.com/route53) to provide DNS services for the VPC.

## The EC2 Instances

Currently (as of August 2021), the AWS staging setup consists of 8 EC2 instances.
These instances are built from a 4 different [Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html), which in turn use 4 different [Amazon Machine Images (AMIs)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) on provisioning.

- `galadriel`
: Corresponds to a `t3.micro` instance running Ubuntu Server 20.04 LTS.
    Built from a custom AMI which includes a base setup with required software for management, the `TestbedConfig` repository, and Ansible all set up and ready.

- `celeborn` and `elrond`
: Also correspond to `t3.micro` instances running Ubuntu Server 20.04 LTS, but these are built from a different AMI than `galadriel`.

- `fingolfin`
: `t3.micro` instance running Ubuntu Server 18.04 LTS, to mimic the physical testbed setup.
    Built from yet another custom AMI.

- Finally, the workload clients, `workload-client-[00:03]`
: Temporarily running on `t3.micro` instances (with yet another custom AMI).
    `t3.micro` instances are `x86_64` VMs though, so these will eventually be migrated to `ARM64`-based `t4g.micro` instances to mimic the physical setup which runs on Raspberry Pis.

## Networking

All EC2 instances are attached to a single Virtual Private Cloud, named `ExPECA Staging Network`.
The instances are also attached to the custom subnet `ExPECAStaging`, which has an `IPv4` CIDR of `172.31.0.0/24`; each instance gets an automatically assigned static IP within this range.
These private IPs are valid throughout the lifetime of the instance, i.e. until it instance is terminated.
Instances additionally get public IPs and FQDNs from AWS for internet access; these are however discarded and renewed whenever instances are started and stopped (see [here](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-ip-addressing.html) for more details.)

We use two security groups, attached to the network interface, to manage firewall rules.
These groups allow inbound SSH traffic from the internet, free outbound traffic from the network, and finally unrestricted traffic within the network.

For DNS we use a [private hosted zone in Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html).
This zone is associated with the `ExPECA Staging Network` VPC and assigned the top-level domain `expeca`.
When (re)creating the staging setup using the Ansible playbook, it automatically creates an `A` record on this zone for each instance, pairing the corresponding fully qualified domain name (e.g. `galadriel.expeca`) to the private static IP address assigned to it.
This then allows for DNS lookups to all devices on the network from any instance.
