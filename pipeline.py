import yaml
import ipaddress
from src.ecriture import ecriture_config
from src.class_to_dict import convert_as_to_dict_list
import argparse
from src.models import AS, Router, IGP

"""

This file contains the different functions that make the pipeline this project relies on
This pipeline take in a yaml configuration file (I.E. templates/example.yaml) and returns Cisco routers configuration files
The steps of the pipeline are the functions of this file, written in order (first-to-last)
"""


def print_help():
    print("Usage: python pipeline.py [-f FILE | --file FILE] [-h | --help] [-v | --verbose]")
    print("Generate Cisco router configs from YAML configuration file.")
    print()
    print("Options:")
    print("  -f, --file FILE    Specify the YAML config file (default: templates/example.yaml)")
    print("  -h, --help         Show this help message and exit")
    print("  -v, --verbose     Show logs as the pipeline is executed")
    print()
    print("Examples:")
    print("  python pipeline.py")
    print("  python pipeline.py -f my_config.yaml")
    print("  python pipeline.py --help")


# Step 1: read and serialize yaml config
def read_config(file_path: str, ass: dict[str, "AS"]) -> dict[str, "AS"]:
    if verbose: print("Step 1: Processing config file...")
    if verbose: print("=================================")

    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    if verbose: print("Config file successfully read.")

    for as_key, as_data in data["ASs"].items():
        # Parse IGP
        igp = getattr(IGP, as_data["igp"].upper())

        # Parse loopback space
        loopback_space = ipaddress.IPv6Network(as_data["loopback_space"])

        # Create Router objects first
        routers_dict = {}
        for r_id, r_data in as_data["routers"].items():
            router = Router(ID=r_id, border=r_data["border"])
            routers_dict[r_id] = router

        # Link interfaces (assuming interfaces are lists of router IDs)
        for r_id, router in routers_dict.items():
            interfaces = []
            for intf_id in as_data["routers"][r_id]["interfaces"]:
                if intf_id in routers_dict:
                    interfaces.append(routers_dict[intf_id])
            router.interfaces = interfaces

        # Create AS object
        as_obj = AS(number=as_key, igp=igp, loopback_space=loopback_space)
        as_obj.routers = list(routers_dict.values())

        ass[as_key] = as_obj
        if verbose: print("Serialized:", as_obj)

    if verbose: print()
    return ass


# Step 2: Assign unique loopback IP addresses to routers from their AS's loopback_space
def generate_loopback_addresses(ass: dict[str, "AS"]) -> dict[str, "AS"]:
    if verbose: print("Step 2: Generating and assigning loopback addresses to routers from AS loopback space...")
    if verbose: print("========================================================================================")

    for a in ass.values():
        network = a.loopback_space
        if verbose: print(f"Now processing routers in AS number {a.number}...")
        for i, router in enumerate(a.routers):
            router.loopback = network.network_address + (i + 1)
            if (verbose): print("Processed :", router)

    if verbose: print()
    return ass


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate Cisco router configs from YAML.", add_help=False)
    parser.add_argument("-f", "--file", default="templates/example.yaml", help="YAML config file")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.help:
        print_help()
        exit(0)

    file_path: str = args.file
    global verbose
    verbose: bool = args.verbose

    # Start pipeline
    print("Starting pipeline")
    if verbose: print("Config file:", file_path, "\n")

    ass: dict[str, "AS"] = {}
    read_config(file_path, ass)
    generate_loopback_addresses(ass)

    print("Pipeline completed. Router configurations ready.")

    #ecriture config
    as_list = list(ass.values())
    routers_for_template = convert_as_to_dict_list(as_list)
    ecriture_config(routers_for_template)
