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
            i = 0
            for ri, r in a["routers"].items():
                # Keep track of whether ospf and bgp are enabled router-wide
                ospf, bgp_neighbours = False, []
                i += 1

                # Add hostname (router id) and computed loopback from loopback_space
                router = {
                    "hostname": f"{an}:{ri}",
                    "loopback": {
                        "ipv6": str(
                            ipaddress.IPv6Network(a["loopback_space"])[0] + i + 1
                        )
                    },
                }

                # Add interfaces
                interfaces = []
                for int_name, int_data in r["interfaces"].items():
                    interface = {
                        "name": int_name,
                        "ipv6_enable": True,
                        "rip_enable": int_data["rip"],
                    }

                    # Add interface-specific ospf config
                    if int_data["ospf"]:
                        ospf = True
                        interface["ospf_area"] = 0

                    # Add interface-specific bgp config
                    if int_data["bgp"]:
                        bgp_neighbours.append(
                            {
                                "address": str(
                                    int_data["neighbour"]
                                ),  # Not an IP address for now
                                "remote_as": None,  # Not a remote as for now
                            }
                        )
                        interface["ipv6_addresses"] = router["loopback"]
                    else:
                        interface["ipv6_addresses"] = int_data["addresses"]

                    interfaces.append(interface)

                router["interfaces"] = interfaces

                # Add ospf and bgp config if they are enabled
                if ospf:
                    router["ospf"] = {"router_id": ri}

                if len(bgp_neighbours):
                    # Transfrom the router ids to loopbacks first

                    router["bgp"] = {
                        "as": an,
                        "router_id": ri,
                        "neighbours": bgp_neighbours,
                        "networks": [],  # Empty networks for now
                    }

                routers.append(router)

    return routers


def main():
    routers = step1("templates/example.yaml", True)
    pprint.pprint(routers)
    return routers


if __name__ == "__main__":
    main()
