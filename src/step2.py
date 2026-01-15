#!/usr/bin/env python3

import pprint


# Translate as:router_id to actual ip addresses
def step2(routers: list, verbose: bool = False):
    if verbose:
        print("#STEP 2:")
        print("Resolving BGP loopback addresses and as numbers")

    for r in routers:
        if "bgp" not in r:
            continue

        for n in r["bgp"]["neighbours"]:
            n["address"], n["remote_as"] = __resolve_loopback__(routers, n["address"])

    if verbose:
        print()

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
    step2(routers, verbose=True)
    pprint.pprint(routers)
    return routers


if __name__ == "__main__":
    main()
