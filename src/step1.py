#!/usr/bin/python3

import yaml
import ipaddress
import pprint


# Parse yaml config file and transfrom it to match the output structure
def step1(filepath: str, verbose: bool = False) -> list:
    routers = []

    with open(filepath, "r") as f:
        data = yaml.safe_load(f)["ASs"]
        if verbose:
            print("#STEP 1: ")
            print(f"Reading from config: {data}")

        for an, a in data.items():
            __process_as__(routers, an, a)

    return routers


def __process_as__(routers, as_number, as_data):
    i = 0
    for ri, r in as_data["routers"].items():
        # Keep track of whether ospf is enabled router-wide
        ospf = False
        i += 1

        # Add hostname (router id) and computed loopback from loopback_space
        router = {
            "hostname": f"{as_number}:{ri}",
            "loopback": {
                "ipv6": str(ipaddress.IPv6Network(as_data["loopback_space"])[0] + i + 1)
            },
        }

        # Add interfaces
        interfaces = []
        for int_name, int_data in r["interfaces"].items():
            ospf, interface = __process_interface__(int_name, int_data, ospf)
            interfaces.append(interface)

        router["interfaces"] = interfaces

        # Add ospf config if it is enabled
        if ospf:
            router["ospf"] = {"router_id": ri}

        routers.append(router)


def __process_interface__(int_name, int_data, ospf) -> tuple[bool, dict]:
    interface = {
        "name": int_name,
        "ipv6_enable": True,
        "rip_enable": int_data["rip"],
        "ipv6_addresses": int_data["addresses"],
    }

    # Add interface-specific ospf config
    if int_data["ospf"]:
        ospf = True
        interface["ospf_area"] = 0

    return ospf, interface


def main():
    routers = step1("templates/example.yaml", True)
    pprint.pprint(routers)
    return routers


if __name__ == "__main__":
    main()
