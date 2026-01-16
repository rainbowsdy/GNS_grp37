#!/usr/bin/python3

import yaml
import ipaddress
from pprint import pprint


# Parse yaml config file and transfrom it to match the output structure
def step1(filepath: str, verbose: bool = False) -> list:
    routers = []

    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
        if verbose:
            print("#STEP 1: ")
            pprint(f"Reading from config: {data}")

        if "ASs" in data:
            data = data["ASs"]

        for an, a in data.items():
            __process_as__(routers, an, a)

        if verbose:
            print("Data parsed successfully")
    return routers


def __process_as__(routers, as_number, as_data):
    # Note on IGPs:
    # Different IGPs are configured in diffeerent places or stages
    # OSPF is taken care of in this function
    # RIP is configured per interface, so in this step but in the __process_interface__ function
    # iBGP is configured in this stage, but we aren't sure how yet since it hasn't been implemented yet
    igp = as_data["igp"]

    for i, (ri, r) in enumerate(as_data["routers"].items()):
        # Add hostname (as:router_id) and computed loopback from loopback_space
        router = {
            "hostname": f"{as_number}:{ri}",
            "loopback": {
                "ipv6": str(ipaddress.IPv6Network(as_data["loopback_space"])[0] + i + 1)
            },
        }

        # Add interfaces
        interfaces = []
        for int_name, int_data in r["interfaces"].items():
            interface = __process_interface__(int_name, int_data, igp)
            interfaces.append(interface)

        router["interfaces"] = interfaces

        # Add ospf config if it is enabled
        if igp == "ospf":
            router["ospf"] = {"router_id": ri}

        routers.append(router)


def __process_interface__(int_name, int_data, igp) -> dict:
    interface = {
        "name": int_name,
        "ipv6_enable": True,
        "rip_enable": igp == "rip",
        "ipv6_addresses": int_data["addresses"],
        # Data left here for next steps
        "neighbour": int_data["neighbour"],
        "bgp": int_data["bgp"],
    }

    return interface


def main():
    routers = step1("templates/example.yaml", True)
    pprint(routers)
    return routers


if __name__ == "__main__":
    main()
