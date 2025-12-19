from jinja2 import Environment, FileSystemLoader
from data import routers
import os

# Dossier des templates
TEMPLATE_DIR = "templates"

# Dossier de sortie
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialisation de Jinja2
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    trim_blocks=True,
    lstrip_blocks=True
)

template = env.get_template("template_router.j2")

# Génération des configurations
for router in routers:
    config = template.render(**router)

    filename = f"{router['hostname']}.cfg"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(config)

    print(f"✔ Configuration générée : {filepath}")
