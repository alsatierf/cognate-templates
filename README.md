# cognate-playbooks

A curated list of Ansible playbooks that can be easily integrated with the [Cognate](https://github.com/alsfreitaz/cognate) framework.

# How-to

1. Clone the Cognate project, change diretory to its provisioning folder, clone this project then change directory to it:

    ```
    $ git clone https://github.com/alsfreitaz/cognate.git
    $ cd provisioning
    $ git clone https://github.com/alsfreitaz/cognate-playbooks.git
    $ cd cognate-playbooks
    ```
    
2. Change directory to one of this project's subdirectories, fetch all external roles with Ansible Galaxy, copy the file named *cognate__X.yml* to Cognate's [vagrant_inventory](https://github.com/alsfreitaz/cognate/tree/master/vagrant_inventory) folder and then change directory back to Cognate root folder. Substitute `X` by the directory name of your choice:

    ```
    $ cd X/
    $ ansible-galaxy install -r requirements.yml # if requirements.yml file exists and is not empty
    $ cp cognate__X.yml ../../../vagrant_inventory
    $ cd ../..
    ```
    
3. Run `vagrant up` to provide and provision the virtual machine(s):

    ```
    $ vagrant up
    ```

# Conventions

All subdirectories under this project's root folder should have **at least** four files:

1. One Ansible config file (generally named *ansible.cfg* but there are no hard requirements on this)
2. One Ansible inventory file (generally named *inventory.yml* but there are no hard requirements on this)
3. One Ansible playbook file (generally named *playbook.yml* but there are no hard requirements on this)
4. One Ansible dependency file (generally named *requirements.yml* but there are no hard requirements on this)
5. One Cognate inventory file (named  *cognate__X.yml* and the only requirement is that this file name begins with *cognate__* and ends with *.yml* or *.yaml*.

> **Please notice that all paths declared in the Cognate inventory files (item 5) should be absolute or, *ideally*, relative to Cognate's root folder (i.e. where Cognate's Vagrantfile is placed), otherwise Vagrant won't be able to find the files described in items 1, 2 and 3**.

> Please notice that you could tipically find many Ansible inventory, Ansible playbook and Cognate inventory files in one directory. This allows us to have different cluster configurations under the same folder structure.

# Creating, Using and Modifing Files

In order to make things clear, you can use preconfigured files (inventories and/or playbooks) that allow you to rapidly spin up a VM cluster from static inventories under one unique folder that aims to answer to a specific need. 

By doing so, you are able to use one set of four files (described in the [Conventions](#conventions) section) to spin up just a single development node. When you are done with the development stage, you could easily change the configuration set up to deploy two or more nodes locally and to test your application in a distributed mode.

Probably you'll need to change some of these files to match your expectations (amount of CPU, memory, playbook steps, etc). These Playbooks and configuration files contain just one initial setup for you to begin with but, at the end of the day, it's up to you to structure the files and folders the way you want.
