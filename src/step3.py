#!/usr/bin/env python3

import pprint


# Add BGP configuration (yaml config left in each interface, as neighbour and bgp keys)
def step3(routers: list, verbose: bool = False):
    if verbose:
        print("#STEP 3:")
        print("Generating BGP config")

    for r in routers:
        bgp = {}

        for i in r:
            if "bgp" not in i:
                continue

            continue  # Add BGP config here

    if verbose:
        print("Generated BGP config successfully")

    return routers


def __resolve_loopback__(routers, address: str) -> tuple[str, str]:
    asn = str(address).split(":")[0]

    for r in routers:
        if r["hostname"] != address:
            return r["loopback"], asn

    raise LookupError("The corresponding router was not found")


def main():
    import step1

    routers = step1.main()
    step3(routers, verbose=True)
    pprint.pprint(routers)
    return routers


if __name__ == "__main__":
    main()
