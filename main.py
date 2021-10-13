import pandas as pd
from numpy import random



## --- Classes & fonction --- ##
class Ingredient:
    def __init__(self, nom, section, quantite):
        self.nom = nom
        self.section = section
        self.quantite = quantite


class Recette:
    def __init__(self, nom, ingredients, preference, categorie):
        self.nom = nom
        self.ingredients = ingredients
        self.preference = preference
        self.categorie = categorie


class Inventaire:
    def __init__(self):
        pass

    recettes = []
    dernieres_recettes = []
    avant_dernieres_recettes = []

    def add_recette(self, recette):
        self.recettes.append(recette)

    def add_dernieres_recettes(self, dernieres, avant_dernieres):
        self.dernieres_recettes = dernieres
        self.avant_dernieres_recettes = avant_dernieres

    def sort_recette_preference(self):
        recettes_preferences = [[], [], []]

        for recette in self.recettes:
            if recette.preference == 0:
                recettes_preferences[0].append(recette)
            elif recette.preference == 1:
                recettes_preferences[1].append(recette)
            elif recette.preference == 2:
                recettes_preferences[2].append(recette)

        return recettes_preferences


def process_ingredients(ingredient_quantite, dictionnaire_ingredients):
    processed_ingredient = []
    for i in range(2, ingredient_quantite.shape[0], 2):
        ingredient = ingredient_quantite[i]
        section = dictionnaire_ingredients[ingredient_quantite[i]]
        quantite = ingredient_quantite[i + 1]
        processed_ingredient.append(Ingredient(ingredient, section, quantite))

    return processed_ingredient


def get_recette_aleatoire(n_recettes, pref, recettes_preference):
    n = random.randint(0, n_recettes)
    recette_candidate = recettes_preference[pref][n]

    return recette_candidate



## --- Crée un dictionnaire pour associer les ingrédients aux sections d'épicerie --- ##
liste_ingredients = pd.read_csv("ingredients.csv", sep=";")
dictionnaire_ingredients = dict()
for ingredient, section in zip(liste_ingredients["Ingrédients"], liste_ingredients["Sections"]):
    dictionnaire_ingredients[ingredient] = section

## --- Déclare & remplis l'inventaire --- ##
inventaire = Inventaire()

# Ajoute les recettes dans l'inventaire
recettes = pd.read_csv("recettes.csv", sep=";")
for recette_info in recettes:
    ingredients = process_ingredients(recettes[recette_info].dropna(), dictionnaire_ingredients)
    recette = Recette(recette_info, ingredients, int(recettes[recette_info][1]), recettes[recette_info][0])
    inventaire.add_recette(recette)



## --- Génération du menu de la semaine --- ##
menu = []
noms_recettes = []

# Tri les recettes selon les préférences
recettes_preference = inventaire.sort_recette_preference()


# Permet de choisir des recettes dans le génétateur automatique ou un liste personnalisée
def choisir_recette(recettes):
    tag_recette = {}
    i = 0
    print('\n-- Inventaire des recettes --')
    for preference in recettes:
        for recette in preference:
            print(i, recette.nom)
            tag_recette[str(i)] = recette
            i += 1

    continu = True
    liste_recette = []
    while continu == True:
        j = input("\nChoisir une recette (numéro) : ")
        liste_recette.append(tag_recette[j])

        k = input("Choisir d'autres recette ? (oui/non) : ")
        if k == "non":
            continu = False

    return liste_recette




def check(recette, menu):
    reponse = input(f"Est-ce que la recette ({recette.nom}) convient? (oui/non) : ")

    if reponse == "oui":
        menu.append(recette)
    elif reponse == "non":
        nouvelle_liste = choisir_recette(recettes_preference)

        for nouvelle_recette in nouvelle_liste:
            menu.append(nouvelle_recette)
    else:
        print("Tu sais pas écrire, alors je décide que oui!")
        menu.append(recette)

# Ajoute l'historique des 2 dernières semaines (si semaine 1, crée des semaines temporaires)
historique = pd.DataFrame()
try:
    historique = pd.read_csv("historique_recettes.csv", sep=";")
    if historique.shape[1] == 1:
        historique["Semaine -1"] = [0, 0, 0, 0, 0, 0, 0]
except:
    historique["Semaine -2"] = [0, 0, 0, 0, 0, 0, 0]
    historique["Semaine -1"] = [0, 0, 0, 0, 0, 0, 0]

