# Accessing the AWS test instances

In order to facilitate building and testing of software intended to run on the testbed devices, we provide two [Amazon Web Services EC2 instances](https://aws.amazon.com/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc) running [Ubuntu Server 20.04 LTS](https://ubuntu.com/blog/ubuntu-server-20-04) for testing: 

- One [x86_64-based](https://aws.amazon.com/ec2/instance-types/t3/) instance to represent a "regular" x86 server.
- One [ARM64-based](https://aws.amazon.com/ec2/instance-types/t4/) instance to represent a Raspberry Pi 4B client.

Below you will find instructions on how to remotely access these virtual machines, please read them carefully.

## Credentials

The first requirement is of course to obtain the necessary credentials, corresponding to a username, a password, and an SSH private key file.
These will be provided to you by one of the members of the research group.
It should go without saying that you should be careful with these credentials and not share them with anybody outside the project.

## Managing and accessing the EC2 virtual machine through the AWS Console

In order to avoid excessive/unecessary costs, you will have to **manually start the VMs whenever you need to use them, and make sure to shut them down after you are done.**
This is done through the Amazon Web Services web console.

### Accessing the AWS web console

1. Head to [https://eu-north-1.console.aws.amazon.com/console](https://eu-north-1.console.aws.amazon.com/console).
2. Select `IAM User`.
3. Enter the following account ID: `kth-expeca`.
4. Click `Next`.
5. On the following page, enter the credentials you have been provided.
6. You should now be logged into the AWS Console.

### Managing the AWS EC2 Instances

1. Once you're [logged in](#accessing-the-aws-web-console), head to `Services -> EC2`.
2. Next, on the left sidebar, click on `Instances`.
3. On the list of instances, in the top filter text box, search for `project_course`.
4. Select both instances (`project_course_arm64` and `project_course_x86`).
5. In the upper right corner, click on `Instance state`, then on the desired state for the instance (**Note: never click on `Terminate instance` as that will completely delete the instance and whatever is stored on it.**)

Once again, ***please make sure to always _stop_ the EC2 instance when you're not using it.***

### Connecting to one of the EC2 instances from the web console

1. Make sure the instance is running by following [the steps above.](#managing-the-aws-ec2-instance)
2. Reload the page until the instance state is detected as `Running`.
3. In the upper right corner, click on `Connect`.
4. On the next page, select `EC2 Instance Connect`.
5. Verify that the username is set to `ubuntu`, then click `Connect`.
6. A new tab should open with a terminal attached to the EC2 instance.

### Connecting to one of the EC2 instances through SSH

1. Make sure the instance is running by following [the steps above.](#managing-the-aws-ec2-instance)
2. Reload the page until the instance state is detected as `Running`.
3. Take note of the public IP address and/or the public IPv4 DNS assigned to the instance.
4. Open a terminal window.
5. Ensure the private SSH key provided to you has been correctly added to your SSH agent by following [the steps here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent) (note, **you do not need to generate a key**, as one will be provided to you).
6. Open an SSH connection to the instance:
   
   ```bash
   $ ssh -A ubuntu@1.2.3.4
   ubuntu@ip-1-2-3-4:~$ 
   ```

   (Replace `1.2.3.4` with the public IPv4/DNS address of the instance.)

### Communicating between the instances

Both instances have both a public as well as private IPv4 address.
When connecting to the instance over the internet (e.g. for SSH access), you will need to use the public address.
However, when deploying workloads on the instances, make sure they communicate over the private network using the private IPv4 addresses.
This ensures traffic does not transit through the internet and stays within the datacenter, giving you much better performance.
