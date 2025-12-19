# Générateur de Configurations Cisco pour GNS

Ce projet est un outil pour générer automatiquement des configurations de routeurs Cisco à partir d'une description YAML des systèmes autonomes (AS) et de leurs routeurs. Il est conçu pour faciliter la création de topologies réseau dans des simulateurs comme GNS3.

## Fonctionnalités
- **Parsing de configuration** : Lit un fichier YAML décrivant les AS, leurs IGPs (OSPF, RIP), espaces de loopback, routeurs et interfaces.
- **Génération de configurations** : Utilise des templates Jinja2 pour produire des fichiers de configuration Cisco valides.
- **Support multi-AS** : Gère plusieurs systèmes autonomes dans un seul fichier de configuration.

## Structure du Pipeline
1. **Lecture et sérialisation** : Le fichier `pipeline.py` contient la fonction `read_config` qui parse le YAML et crée des objets AS et Router.
2. **Étapes suivantes** : [À implémenter] Traitement des données pour assigner des adresses IP, configurer les protocoles, etc.
3. **Génération des configs** : Utilisation du template `templates/template_router.j2` pour créer les fichiers de config.

## Installation
Créer un venv et installer les dépendances :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Exemple
Voir `templates/example.yaml` pour un exemple de configuration avec deux AS.
