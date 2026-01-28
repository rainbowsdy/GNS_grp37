#!/usr/bin/env python3
from pprint import pprint


def step4_ospf(data: dict, routers: list, verbose: bool = False):
    if verbose:
        print("\n#STEP 4:")
        print("Processing OSPF metrics")

    for as_number, as_data in data.items():
        if as_data.get("igp") != "ospf":
            continue

        if verbose:
            print(f"Processing OSPF for AS {as_number}")

        for router_id, router_data in as_data["routers"].items():
            for interface_name, interface_data in router_data["interfaces"].items():
                if "ospf_metric" not in interface_data:
                    continue  # Skip interfaces without OSPF metric defined

                # Find neighbour hostname
                neighbour_hostname = interface_data["neighbour"]
                if ":" not in neighbour_hostname:
                    neighbour_hostname = f"{as_number}:{neighbour_hostname}"

                # Find neighbour router in data
                neighbour_as, neighbour_rid = neighbour_hostname.split(":")
                neighbour_as_data = data[int(neighbour_as)]
                neighbour_router_data = neighbour_as_data["routers"][neighbour_rid]

                # Find the neighbour interface in data
                current_hostname = f"{as_number}:{router_id}"
                neighbour_metric = None
                neighbour_int_name = None
                for n_int_name, n_int_data in neighbour_router_data[
                    "interfaces"
                ].items():
                    n_neighbour = n_int_data["neighbour"]
                    if ":" not in n_neighbour:
                        n_neighbour = f"{neighbour_as}:{n_neighbour}"
                    if n_neighbour == current_hostname:
                        neighbour_metric = n_int_data.get("ospf_metric")
                        neighbour_int_name = n_int_name
                        break

                if neighbour_int_name is None:
                    raise ValueError(
                        f"Cannot find neighbour interface for {current_hostname}:{interface_name}"
                    )

                current_metric = interface_data["ospf_metric"]

                # Determine the metric to set
                if neighbour_metric is not None and current_metric != neighbour_metric:
                    raise ValueError(
                        f"OSPF metric mismatch between {current_hostname}:{interface_name} and {neighbour_hostname}:{neighbour_int_name}: {current_metric} vs {neighbour_metric}"
                    )

                metric_to_set = (
                    current_metric if neighbour_metric is None else neighbour_metric
                )

                # Add to routers
                # Find current router
                current_router = next(
                    r for r in routers if r["hostname"] == current_hostname
                )
                current_interface = next(
                    i
                    for i in current_router["interfaces"]
                    if i["name"] == interface_name
                )
                if "bgp" not in current_router:
                    current_interface["ospf_metric"] = metric_to_set

                # Find neighbour router
                neighbour_router = next(
                    r for r in routers if r["hostname"] == neighbour_hostname
                )
                neighbour_interface = next(
                    i
                    for i in neighbour_router["interfaces"]
                    if (
                        i["neighbour"]
                        if ":" in i["neighbour"]
                        else f"{neighbour_as}:{i['neighbour']}"
                    )
                    == current_hostname
                )
                if "bgp" not in neighbour_router:
                    neighbour_interface["ospf_metric"] = metric_to_set

    # Add ospf_area to interfaces for routers without bgp in OSPF ASes
    for router in routers:
        if "bgp" in router:
            continue
        as_num, r_id = router["hostname"].split(":")
        as_num = int(as_num)
        if data[as_num].get("igp") == "ospf":
            for interface in router["interfaces"]:
                orig_int_data = data[as_num]["routers"][r_id]["interfaces"][
                    interface["name"]
                ]
                interface["ospf_area"] = orig_int_data.get("ospf_area", 0)

    if verbose:
        print("OSPF metrics processed successfully")

    return routers


# The hostname could be either "router_id" or "as_number:router_id"
def __get_id_from_hostname__(hostname: str) -> str:
    return hostname if ":" not in hostname else hostname.split(":")[1]


def main():
    import step1
    import step3

    data = step1.main()
    routers = step3.main()
    routers = step4_ospf(data, routers, True)
    pprint(routers)
    return routers


if __name__ == "__main__":
    main()
