# Cognate Templates

A curated list of Ansible playbooks that can be easily integrated with the [Cognate](https://github.com/alsfreitaz/cognate) framework.

## Dependencies

* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* [Ansible](https://docs.ansible.com/ansible/latest/index.html)
* [Git](https://git-scm.com/)
* [Cognate](https://github.com/alsfreitaz/cognate)
* Privileged access (**only if** you wish to mount NFS sharing between host and guest on Virtualbox)

> **Obs:** If you already have Ansible and Git installed and want to install Virtualbox and Vagrant in an automated and reproducible way, you can check project [alsfreitaz/virtualization](https://github.com/alsfreitaz/virtualization) out.

# Example

1. Clone Cognate Templates project

    ```
    $ git clone https://github.com/alsfreitaz/cognate-templates.git
    ```
2. Check/Modify variable `cognate_folder` in Congnate Templates [config.yml](config.yml) file to point to your Cognate root folder (referred here as `$COGNATE_DIR`). 

    > The default value points currently to ~/Workspaces/cognate but you will probably need to adapt it to a different path.

3. Check/Modify variable `cognate_ip_range` in Congnate Templates [config.yml](config.yml) file to reserve an IP range for using with Cognate.

    > Currently, the default IP range is `192.168.10-11.0-255` which is far than sufficient for development purposes but you will need to change if you have other apps that could potentially use IP addresses from 192.168.10.2 to 192.168.11.254.

    > One thing to notice here is that IP addresses ending in x.y.z.0 (subnet address), x.y.z.1 (default gateway address used by Virtualbox) and x.y.z.255 (broadcast address) are automatically discarded. So the default IP range `192.168.10-11.0-255` provides us with 256*2 - 3*2 = 506 assignable valid private IP addresses.

4. Change directory to Cognate Templates root folder, choose a template folder you want to use to create a cluster then run the [setup_cluster](setup_cluster) command with the appropriate arguments to translate the template files to actual static files ready to be used by Cognate:

    ```
    $ cd $COGNATE_TEMPLATES_DIR
    $ ./setup_cluster -c centos7 -s base/centos7_v1905.1 \
          -r @node@=@prefix_symbol -r @ip@=@dynamic_ip -r @memory@=1024 -r @cpus@=1 
    ```
    
    > The above command will build a Cognate inventory file called `centos7.yml` from a template source folder (`base/centos7_v1905.1` in this case) in which we describe we want a CentOS 7 VM to be provided with 1024 MB of RAM, 1 CPU and one IP dynamically chosen from a preset range of possible IP addresses (set in config.yml file). We also say the name of the cluster is `centos7` and it will be used as a namespace for the nodes' names and destination folder name in order to avoid name clashes.
    
    > Notice the use of the multivalued `-r` option to pass the string names to be replaced (in format `key=value`) in all files present in the source folder pointed by `-s` option.
    
    > In the above example, we asked to prefix all occurences of the `@node@` symbol with the `<cluster_name>__` pattern (this is the mean of the `@prefix_symbol` value). As result, all occurences of `@node@` in all files present in the template folder `base/centos7_v1905.1` will be translated to the string `centos7__node` (*i.e* character '@' is removed from the symbol `@node@` and then it is the prefixed with "<clustername>__") in the destination folder `$COGNATE_DIR/provisioning/centos7`.
    
    > Please notice how the cluster name (passed as argument by the `-c` option) plays an importante role here. It is used to name the destination cognate inventory file (*i.e.* *<cluster_name>*.yml), the cluster destination folder name (*i.e.* $COGNATE_DIR/provisioning/*<cluster_name>*) and possibly string symbols in all files (which is *very* useful for setting VM names at creation time without having to manually modify files).
    
5. Run `vagrant up` from Cognate root folder to provide and provision all virtual machine(s) in the cluster `centos7`:

    ```
    $ cd $COGNATE_DIR
    $ vagrant up /centos7__/ 
    ```
    
    > The above command will create and provision all VM whose names start with `centos__` using pattern matching provided by Vagrant to limit actions only to a group of virtual machines.

# Conventions

All template subdirectories under this project's root folder should have **at least** four files:

1. [**Required**] One Ansible config file (generally named *ansible.cfg* but there are no hard requirements on this)
2. [**Required**] One Ansible inventory file (generally named *inventory.yml* but there are no hard requirements on this)
3. [**Required**] One Ansible playbook file (generally named *playbook.yml* but there are no hard requirements on this)
4. [**Optional**] One Ansible dependency file in case you have external roles to install using Ansible Galaxy (generally named *requirements.yml* but there are no hard requirements on this)
5. [**Required**] One Cognate inventory file (must be named  *cognate_inventory.yml*)

> **Please notice that all paths declared in the Cognate inventory file (item 5) must be relative to Cognate's root folder (*i.e.* where Cognate's Vagrantfile is placed), otherwise Vagrant won't be able to find the files described in items 1, 2 and 3**.

# Creating, Using and Modifing Files

You can use these templates (inventories and/or playbooks) to rapidly spin up a VM cluster from static inventories under one unique folder that aims to answer to a specific need (this folder is refered as a *cluster* because all files inside it are able to create N virtual machines). 

By doing so, you are able to use one set of files (see [Conventions](#conventions) section) to spin up just a single development node and when you are done with the development stage, you could easily change the configuration set up to deploy two or more nodes on a different cluster locally and to test your application in a distributed mode.

Probably you'll need to change some of these files to match your expectations (amount of CPU, memory, playbook steps, etc). These Playbooks and configuration files contain just one initial setup for you to begin with but, at the end of the day, it's up to you to structure the files and folders the way you want.
