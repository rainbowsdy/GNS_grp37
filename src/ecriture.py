from jinja2 import Environment, FileSystemLoader
import os



def ecriture_config(routers_for_template,verbose):
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
    # Config par routeur
    template = env.get_template("template_router_test.j2")
    for router in routers_for_template:
        config = template.render(**router)

        emplacement= router['hostname'].split(":") # [0] est l'AS , [1] est le nom du routeur

        filename = f"{emplacement[1]}.cfg"
        filepath = os.path.join(OUTPUT_DIR, emplacement[0])
        os.makedirs(filepath, exist_ok=True)
        filepath = os.path.join(filepath, filename)

        with open(filepath, "w") as f:
            f.write(config)

        if verbose:
            print(f"Configuration générée : {filepath} \n\n")
