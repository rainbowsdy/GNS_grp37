#!/usr/bin/env python3

import ipaddress


def step1(config_data: dict, verbose: bool = False):
    """Step 1: Assign IPv6 /126 networks to interfaces that don't have addresses configured."""
    if verbose:
        print("#STEP 1:")
        print("Assigning networks to interfaces without addresses")

    __assign_networks_across_ases__(config_data)

    if verbose:
        print("Network assignment completed successfully")


def __assign_networks_across_ases__(all_as_data):
    """Assign IPv6 /126 networks to interfaces across all ASes that don't have addresses configured."""
    # Handle ASs wrapper
    if "ASs" in all_as_data:
        all_as_data = all_as_data["ASs"]

    # Collect all interfaces needing addresses
    interfaces_needing_addresses = []

    for as_number, as_data in all_as_data.items():
        networks_space = as_data.get("networks_space")
        if not networks_space:
            continue

        # Parse the networks space
        try:
            network = ipaddress.IPv6Network(networks_space)
        except ipaddress.AddressValueError as e:
            raise ValueError(
                f"Invalid networks_space '{networks_space}' for AS {as_number}: {e}"
            )

        for router_name, router_data in as_data["routers"].items():
            for interface_name, interface_data in router_data["interfaces"].items():
                if "addresses" not in interface_data:
                    interfaces_needing_addresses.append(
                        {
                            "as_number": as_number,
                            "router": router_name,
                            "interface": interface_name,
                            "neighbour": interface_data["neighbour"],
                            "interface_data": interface_data,
                            "networks_space": network,
                        }
                    )

    # Group interfaces by connection (bidirectional)
    connections = {}
    for iface in interfaces_needing_addresses:
        neighbour = iface["neighbour"]
        # Normalize neighbour to full format (AS:Router)
        if ":" not in neighbour:
            # Same AS, add AS number
            neighbour = f"{iface['as_number']}:{neighbour}"

        # Create full identifiers for both sides
        local_id = f"{iface['as_number']}:{iface['router']}"
        remote_id = neighbour

        # Sort to ensure consistent key regardless of which side we process first
        connection_key = tuple(sorted([local_id, remote_id]))
        if connection_key not in connections:
            connections[connection_key] = []
        connections[connection_key].append(iface)

    # Assign /126 subnets to each connection
    subnet_index = 0
    for connection_key, interfaces in connections.items():
        if len(interfaces) != 2:
            raise ValueError(
                f"Connection {connection_key} has {len(interfaces)} interfaces, expected 2"
            )

        # Use the networks_space from the first interface (they should be from same AS or compatible)
        network = interfaces[0]["networks_space"]

        # Generate /126 subnet
        subnet = ipaddress.IPv6Network(
            (network.network_address + subnet_index * 4, 126)
        )
        subnet_index += 1

        # Assign addresses to the two interfaces
        addresses = [
            str(subnet[1]),
            str(subnet[2]),
        ]  # Use .1 and .2, skip .0 (network) and .3 (broadcast)

        for i, iface in enumerate(interfaces):
            iface["interface_data"]["addresses"] = [f"{addresses[i]}/126"]


def main():
    import yaml
    from src.step1 import step1

    # Load config and run step1
    with open("templates/example.yaml", "r") as f:
        data = yaml.safe_load(f)

    step1(data, verbose=True)


if __name__ == "__main__":
    main()
