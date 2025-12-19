import ipaddress
from src.models import AS, Router, IGP

def convert_as_to_dict_list(as_list: list[AS]) -> list[dict]:
    """
    Transforme une liste d'AS avec leurs routers en une liste de dictionnaires
    compatibles avec le template Jinja2.
    """
    router_dicts = []

    for as_obj in as_list:
        # Génération d'une adresse de loopback pour chaque router à partir de l'espace de l'AS
        loopback_hosts = as_obj.loopback_space.hosts()  # iterator

        for router in as_obj.routers:
            # Attribuer une loopback unique par router
            loopback_ip = str(next(loopback_hosts))

            # Conversion des interfaces en dicts
            interfaces_list = []
            for intf_router in router.interfaces:
                iface_dict = {
                    "name": getattr(intf_router, "ID", "unknown"),
                    "ipv6_addresses": getattr(intf_router, "ipv6_addresses", []),
                    "ipv6_enable": getattr(intf_router, "ipv6_enable", True),
                    "ospf_area": getattr(intf_router, "ospf_area", None),
                    "rip_enable": getattr(intf_router, "rip_enable", None),
                }
                interfaces_list.append(iface_dict)

            # Création du dict router principal
            r_dict = {
                "hostname": router.ID,
                "loopback": {
                    "name": "Loopback0",
                    "ipv6": loopback_ip + "/128"
                },
                "interfaces": interfaces_list
            }

            # BGP si router frontière
            if router.border:
                r_dict["bgp"] = {
                    "as": as_obj.number,
                    "router_id": loopback_ip,  # router-id basé sur loopback
                    "neighbors": [],           # à compléter selon topologie
                    "networks": [ip for iface in interfaces_list for ip in iface.get("ipv6_addresses", [])]
                }

            # IGP selon AS
            if as_obj.igp == IGP.OSPF:
                r_dict["ospf"] = {
                    "process_id": 1,
                    "router_id": loopback_ip
                }
            elif as_obj.igp == IGP.RIP:
                r_dict["rip"] = {
                    "process_name": "RIPNG"
                }

            router_dicts.append(r_dict)

    return router_dicts
