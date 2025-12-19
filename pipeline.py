import yaml
import ipaddress
from src.ecriture import ecriture_config
from src.class_to_dict import convert_as_to_dict_list
from src.models import AS, Router, IGP

# First step of the pipeline : read and serialize yaml config
def read_config(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    ass = {}
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


if __name__ == "__main__":
    
    # Lecture du YAML
    ass_dict = read_config("templates/example.yaml")
    print(read_config("templates/example.yaml"))
    as_list = list(ass_dict.values())
    # Conversion en liste de dicts pour Jinja2
    routers_for_template = convert_as_to_dict_list(as_list)
    ecriture_config(routers_for_template)
