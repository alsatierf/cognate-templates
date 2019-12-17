# cognate-templates

A curated list of Ansible playbooks that can be easily integrated with the [Cognate](https://github.com/alsfreitaz/cognate) framework.

# How-to

1. Clone the Cognate project (if not already installed) then clone this project:

    ```
    $ git clone https://github.com/alsfreitaz/cognate.git
    $ git clone https://github.com/alsfreitaz/cognate-templates.git
    ```
    
2. Change directory to this project root folder, choose the template folder you want to use to create a cluster then run the setup_cluster command with the appropriate arguments to translate the templates into actual static files ready to be used by Cognate:

    ```
    $ cd $COGNATE_TEMPLATES_DIR
    $ ./setup_cluster -c centos7 -s base/centos7_v1905.1 -r @node@=@prefix_symbol -r @ip@=@dynamic_ip -r @memory@=1024 -r @cpus@=1 
    ```
    
    > The above command will build a Cognate inventory file called `centos7.yml` from a template (`base/centos7_v1905.1/cognate_inventory.yml` in this case) in which we describe a CentOS 7 VM to be provided with 1024 MB of RAM, 1 CPU and one IP dynamically chosen from a preset range of possible IP addresses (set in config.yml file). We also say the name of the cluster is `centos7` and it will be used as a namespace for the nodes' names and destination folder name in order to avoid name clashes when the same template is used twice for building different clusters. 
    
    > We also asked to prefix all occurences of the `@node@` symbol with the `<cluster_name>__` pattern (this is the mean of the `@prefix_symbol` value). As result, all occurences of `@node@` in all files present in the template folder `base/centos7_v1905.1` will be translated to the string `centos7__node` (notice that the character '@' is removed from the symbol `@node@` and only then the prefix "<clustername>__" is prepended to it) on the destination folder `$COGNATE_DIR/provisioning/centos7`.
    
    > Please notice how the cluster name (passed as argument by the `-c` flag) plays an importante role here. It is used to name the destination cognate inventory file (*i.e.* *<cluster_name>*.yml), the cluster destination folder name (*i.e.* $COGNATE_DIR/provisioning/*<cluster_name>*) and possibly string symbols in all files (which is *very* useful for setting VM names at creation time without having to manually modify files).
    
3. Run `vagrant up` (from Cognate root folder) to provide and provision all virtual machine(s) in the cluster `centos7`:

    ```
    $ cd $COGNATE_DIR
    $ vagrant up /centos7__/ 
    ```
    
    > The above command will create and provision all VM whose names start with `centos__` (it uses pattern matching provided by vagrant to limit actions only to virtual machines mached by the regexp).

# Conventions

All template subdirectories under this project's root folder should have **at least** four files:

1. One Ansible config file (generally named *ansible.cfg* but there are no hard requirements on this)
2. One Ansible inventory file (generally named *inventory.yml* but there are no hard requirements on this)
3. One Ansible playbook file (generally named *playbook.yml* but there are no hard requirements on this)
4. One Ansible dependency file (generally named *requirements.yml* but there are no hard requirements on this)
5. One Cognate inventory file (must be named  *cognate_inventory.yml*)

> **Please notice that all paths declared in the Cognate inventory file (item 5) must be relative to Cognate's root folder (*i.e.* where Cognate's Vagrantfile is placed), otherwise Vagrant won't be able to find the files described in items 1, 2 and 3**.

# Creating, Using and Modifing Files

In order to make things clear, you can use preconfigured files (inventories and/or playbooks) that allow you to rapidly spin up a VM cluster from static inventories under one unique folder that aims to answer to a specific need. 

By doing so, you are able to use one set of four files (described in the [Conventions](#conventions) section) to spin up just a single development node. When you are done with the development stage, you could easily change the configuration set up to deploy two or more nodes locally and to test your application in a distributed mode.

Probably you'll need to change some of these files to match your expectations (amount of CPU, memory, playbook steps, etc). These Playbooks and configuration files contain just one initial setup for you to begin with but, at the end of the day, it's up to you to structure the files and folders the way you want.
