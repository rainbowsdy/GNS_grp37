# Générateur de Configurations Cisco pour GNS

Ce projet est un outil pour générer automatiquement des configurations de routeurs Cisco à partir d'une description YAML des systèmes autonomes (AS) et de leurs routeurs. Il est conçu pour faciliter la création de topologies réseau dans des simulateurs comme GNS3.

## Fonctionnalités

- **Parsing de configuration** : Lit un fichier YAML décrivant les AS, leurs IGPs (OSPF, RIP), espaces de loopback, routeurs et interfaces.
- **Génération de configurations** : Utilise des templates Jinja2 pour produire des fichiers de configuration Cisco valides.
- **Support multi-AS** : Gère plusieurs systèmes autonomes dans un seul fichier de configuration.

## Structure du Pipeline

1. **Lecture et sérialisation** : Le fichier `pipeline.py` contient la fonction `read_config` qui parse le YAML et crée des objets AS et Router.
2. **Étapes suivantes** : Traitement des données pour assigner des adresses IP, configurer les protocoles, etc.
3. **Génération des configs** : Utilisation du template `templates/template_router.j2` pour créer les fichiers de config.
4. **Export des configs vers GNS3** : Export des fichiers des configs vers un fichier GNS3 ouvert au préalable, et ou la structure physique du réseau est configuré.

Des informations supplémentaires sont disponible a l'aide du flag `-h` ou `--help` .

## Installation

Créer un venv et installer les dépendances :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilsation du programme
Afin de générer des configurations pour un réseau il faut donc:
1. Rédiger le fichier d'intention selon le format explicité plus bas.
1. Éxecuter le fichier pipeline.py avec `-f CHEMIN_FICHIER` en argument. 
1. (Optionel) Pour exporter les configurations, indiquer `-p NOM_PROJET_GNS3` a l'execution.

## Fichier d'intention

Vous pouvez trouver un exemple complet dans `templates/example.yaml`, avec une démo des IGPs supportés dans 3 AS différents.

### AS

Le fichier est organisé par AS de la façcon suivante:

```yaml
ASs:
 111:
  ...
 112:
  ...
```

*A noter que l'en-tête `ASs` n'est pas obligatoire:*

```yaml
111:
 ...
112:
 ...
```

On configure ensuite les paramètres suivants:

```yaml
111:
 igp: "(ospf|rip|ibgp)" # Applicable sur tout l'AS (obligatoire)
 loopback_space: "2001::/64" # Espace d'adresses de loopback des routeurs (obligatoire)
 networks_space: "2001:db8::/48" # Espace pour générer automatiquement des sous-réseaux /126 (optionnel)
```

### Routeurs

Chaque AS contient plusieurs routeurs, indiqués par leurs ID:

```yaml
111:
 routers:
  R1:
   ...
  R2:
   ...
```
Chaque routeur doit avoir un nom distinct.

La configuration d'un routeur inclus une liste d'interfaces:

```yaml
R1:
 ospf_area: 0 # Valide si igp est ospf, vaut 0 par défaut
 interfaces:
  GigabitEthernet0/0:
   ...
  GigabitEthernet0/1:
   ...
```

### Interfaces

Une interface est configurée de la façon suivante:

```yaml
GigabitEthernet0/0:
 neighbour: "[as_number:](router_id)" # as_number optionnel si le routeur est dans le même AS
 ospf_metric: 100 # Doit match celle du neighbour (ou être définie à un seul endroit). Valide si ibgp est ospf
 bgp: "(none|peer|client|provider)" # optionnel, none par défaut
 addresses: # Spécifie une liste d'adresses IPv6 (optionnel - généré automatiquement si absent, à condition de spécifier networks_space plus haut)
  - "2001::1/64"
  - "2001::2/64"
```

Si `addresses` n'est pas spécifié, le système génère automatiquement une adresse IPv6 dans un sous-réseau /126 à partir de `networks_space` de l'AS. Les deux interfaces connectées recevront des adresses dans le même sous-réseau.

## Export de la config vers GNS3
L'export est réalisé via gns3fy une bibliotheque qui permet, en se connectant a l'API GNS3, d'injecter directement les configurations générée en tant que startup config des routeurs.