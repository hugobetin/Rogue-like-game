Le but de ce projet est de programmer par moi-même un jeu rogue-like, très proche des jeux 'donjon mystère'.

Avec ce projet, je cherche à tester mes compétences en Python et mon approche des mécaniques de gameplay.
J'ai choisi cette série de jeux car c'est une série que j'adore, et dont je connais assez bien le fonctionnement.
J'ai fait assez peu de recherche pour ce travail, car mon but est surtout de trouver une approche pour implémenter ce jeu.

Pour l'instant, mes sources extérieures se limitent à:
-https://www.pygame.org/docs/
pour l'utilisation du module pygame
-https://gamedevelopment.tutsplus.com/tutorials/how-to-use-bsp-trees-to-generate-game-maps--gamedev-12268
pour la génération d'étage, problème auquel je n'ai pas trouvé de solution seul.

Dans l'état actuel, mon programme permet de faire se déplacer un personnage (rond jaune) dans un donjon prédéfini (sol marron, murs verts).
Des ennemis (ronds rouges) dotés d'une intelligence basique explorent le donjon et suivent le joueur s'ils le voient.
Le 'but' du joueur est d'atteindre un escalier (carré bleu), même s'il n'y a pour l'instant pas de victoire implémentée.
Même si elle n'est pas encore intégrée au jeu, une fonction permettant de générer un étage aléatoire a été implémentée.

Remarques:
-je code en python car c'est le langage avec lequel je suis le plus familier.
De plus, sa simplicité de lecture me permet de me concentrer sur l'aspect algorithmique du projet.
J'utilise Pyzo comme environnement de travail.

-le fichier 'Visualisation IA.py' sert de main, il avait un but plus spécifique au départ mais j'ai fini par y intégrer la boucle principale.
Il suffit donc de le lire pour lancer le jeu (attention tout de même au point suivant).

-dans le fichier 'Visualisation IA.py', l'utilisation de la bibliothèque os n'est pas toujours nécessaire.
Personellement, je préfère la rajouter pour être sûr que le bon fichier est chargé.
A modifier selon vos préférences.

-Le document 'Organisation des données.docx' réunit la description des différents raccourcis utilisés pour transmettre des données.
Par exemple, il permet d'interpréter la carte sous forme de grille de chiffre.

-J'ai tendance à oublier de corriger les commentaires déjà écrits.
Je vais faire de mon mieux pour faire attention, mais ne soyez pas surpris si un commentaire décrit un comportement qui ne s'applique pas.
