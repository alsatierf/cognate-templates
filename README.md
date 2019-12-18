# Cognate Templates

A curated list of Ansible playbooks that can be easily integrated with the [Cognate](https://github.com/alsfreitaz/cognate) framework.

## Dependencies

* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* [Ansible](https://docs.ansible.com/ansible/latest/index.html)
* [Git](https://git-scm.com/)
* [Cognate](https://github.com/alsfreitaz/cognate)
* Python 3.5+ and pip3
* Privileged access (**only if** you wish to mount NFS sharing between host and guest on Virtualbox)

> **Obs:** If you already have Ansible and Git installed and want to install Virtualbox and Vagrant in an automated and reproducible way, you can check project [alsfreitaz/virtualization](https://github.com/alsfreitaz/virtualization) out.

# Initial Setup

1. Clone Cognate Templates project and install all dependencies

    ```
    $ git clone https://github.com/alsfreitaz/cognate-templates.git
    $ cd cognate-templates
    $ pip install -r pip_requirements.txt
    ```
    
2. Provide variable `cognate_folder` in Congnate Templates [config.yml](config.yml) file with a path to your Cognate root folder (referred here as `$COGNATE_DIR`).

3. Check/Modify `cognate_ip_range` variable in [Congnate Templates config file](config.yml) to reserve an IP range for using with Cognate

    > Currently, the default IP range is `192.168.10-11.0-255` which is sufficient for development purposes but you will need to change it if you have other processes that could potentially use IP addresses from 192.168.10.0 to 192.168.11.255.

    > One thing to notice here is that IP addresses ending in x.y.z.0 (subnet address), x.y.z.1 (default gateway address used by Virtualbox) and x.y.z.255 (broadcast address) are not considered VM assignable IP addresses. So the default IP range `192.168.10-11.0-255` provides us with 256\*2 - 3\*2 = 506 valid private IP addresses.


# Internals

## Usage

```
usage: setup_cluster [-h] -s TEMPLATE_FOLDER -c CLUSTER_NAME
                     [-r @SYMBOL@=VALUE] [--prefix-with-cluster-name @SYMBOL@]
                     [--replace-by-random-ip @SYMBOL@] [--overwrite]

optional arguments:
  -h, --help            show this help message and exit
  -s TEMPLATE_FOLDER, --source-folder TEMPLATE_FOLDER
                        Template folder name
  -c CLUSTER_NAME, --cluster CLUSTER_NAME
                        Cluster name
  -r @SYMBOL@=VALUE, --replace @SYMBOL@=VALUE
                        Set a number of keys that are to be replaced by their
                        corresponding values (do not put spaces before or
                        after the = sign). If a value contains spaces, you
                        should define it with double quotes: @foo@="this is a
                        sentence" Note that values are always treated as
                        strings.
  --prefix-with-cluster-name @SYMBOL@
                        Replaces all ocurrences of @SYMBOL@ by
                        <CLUSTER_NAME>__SYMBOL
  --replace-by-random-ip @SYMBOL@
                        Replaces all ocurrences of @SYMBOL@ by a random IP
  --overwrite           Overwrite all files and folders. WARNING: Cluster
                        folder and will be deleted and recreated
```

## Cluster Creation

The `setup_cluster` command is responsible for creating one cluster from a template folder by executing the following steps:

1. Create or destroy and recreate (if `--overwrite` option is present) a folder called `${COGNATE_DIR}/provisioning/${CLUSTER_NAME}`. If folder `${COGNATE_DIR}/provisioning/${CLUSTER_NAME}` exists and option `--overwrite` is not set, the program will do nothing and will exit with error to avoid overwriting accidentally an existing folder.

2. Create a dictionary of key->value strings that will be used across all files in `${TEMPLATE_FOLDER}` where key is of the form `@SYMBOL@` and value can be directly set (by using `--replace` option) or dynamically constructed (by using `--replace-by-random-ip` and `--prefix-with-cluster-name` options).

    1. `--replace-by-random-ip` can be used for requesting one random IP from the IP range defined in `cognate_ip_range` config variable that isn't in use yet. For checking which IP addresses are in use, all `ip` values from all \*.yml files under `${COGNATE_DIR}/inventory` folder are collected and subtracted from all assignable IP addresses constructed from `cognate_ip_range` config variable.
    
    2. `--prefix-with-cluster-name` replaces all ocurrences of `@SYMBOL@` by `${CLUSTER_NAME}__SYMBOL`.

3. Apply all replacements on the template files and write the resulting files in `${COGNATE_DIR}/provisioning/${CLUSTER_NAME}`, keeping the same relative files hierarchy as the source template folder.

4. Move the file `${COGNATE_DIR}/provisioning/${CLUSTER_NAME}/cognate_inventory.yml` (translated in step 3) to `${COGNATE_DIR}/inventory/${CLUSTER_NAME}.yml`

> **Notice that options `--replace-by-random-ip`, `--replace-by-random-ip` and `--replace` can be used many times on the command line (*i.e.* they are multi-valued variables).**

## Template Folders Structure

All template folders should have **at least** these files:

1. [**Required**] One Ansible config file (generally named *ansible.cfg* but there are no hard requirements on this)
2. [**Required**] One Ansible inventory file (generally named *inventory.yml* but there are no hard requirements on this)
3. [**Required**] One Ansible playbook file (generally named *playbook.yml* but there are no hard requirements on this)
4. [**Optional**] One Ansible dependency file in case you have external roles to install using Ansible Galaxy (generally named *requirements.yml* but there are no hard requirements on this)
5. [**Required**] One Cognate inventory file (must be named  *cognate_inventory.yml*)

> **Notice that all paths declared in the Cognate inventory file (item 5) must be relative to Cognate's root folder (*i.e.* where Cognate's Vagrantfile is placed), otherwise Vagrant won't be able to find the files described in items 1, 2 and 3**.

## A Note on Creating, Using and Modifing Files and Templates

You can use these templates (inventories and/or playbooks) to rapidly spin up a VM cluster from static inventories under one unique folder that aims to answer to a specific need (this folder is refered as a *cluster* because all files inside it are able to create N virtual machines). 

By doing so, you are able to use one set of files (see [Template Folders Structure](#template-folders-structure) section) to spin up just a single development node and when you are done with the development stage, you could easily deploy another cluster with two or more nodes to test your application in a distributed mode.

Probably you'll need to change some of these files or command line arguments to match your expectations (amount of CPU, memory, playbook steps, etc). These Playbooks and configuration files contain just one initial setup for you to begin with but, at the end of the day, it's up to you to structure the files and folders the way you want.

# Templates

In the following subsections you will learn how to deploy clusters using some templates and what to expect to be automatically configured by Ansible on each virtual machine.

## base/centos7_v1905.1

### Scripts

```
COGNATE_DIR= # TODO
SOURCE_FOLDER=base/centos7_v1905.1
CLUSTER_NAME= # TODO
MEMORY= # TODO
CPUS= # TODO

./setup_cluster --source-folder ${SOURCE_FOLDER} \
    --cluster ${CLUSTER_NAME} \
    --prefix-with-cluster-name @node@ \
    --replace-by-random-ip @ip@ \
    --replace @memory@=${MEMORY} \
    --replace @cpus@=${CPUS} \
    # --overwrite

# Deploy all virtual machines whose names begin with ${CLUSTER_NAME}__
(
    cd ${COGNATE_DIR}
    vagrant up /${CLUSTER_NAME}__/
)
```

### Expected Cluster State

- **Node 1**:
  - Providing:
    - **name**: ${CLUSTER_NAME}__node
    - **box**: CentOS 7
    - **box_version**: 1905.1
    - **ram**: ${MEMORY} MB
    - **cpus**: ${CPUS}
    - **ip**: dynamically assigned
  - Provisioning:
    - OS packages updated


## spark/spark-2.4.4/single

### Scripts

```shell
COGNATE_DIR= # TODO
SOURCE_FOLDER=spark/spark-2.4.4/single
CLUSTER_NAME= # TODO
MEMORY= # TODO
CPUS= # TODO

./setup_cluster --source-folder ${SOURCE_FOLDER} \
    --cluster ${CLUSTER_NAME} \
    --prefix-with-cluster-name @spark_01@ \
    --replace-by-random-ip @spark_01__ip@ \
    --replace @memory@=${MEMORY} \
    --replace @cpus@=${CPUS} \
    # --overwrite

# Install external Ansible roles
(
    cd ${COGNATE_DIR}/provisioning/spark_single
    ansible-galaxy install -r requirements.yml
)

# Deploy all virtual machines whose names begin with ${CLUSTER_NAME}__
(
    cd ${COGNATE_DIR}
    vagrant up /${CLUSTER_NAME}__/ 
)
```

### Expected Cluster State

- **Node 1**:
  - Providing:
    - **name**: ${CLUSTER_NAME}__spark_01
    - **box**: CentOS 7
    - **box_version**: 1905.1
    - **ram**: ${MEMORY} MB
    - **cpus**: ${CPUS}
    - **ip**: dynamically assigned
  - Provisioning:
    - OS packages updated
    - Common development packages installed
    - OpenJDK 8 installed
    - Git 2 installed
    - Maven 3.6.3 installed
    - Latest SBT installed
    - Apache Spark 2.4.4 installed

