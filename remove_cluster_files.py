#!/usr/bin/env python

import yaml, os, argparse, shutil, subprocess

CONFIG_FILE = "config.yml"
COGNATE_INVENTORY_PATH = "inventory"
COGNATE_PROVISIONING_PATH = "provisioning"

def yaml_to_dict(filename):
    with open(filename) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        return config

def build_config_dict(file):
    config = yaml_to_dict(file)
    config["cognate_folder"] = os.path.abspath(os.path.expanduser(config["cognate_folder"]))
    config['cognate_inventory_folder'] = os.path.join(config["cognate_folder"], COGNATE_INVENTORY_PATH)
    config['cognate_provisioning_folder'] = os.path.join(config["cognate_folder"], COGNATE_PROVISIONING_PATH)
    return config

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cluster",
        metavar='''CLUSTER_NAME''',
        required=True,
        type=str,
        help='''Cluster name''')
    return parser

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    config = build_config_dict(CONFIG_FILE)

    if not args.cluster.isidentifier():
        print("Invalid cluster name: {}".format(args.cluster))
        print("Nothing to do")
        exit(1)

    inventory_file_path = os.path.join(config["cognate_inventory_folder"], "{}.yml".format(args.cluster))
    cluster_provisioning_path = os.path.join(config["cognate_provisioning_folder"], args.cluster)
    if os.path.exists(inventory_file_path):
        print("Removing inventory file '{}'".format(inventory_file_path))
        os.remove(inventory_file_path)
    if os.path.exists(cluster_provisioning_path):
        print("Removing cluster folder '{}'".format(cluster_provisioning_path))
        shutil.rmtree(cluster_provisioning_path)