import pandas as pd
import numpy as np

# Nombre de recette à générer
nb = 4

# Lecture du répertoire de recettes, des ingrédients et de l'historique
recettes = pd.read_csv("recettes.csv", sep=";").fillna("")
ingredients = pd.read_csv("ingredients.csv", sep=";")
historique = pd.read_csv("historique_recettes.csv", sep=";")

# Catégories et préférences
preferences = [0, 1, 2]  # 0 : Souvent | 1 : Normal | 2 : Rarement
categories = ["tofu", "lentilles", "viande", "pates", "poissons"]

# Nombre de recette selon la préférence et selon le nombre de recette à générer
# [nb préférence 0, nb préférence 1, nb préférence 2]
if nb == 1:
    liste = [1, 0, 0]
elif nb == 2:
    liste = [1, 1, 0]
elif nb == 3:
    liste = [2, 1, 0]
elif nb == 4:
    liste = [2, 2, 0]
elif nb == 5:
    liste = [2, 3, 0]
elif nb == 6:
    liste = [2, 3, 1]
elif nb == 7:
    liste = [2, 4, 1]

# Division des recettes en préférence
recettes_preferences = [pd.DataFrame() for _ in liste]
for column in recettes:
    if recettes[column][1] == str(0):
        recettes_preferences[0][column] = recettes[column]
    elif recettes[column][1] == str(1):
        recettes_preferences[1][column] = recettes[column]
    elif recettes[column][1] == str(2):
        recettes_preferences[2][column] = recettes[column]

# Numéro de la semaine
semaine = historique.shape[1] + 1

# Génération de menu
menu = pd.Series([])
noms_recettes = []
liste_ingredients = []

# Loop sur le nombre de recette par préférence
for pref, n_preference in enumerate(liste):
    i = 0

    # Génère le nombre de recette de telle préférence
    while i < n_preference:
        n_recettes = recettes_preferences[pref].shape[1]  # Nombre de recettes

        # Si le nombre de recette nécessaire = 0, n doit être = 0 (pas d'autres possibilités)
        if n_recettes != 1:
            n = np.random.randint(0, n_recettes)
        else:
            n = 0

        recette = recettes_preferences[pref].iloc[:, n]  # Nombre aléatoire de l'index d'une recette selon la préférence

        # Recherche si la recette a été fait dans la/les semaines précédantes selon la préférence
        if pref == 0:  # Si pref = 0, peut être choisie chaque semaine
            noms_recettes.append(recette.name)
            liste_ingredients.append(recette)
            i = 1 + 1
        elif pref == 1 and ~(historique.iloc[:, -1].str.contains(recette.name, na=False)).any():  # Si pas dans la dernière semaine
            noms_recettes.append(recette.name)
            liste_ingredients.append(recette)
            i = 1 + 1
        elif pref == 2 and ~(historique.iloc[:, -2:-1].str.contains(recette.name, na=False)).any(axis=None):  # Si pas dans les 2 semaines
            noms_recettes.append(recette.name)
            liste_ingredients.append(recette)
            i = 1 + 1


# Enregistre les recettes de la semaine dans le fichier historique
historique["Semaine " + str(semaine)] = pd.Series(noms_recettes)
historique.to_csv("historique_recettes.csv", index=False, sep=";", encoding='utf-8-sig')
print(historique["Semaine " + str(semaine)])


# Crée un dictionnaire pour associer les ingrédients aux sections d'épicerie
dictionnaire_ingredients = dict()
for ingredient, section in zip(ingredients["Ingrédients"], ingredients["Sections"]):
    dictionnaire_ingredients[ingredient] = section


# Crée la liste d'épicerie selon la section
liste_epicerie = pd.DataFrame(["Section", "Nombre", "Ingrédients"])




a = 0




