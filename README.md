# cognate-playbooks

A curated list of Ansible playbooks that can be used with the [Cognate](https://github.com/alsfreitaz/cognate) framework with little effort.

# How-to

1. Clone the Cognate project, change diretory to its provisioning folder, clone this project then change directory to it:

    ```
    $ git clone https://github.com/alsfreitaz/cognate.git
    $ cd provisioning
    $ git clone https://github.com/alsfreitaz/cognate-playbooks.git
    $ cd cognate-playbooks
    ```
    
2. Change directory to one of this project's subdirectories, fetch all external roles (only needed file *requirements.yml* exists) with Ansible Galaxy, copy the file named *cognate__X.yml* to Cognate's [vagrant_inventory](https://github.com/alsfreitaz/cognate/tree/master/vagrant_inventory) folder and then change directory back to Cognate root folder. Substitute `X` by the directory name of your choice:

    ```
    $ cd X/
    $ ansible-galaxy install requirements.yml
    $ cp cognate__X.yml ../../../vagrant_inventory
    $ cd ../..
    ```
    
3. Run `vagrant up` to provide and provision the virtual machine(s):

    ```
    $ vagrant up
    ```
