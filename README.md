Le but de ce projet est de programmer par moi-même un jeu rogue-like, très proche des jeux 'donjon mystère'.

Avec ce projet, je cherche à tester mes compétences en Python et mon approche des mécaniques de gameplay.
J'ai choisi cette série de jeux car c'est une série que j'adore, et dont je connais assez bien le fonctionnement.
J'ai fait assez peu de recherche pour ce travail, car mon but est surtout de trouver une approche pour implémenter ce jeu.

Pour l'instant, mes sources extérieures se limitent à:

-https://www.pygame.org/docs/ pour l'utilisation du module pygame
-https://gamedevelopment.tutsplus.com/tutorials/how-to-use-bsp-trees-to-generate-game-maps--gamedev-12268 pour la génération d'étage, problème auquel je n'ai pas trouvé de solution seul.

Le concept de mon jeu est le suivant: un personnage se déplace dans un donjon généré aléatoirement.
A chaque étage, il y a un escalier permettant d'accéder à l'étage suivant, et des ennemis.
Le but du joueur est d'atteindre le fond du donjon.
Chaque étage est organisé en grille et fonctionne au tour par tour: les ennemis se déplacent uniquement en même temps que le joueur.

Remarques:
-je code en python car c'est le langage avec lequel je suis le plus familier.
De plus, sa simplicité de lecture me permet de me concentrer sur l'aspect algorithmique du projet.
J'utilise Pyzo comme environnement de travail.

-Pour lancer le jeu, il faut:

  *télécharger tout les fichiers ici présent dans un même dossier (disons "Jeu").
  
  *Mettre l'addresse du dossier "Jeu" dans la variable "dossier" du fichier "Donnees.py" (penser à doubler les \ pour éviter que l'IDE y voit des commandes).
  
  *lancer la commande 'pip install -r requirements.txt' si besoin pour installer les bibliothèques nécessaires.
    
  *lancer le fichier "Main.py".

-dans le fichier 'Main.py', j'utilise la fonction os.chdir pour indiquer à mon IDE où travailler.
Elle est en commentaire ici car elle n'est pas toujours nécessaire selon l'IDE.
Si le jeu ne démarre pas car le programme ne connait pas les autres fichiers, il faut mettre l'adresse du dossier "Jeu".
N'utilisez pas Donnees.dossier car ce fichier n'a pas encore été lu à cette étape du code.

-Le document 'Organisation des données.txt' réunit la description des différents raccourcis utilisés pour transmettre des données.
Par exemple, il permet d'interpréter la carte sous forme de grille de chiffre.

-J'ai tendance à oublier de corriger les commentaires déjà écrits.
Je vais faire de mon mieux pour faire attention, mais ne soyez pas surpris si un commentaire décrit un comportement qui ne s'applique pas.


Etat du jeu et mises à jour:

31/10/2019:

-Le joueur peut explorer un nombre infini d'étage, le jeu n'a pas encore de fin.

-A chaque étage, une carte est créée et le joueur est placé dedans aléatoirement.

-Il y a aussi 2 ennemis qui suivent le joueur s'ils le voient. Ils bloquent le passage du joueur

-Une carte de l'étage en cours est en permanence affichée à l'écran, montrant ce qui a déjà été découvert.


20/11/2019:

-Possibilité d'afficher du texte

-Affichage du numéro d'étage


16/12/2019:

-J'ai commencé l'implémentation de sprites. Les images que j'utilise/ compte utiliser sont dans le dossier Images. Les sprites déjà présents sont ceux des personnages (joueur et ennemis). Il y a aussi une animation simple.

-Ajout de propriétés sur le joueur et les ennemis: le type (pour les sprites), la direction regardée, l'état (marche, attaque, dommage, rien) et une horloge interne pour gérer les sprites et l'animation.

-Ajout de deux nouvelles actions (besoin d'un pavé numérique): le 1 fait passer son tour, et donc fait défiler le temps; le 2 fait attaquer si un ennemi est juste devant le joueur et le tue.

-Ajout d'un écran titre au lancement, espace pour le passer.

-Modifications mineures visibles: carte agrandie, champs de vision retravaillé, modification de l'IA (plus efficace en cas simple)

-Modifications mineures cachées: distinction BLACK (couleur noire) et BACK (couleur transparente de certains sprites), possibilité de modifier la taille du texte, et quelques autres détails


A venir (liste à titre indicative, je peux vouloir tester autre chose entre temps):

-finir l'implémentation des sprites (pour le donjon en lui-même)

-définir des classes. Cette étape va être essentielle afin de simplifier l'implémentation de mécaniques de RPG avec des méthodes

-lisser l'animation: faire en sorte que le personnage glisse d'une case à l'autre au lieu de sauter

-séparer des modes de jeux: un mode "écran titre", un mode "exploration de donjon", un mode "base d'opération", ...

-ajouter de la musique

