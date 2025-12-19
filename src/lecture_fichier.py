# import csv

# def lire_fichier_csv(chemin_fichier):
#     """
#     Lis les infos que l'on donne et les met sous forme de liste 2D, une sous liste= un routeur
#     :param chemin_fichier: chemin du fichier cvs source contenant les infos
#     """
#     lignes = []
#     with open(chemin_fichier, newline='', encoding='utf-8') as fichier:
#         lecteur = csv.reader(fichier)
#         for ligne in lecteur:
#             lignes.append(ligne)
    
#     return lignes

# def ajouter_fin_dans_fichier(chemin_fichier, texte):
#     """
#     Ajoute a la fin du fichier cible le texte passé en parametre
    
#     :param chemin_fichier: Chemin du fichier cible
#     :param texte: Texte a écrire
#     """
#     with open(chemin_fichier, "a", encoding="utf-8") as fichier:
#         fichier.write(texte)


#Fichier Obselete, implémentation de l'écriture du fichier de config modifiée