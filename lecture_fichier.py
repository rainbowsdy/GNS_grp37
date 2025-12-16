import csv

def lire_fichier_csv(chemin_fichier):
    """
    Docstring for lire_fichier_csv
    lit les infos que l'on donne et les met sous forme de liste 2D, une sous liste= un routeur
    :param chemin_fichier: chemin du fichier cvs source contenant les infos
    """
    lignes = []
    with open(chemin_fichier, newline='', encoding='utf-8') as fichier:
        lecteur = csv.reader(fichier)
        for ligne in lecteur:
            lignes.append(ligne)
    
    return lignes

def ajouter_fin_dans_fichier(chemin_fichier, texte):
    """
    Ajoute a la fin du fichier cible le texte passé en parametre
    
    :param chemin_fichier: Chemin du fichier cible
    :param texte: Texte a écrire
    """
    with open(chemin_fichier, "a", encoding="utf-8") as fichier:
        fichier.write(texte)

def fin_init_routeur(chemin_fichier):
    """
    Docstring for fin_init_routeur
    Je sais que ça s'appelle fin_"INIT"_routeur mais cette fonction 
    DOIT s'executer a la toute fin de la config,
    elle permet de rajouter la bonne fin aux fichier config
    (la bonne fin etant l'exemple de config vierge)

    :param chemin_fichier: Chemin vers le fichier cible
    """
    with open("exemple_config_vierge.cfg", "r", encoding="utf-8") as f:
        contenu = f.read()
    ajouter_fin_dans_fichier(chemin_fichier, contenu)

