import lecture_fichier as lf  

def fin_init_routeur(chemin_fichier):
    """
    Je sais que ça s'appelle fin_"INIT"_routeur mais cette fonction 
    DOIT s'executer a la toute fin de la config,\n
    elle permet de rajouter la bonne fin aux fichier config
    (la bonne fin etant l'exemple de config vierge)

    :param chemin_fichier: Chemin vers le fichier cible
    """
    with open("exemple_config_vierge.cfg", "r", encoding="utf-8") as f:
        contenu = f.read()
    lf.ajouter_fin_dans_fichier(chemin_fichier, contenu)

