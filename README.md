# cognate-playbooks

A project that integrates a curated list of Ansible playbooks into the Cognate framework


# How-to

1. Clone the Cognate project, change diretory to its provisioning folder then clone this project:

    ```
    $ git clone https://github.com/alsfreitaz/cognate.git
    $ cd provisioning
    $ git clone https://github.com/alsfreitaz/cognate-playbooks.git
    ```
    
2. Copy a file named *cognate__XXX.yml* from some playbook folder to Cognate's [vagrant_inventory](https://github.com/alsfreitaz/cognate/tree/master/vagrant_inventory) folder then change directory to Cognate project root folder. In this example, we are copying a configuration file for deploying and provisioning a set of spark-2.4.4 machines:

    ```
    $ cp spark-2.4.4/cognate__spark-2.4.4.yml ../../vagrant_inventory
    $ cd ../..
    ```
    
3. Run `vagrant up` to provide and provision the virtual machine(s):

    ```
    $ vagrant up
    ```
