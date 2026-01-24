import os
from gns3fy import Gns3Connector, Project

def export_config(verbose,project_name):
    # ==============================
    # PARAMÈTRES
    # ==============================
    GNS3_URL = "http://localhost:3080"
    PROJECT_NAME = project_name
    CONFIG_DIR = "output"


    # ==============================
    # CONNEXION GNS3
    # ==============================
    gns3 = Gns3Connector(url=GNS3_URL)
    project = Project(name=PROJECT_NAME, connector=gns3)
    project.get()

    if verbose:
        print(f"[+] Connecté au projet : {project.name}")

    # ==============================
    # RÉCUPÉRATION DES NODES
    # ==============================
    project.get_nodes()

    # ==============================
    # INJECTION DES STARTUP CONFIGS + DÉMARRAGE
    # ==============================
    
    for node in project.nodes:
        if node.node_type not in ["dynamips", "qemu"]:
            continue

        cfg_path = os.path.join(CONFIG_DIR, f"{node.name}.cfg")
        if not os.path.isfile(cfg_path):
            print(f"[-] Aucun fichier de config pour {node.name}")
            continue

        try:
            # Lire la nouvelle config
            with open(cfg_path, "r", encoding="utf-8") as f:
                config_data = f.read()

            # Chemin vers le dossier configs du node
            configs_dir = os.path.join(node.node_directory, "configs")
            os.makedirs(configs_dir, exist_ok=True)

            # Vérifier s'il y a déjà un fichier dans ce dossier
            existing_files = [f for f in os.listdir(configs_dir) if os.path.isfile(os.path.join(configs_dir, f))]
            if existing_files:
                # On prend le premier fichier existant et on le remplace
                target_file = os.path.join(configs_dir, existing_files[0])
            else:
                # Sinon, créer un fichier par défaut "startup-config"
                target_file = os.path.join(configs_dir, "startup-config")

            # Écrire la nouvelle config
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(config_data)

            if verbose:
                print(f"[+] Config remplacée pour {node.name} dans {target_file}")

            # Démarrage du node
            if verbose:
                print(f"[+] Redémarrage du routeur {node.name}")
            node.stop()
            node.start()

        except Exception as e:
            print(f"[!] Erreur sur {node.name} : {e}")

    if verbose:
        print("[+] Tous les routeurs sont traités")