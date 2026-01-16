#!/usr/bin/env python3

import argparse
from pprint import pprint
from src.step1 import step1
from src.step2 import step2
from src.ecriture import ecriture_config


def print_help():
    print(
        "Usage: python pipeline.py [-f FILE | --file FILE] [-h | --help] [-v | --verbose] [-n | --dry-run]"
    )
    print("Generate Cisco router configs from YAML configuration file.")
    print()
    print("Options:")
    print(
        "  -f, --file FILE    Specify the YAML config file (default: templates/example.yaml)"
    )
    print("  -h, --help         Show this help message and exit")
    print("  -v, --verbose     Show logs as the pipeline is executed")
    print("  -n, --dry-run     Run all steps without writing output files")
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
    args = parser.parse_args()

    if args.help:
        print_help()
        exit(0)

    file_path: str = args.file
    verbose: bool = args.verbose
    dry_run: bool = args.dry_run

    # Start pipeline
    # Step 1 : Read file and create list of routers
    # Step 2 : Resolve BGP data
    # Step 3 : Configure iBGP
    # Step 4 : Write config files for each router

    routers = step1(file_path, verbose)

    # Step 4 : only if --dry-run flag is unset
    if not dry_run:
        ecriture_config(routers, verbose)

    if dry_run and not verbose:
        pprint(routers)
