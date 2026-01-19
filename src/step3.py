#!/usr/bin/env python3

import pprint


# Add BGP configuration (yaml config left in each interface, as neighbour and bgp keys)
def step3(data: dict, routers: list, verbose: bool = False):
    if verbose:
        print("#STEP 3:")
        print("Generating BGP config")
    bgp = __extract_bgp_config__(data)
    __apply_bgp_config__(routers, bgp)
    __resolve_neighbours_ips__(data, routers)

    return routers


def __extract_bgp_config__(data: dict) -> dict:
    bgp = {}

    for aid, a in data.items():
        for rid, r in a["routers"].items():
            __proccess_router__(bgp, aid, rid, r)

    return bgp


def __proccess_router__(bgp: dict, as_number: int, router_id: str, router: dict):
    for interface in router["interfaces"].values():
        if "bgp" not in interface:
            return

        hostname = f"{as_number}:{router_id}"

        # This host already has one neighbour
        if hostname in bgp.keys():
            bgp[hostname].append(interface["neighbour"])
            continue

        bgp[hostname] = [interface["neighbour"]]


def __apply_bgp_config__(routers: list, bgp: dict) -> list:
    for router in routers:
        if router["hostname"] in bgp.keys():
            hostname = router["hostname"]
            current_as, current_router_id = hostname.split(":")

            router["bgp"] = {
                "as": current_as,
                "router_id": current_router_id,
                "neighbours": bgp[hostname],
            }

    return routers


def __resolve_neighbours_ips__(data: dict, routers: list):
    for current_router in routers:
        if "bgp" not in current_router:
            continue

        neighbours = current_router["bgp"]["neighbours"]
        for i in range(len(neighbours)):
            neighbour_as_number = neighbours[i].split(":")[0]
            neighbours[i] = {
                "address": __resolve_neighbour_ip__(
                    data, neighbours[i], current_router["hostname"]
                )[0],  # Pick the first ip in the list
                "remote_as": neighbour_as_number,
            }


def __resolve_neighbour_ip__(
    data: dict, neighbour: str, current_router_id: str
) -> list:
    neighbour_as_number, neighbour_router_id = neighbour.split(":")

    for interface in data[int(neighbour_as_number)]["routers"][neighbour_router_id][
        "interfaces"
    ].values():  # Loop over the interfaces of our desired router
        if interface["neighbour"] == current_router_id:
            return interface["addresses"]


def main():
    import step1
    import step2

    data = step1.main()
    routers = step2.main()
    step3(data, routers, verbose=True)
    pprint.pprint(routers)
    return routers


if __name__ == "__main__":
    main()