def generateur_auto(nb):
    dernieres = list(historique[historique.columns[-1]].dropna())
    avant_dernieres = list(historique[historique.columns[-2]].dropna())
    inventaire.add_dernieres_recettes(dernieres, avant_dernieres)

    # Catégories et préférences (WIP)
    #preferences = [0, 1, 2]  # 0 : Souvent | 1 : Normal | 2 : Rarement
    #categories = ["tofu", "lentilles", "viande", "pates", "poissons"]

    ## --- Nombre de recette selon la préférence et selon le nombre de recette à générer --- ##
    # [nb préférence 0, nb préférence 1, nb préférence 2]
    liste = []
    if nb == 1:
        liste = [1, 0, 0]
    elif nb == 2:
        liste = [1, 1, 0]
    elif nb == 3:
        liste = [1, 1, 1]
    elif nb == 4:
        liste = [1, 2, 1]
    elif nb == 5:
        liste = [2, 2, 1]
    elif nb == 6:
        liste = [2, 2, 2]
    elif nb == 7:
        liste = [2, 3, 2]


    # Loop sur le nombre de recette par préférence
    for pref, n_preference in enumerate(liste):
        if n_preference > 0:
            n_recettes = len(recettes_preference[pref])

            for x in range(0, n_preference):
                recette_candidate = get_recette_aleatoire(n_recettes, pref, recettes_preference)
                while recette_candidate in menu:  # Cherche une recette qui n'est pas déjà dans le menu de la semaine
                    recette_candidate = get_recette_aleatoire(n_recettes, pref, recettes_preference)

                # Recherche si la recette a été fait dans la/les semaines précédantes selon la préférence
                if pref == 0:  # Si pref = 0, peut être choisie chaque semaine
                    check(recette_candidate, menu)
                elif pref == 1:  # Si pas dans la dernière semaine
                    while (recette_candidate.nom in inventaire.dernieres_recettes or
                           recette_candidate in menu):
                        recette_candidate = get_recette_aleatoire(n_recettes, pref, recettes_preference)

                    check(recette_candidate, menu)
                elif pref == 2:  # Si pas dans les deux dernières semaines
                    while (recette_candidate.nom in inventaire.dernieres_recettes or
                           recette_candidate.nom in inventaire.avant_dernieres_recettes or
                           recette_candidate in menu):
                        recette_candidate = get_recette_aleatoire(n_recettes, pref, recettes_preference)

                    check(recette_candidate, menu)

                # Vérifie si le nombre de recette est bon
                if len(menu) >= nb:
                    break

## --- Nombre de recette à générer --- ##
choix = input("Génétateur automatique (0) ou choisir des recettes (1) : ")
if choix == "0":
    nb = input("Nombre de recettes à générer (1 à 7) : ")
    nb = int(nb)
    generateur_auto(nb)
else:
    recettes = choisir_recette(recettes_preference)

    for recette in recettes:
        menu.append(recette)


## --- Exporte le menu & enregiste l'historique --- ##
liste_semaine = []
print("\n -- Menu de la semaine --")
for recette in menu:
    liste_semaine.append(recette.nom)
    print(recette.nom)


fichier = open("menu_semaine.txt", "w+")
fichier.write(" -- Menu de la semaine --\n")

for recette in liste_semaine:
    fichier.write(recette + "\n")

# Efface des semaines provisoires
if "Semaine -2" in historique:
    historique.drop(['Semaine -2'], axis=1, inplace=True)
if "Semaine -1" in historique:
    historique.drop(["Semaine -1"], axis=1, inplace=True)

historique["Semaine " + str(historique.shape[1] + 1)] = pd.Series(liste_semaine)
historique.to_csv("historique_recettes.csv", index=False, sep=";", encoding='utf-8-sig')


## --- Crée la liste d'épicerie --- ##
liste_epicerie = {"Fruits & Légumes": [], "Boulangerie": [], "Rangées": [], "Réfrigéré": [], "Congelé": [],
                  "Autre": []}

for recette in menu:
    for ingredient in recette.ingredients:
        section = ingredient.section

        # Verifie que l'ingrédient n'est pas déjà dans la liste
        if len(liste_epicerie[section]) > 0:
            qte = ingredient.quantite
            nom = ingredient.nom
            for val in liste_epicerie[section]:
                if val[1] == ingredient.nom:
                    try:
                        int(ingredient.quantite)
                        qte = int(val[0]) + int(ingredient.quantite)
                        qte = str(qte)
                    except ValueError:
                        qte += " + " + ingredient.quantite

                    liste_epicerie[section].remove(val)
                    nom = ingredient.nom
                    break

            liste_epicerie[section].append((qte, nom))
        else:
            liste_epicerie[section].append((ingredient.quantite, ingredient.nom))


## --- Export la liste d'épicerie --- ##
fichier.write("\n\n -- Liste d'épicerie --\n")
for section in liste_epicerie:
    fichier.write(" - " + section + " - \n")
    for qte_ingredient in liste_epicerie[section]:
        fichier.write(qte_ingredient[0] + " " + qte_ingredient[1] + "\n")

    fichier.write("\n")

fichier.close()






