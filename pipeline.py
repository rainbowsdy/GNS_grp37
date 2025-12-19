import yaml
import ipaddress
from src.models import AS, Router, IGP

"""
This file contains the different functions that make the pipeline this project relies on
This pipeline take in a yaml configuration file (I.E. templates/example.yaml) and returns Cisco routers configuration files
The steps of the pipeline are the functions of this file, written in order (first-to-last)
"""

# Step 1: read and serialize yaml config
def read_config(file_path: str, ass: dict[str, "AS"]) -> dict[str, "AS"]:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    for as_key, as_data in data['ASs'].items():
        # Parse IGP
        igp = getattr(IGP, as_data['igp'].upper())
        
        # Parse loopback space
        loopback_space = ipaddress.IPv6Network(as_data['loopback_space'])
        
        # Create Router objects first
        routers_dict = {}
        for r_id, r_data in as_data['routers'].items():
            router = Router(ID=r_id, border=r_data['border'])
            routers_dict[r_id] = router
        
        # Link interfaces (assuming interfaces are lists of router IDs)
        for r_id, router in routers_dict.items():
            interfaces = []
            for intf_id in as_data['routers'][r_id]['interfaces']:
                if intf_id in routers_dict:
                    interfaces.append(routers_dict[intf_id])
            router.interfaces = interfaces
        
        # Create AS object
        as_obj = AS(number=as_key, igp=igp, loopback_space=loopback_space)
        as_obj.routers = list(routers_dict.values())
        
        ass[as_key] = as_obj
    
    return ass


# Step 2: Assign unique loopback IP addresses to routers from their AS's loopback_space
def generate_loopback_addresses(ass: dict[str, "AS"]) -> dict[str, "AS"]:
    for a in ass.values():
        network = a.loopback_space
        for i, router in enumerate(a.routers):
            router.loopback = network.network_address + (i + 1)
            print(router)

    return ass


if __name__ == "__main__":
    ass: dict[str, "AS"] = {}
    read_config("templates/example.yaml", ass)
    generate_loopback_addresses(ass)
    