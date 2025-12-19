
# import lecture_fichier as lf  

# def fin_init_routeur(chemin_fichier):
#     """
#     Je sais que ça s'appelle fin_"INIT"_routeur mais cette fonction 
#     DOIT s'executer a la toute fin de la config,\n
#     elle permet de rajouter la bonne fin aux fichier config
#     (la bonne fin etant l'exemple de config vierge)

#     :param chemin_fichier: Chemin vers le fichier cible
#     """
#     with open("exemple_config_vierge.cfg", "r", encoding="utf-8") as f:
#         contenu = f.read()
#     lf.ajouter_fin_dans_fichier(chemin_fichier, contenu)

# def config_interface(nom_interface,subnet_address,chemin_fichier):
#     """
#     Configure une interface, lui associe une adresse avec EUI-64 dans le subnet
    
#     :param nom_interface: STR Gigabitethernet0/0 par exemple...
#     :param subnet_address: STR prefixe d'addresse qui est non alloué ( en /64 )
#     :param chemin_fichier: le chemin du fichier config pour le routeur cible
#     """
#     string= f"interface %s\n ipv6 address %s/64 eui-64",nom_interface,subnet_address
#     lf.ajouter_fin_dans_fichier()

#Fichier Obselete, implémentation de l'écriture du fichier de config modifiée