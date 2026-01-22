#!/usr/bin/env python3

import argparse
import yaml
from pprint import pprint
from src.step1 import step1
from src.step2 import step2
from src.step3 import step3
from src.step4_ospf import step4_ospf
from src.step4_ibgp import step4_ibgp
from src.ecriture import ecriture_config
from src.config_to_gns3 import export_config


def print_help():
    print(
        "Usage: python pipeline.py [-f FILE | --file FILE] [-h | --help] [-v | --verbose] [-n | --dry-run]"
    )
    print("Generate Cisco router configs from YAML configuration file.")
    print()
    print("Options:")
    print("  -f, --file FILE        |Specify the YAML config file (default: templates/example.yaml)")
    print("  -h, --help             |Show this help message and exit")
    print("  -v, --verbose          |Show logs as the pipeline is executed")
    print("  -n, --dry-run          |Run all steps without writing output files")
    print("  -p, --project-name NAME|Specify the gns3 project name (default : 'untitled') ")
    print()
    print("Examples:")
    print("  python pipeline.py")
    print("  python pipeline.py -f my_config.yaml")
    print("  python pipeline.py --dry-run")
    print("  python pipeline.py --help")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Generate Cisco router configs from YAML.", add_help=False
    )
    parser.add_argument(
        "-f", "--file", default="templates/example.yaml", help="YAML config file"
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Run all steps without writing output files",
    )
    parser.add_argument(
        "-p", "--project-name", help="Specify GNS3 project name"
    )
    args = parser.parse_args()

    if args.help:
        print_help()
        exit(0)

    file_path: str = args.file
    verbose: bool = args.verbose
    dry_run: bool = args.dry_run
    project_name: str = args.project_name

    # Load YAML configuration
    with open(file_path, "r") as f:
        config_data = yaml.safe_load(f)

    # Start pipeline
    # Step 1 : Assign networks to interfaces without addresses
    # Step 2 : Create list of routers from config data
    # Step 3 : Resolve BGP data
    # Step 4 : Configure IGP (OSPF or iBGP, RIP doesn't need any extra work)
    # Step 5 : Write config files for each router

    step1(config_data, verbose)  # Pass empty list, step2 modifies config_data
    routers = step2(config_data, verbose)
    routers = step3(config_data, routers, verbose)
    routers = step4_ospf(config_data, routers, verbose)
    routers = step4_ibgp(config_data, routers, verbose)

    # Step 4 : only if --dry-run flag is unset
    if not dry_run:
        ecriture_config(routers, verbose)
        if project_name is not None :
            export_config(verbose,project_name)

    if dry_run and not verbose:
        pprint(routers)