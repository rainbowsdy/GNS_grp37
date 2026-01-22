#!/usr/bin/env python3

from pprint import pprint


def step4_ibgp(data: dict, routers: list, verbose: bool = False):
    if verbose:
        print("\n#STEP 4 iBGP:")
        print("Configuring iBGP")

    for as_number, as_data in data.items():
        if as_data.get("igp") != "ibgp":
            continue

        if verbose:
            print(f"Configuring iBGP for AS {as_number}")

        as_num = int(as_number)
        router_ids = list(as_data["routers"].keys())

        # Get loopbacks
        loopbacks = {}
        for ri in router_ids:
            router = next(r for r in routers if r["hostname"] == f"{as_number}:{ri}")
            loopbacks[ri] = router["loopback"]["ipv6"]

        for router_id in router_ids:
            current_hostname = f"{as_number}:{router_id}"
            current_router = next(
                r for r in routers if r["hostname"] == current_hostname
            )

            if "bgp" not in current_router:
                current_router["bgp"] = {
                    "as": str(as_num),
                    "router_id": router_id,
                    "neighbours": [],
                }

            # Add all other routers as neighbours
            for other_ri in router_ids:
                if other_ri == router_id:
                    continue
                other_loopback = loopbacks[other_ri]
                neighbour = {
                    "address": {"ipv6": other_loopback},
                    "remote_as": str(as_num),
                }
                if neighbour not in current_router["bgp"]["neighbours"]:
                    current_router["bgp"]["neighbours"].append(neighbour)

    if verbose:
        print("iBGP configured successfully")

    return routers


# The hostname could be either "router_id" or "as_number:router_id"
def __get_id_from_hostname__(hostname: str) -> str:
    return hostname if ":" not in hostname else hostname.split(":")[1]


def main():
    import step1
    import step3

    data = step1.main()
    routers = step3.main()
    routers = step4_ibgp(data, routers, True)
    pprint(routers)
    return routers


if __name__ == "__main__":
    main()
