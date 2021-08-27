Comment utiliser :
 - Partir le programme et choisir le nombre de recette à générer (1 à 7)


Comment rajouter une recette :

1. Ajouter la recette dans une colonne du fichier recettes.csv

 - Écrire les informations comme suit :
   |----------------------------|
   |      Nom de la recette     |
   |----------------------------|
   |     Catégorie de repas     | (tofu, pâtes, lentilles, fèves, fromage, viande, pois chiches, ...) Usage à suivre
   |----------------------------|
   |   Catégorie de préférence  | (0 : recette fréquente, 1 : recette plus ou moins fréquente, 2 : recette peu fréquente)
   |----------------------------|
   |        Ingrédient 0        |
   |----------------------------|
   | Quantité de l'ingrédient 0 |
   |----------------------------|
   |             ...            |
   |----------------------------| 
   |             ...            |
   |----------------------------|
   |        Ingrédient n        |
   |----------------------------|
   | Quantité de l'ingrédient n |
   |----------------------------| 


2. Ajouter la section d'épicerie de l'ingédient dans le fichier ingredients.csv

 - Écrire les informations comme suit :
   |----------------------------|----------------------------|
   |             ...            |             ...            |
   |----------------------------|----------------------------|
   |         Ingrédient X       |  Section de l'ingrédient X |
   |----------------------------|----------------------------|
   |         Ingrédient Y       |  Section de l'ingrédient Y |
   |----------------------------|----------------------------|

 - Les sections actuelles sont les suivantes : 
	Fruits & Légumes
	Boulangerie
	Rangées
	Réfrigéré
	Congelé
	Autre