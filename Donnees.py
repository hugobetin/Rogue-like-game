import numpy as np

#Ce fichier doit contenir toutes les variables globales utilisées, qu'elles soient constantes ou variable.
#Il ne les contient pas encore toutes car les tests sont plus simples avec des variables dans les fichiers concernés. Je les déplace au fur et à mesure que le projet avance.

##Constantes
#Ces variables indiquent la taille de la carte
width_map=20
height_map=20

#Ces variables servent à l'affichage, elles donnent la taille de la représentation d'une case et le nombre de cases affichées (en hauteur et largeur, l'écran est pour l'instant carré).
taille_case=75
taille_ecran=7

#Voici les couleurs que j'utilise pour l'instant. Elles sont codées en RGB.
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY     = ( 124, 124, 124)
YELLOW   = ( 255, 255,   0)
RED      = ( 255,   0,   0)
GREEN    = (   0, 200,   0)
L_BLUE   = (   0, 255, 255)
D_BLUE   = (   0,  90, 180)
BEIGE    = ( 230, 200, 100)

#palette contient la palette du donjon, à savoir la couleur des murs et du sol
palette=[GREEN,BEIGE]

##Variables (valeurs de test)
#Les valeurs écrites ici sont à titre indicatif, les vraies valeurs sont dans l'initialisation (dans IA.py).
#grille_vide contient juste les murs (0), les salles (1), les couloirs (0) et l'escalier (3), c'est-à-dire ce qui ne change pas durant l'exploration de l'étage
#Les bandes de 0 de largeur 3 sont là pour l'affichage graphique.
grille_vide=np.array(  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,0,0,0,0,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,1,0,0,2,2,2,2,2,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,2,0,0,0,0,0,0,0,1,1,1,1,2,0,0,0],
                        [0,0,0,3,1,1,1,0,0,0,0,2,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,1,1,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,1,1,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,2,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,0,2,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,0,2,0,0,0,2,2,1,1,1,1,0,0,0,0,0],
                        [0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,1,1,1,1,0,0,0,0,0],
                        [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

#grille est une copie de grille_vide avec en plus le personnage (4) et les ennemis (5)
grille=np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,5,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,5,0,0,0,0],
                [0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,0,0,0,0,1,1,1,1,0,0,0,0],
                [0,0,0,1,1,1,1,0,0,0,0,1,0,0,2,2,2,2,2,1,1,1,1,0,0,0,0],
                [0,0,0,1,1,1,1,0,0,0,0,2,0,0,0,0,0,0,0,1,1,1,1,2,0,0,0],
                [0,0,0,3,1,1,1,0,0,0,0,2,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,1,1,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,1,1,1,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,1,1,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
                [0,0,0,4,1,1,1,0,0,0,0,0,2,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
                [0,0,0,1,1,1,1,0,0,0,0,0,2,0,0,0,2,2,1,1,1,1,0,0,0,0,0],
                [0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,1,1,1,1,0,0,0,0,0],
                [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    
    
#murs est une carte indiquant les murs, il sert à tracer la carte.
#Pour l'instant, ne fonctionne qu'avec la carte préfabriquée.
#Si la carte a des dimmensions (6+width,6+height), murs a des dimmensions (2*(width+1),2*(height+1).
#La case grille[3+i,3+j] est associée à la case murs[1+2*i][1+2*j]. Les arrêtes sont les 4 cases voisines(murs[2*i][1+2*j],murs[3+2*i][1+2*j],murs[1+2*i][2*j],murs[1+2*i][3+2*j]).
#0 indique qu'il n'y a rien, 1 indique qu'il y a un mur
murs=np.zeros((2*19,2*22))
for i in range(18):
    for j in range(21):
        if grille[3+i,3+j]:
            if not grille[2+i,3+j]:
                murs[2*i][1+2*j]=1
            if not grille[4+i,3+j]:
                murs[2+2*i][1+2*j]=1
            if not grille[3+i,2+j]:
                murs[1+2*i][2*j]=1
            if not grille[3+i,4+j]:
                murs[1+2*i][2+2*j]=1
                
#vus est une carte des zones entrées au moins une fois dans le champs de vision. Il sert à savoir quelle partie de la carte révéler.
#Pour l'instant, ne fonctionne qu'avec la carte préfabriquée.
#vus a le même format que murs. 0 indique une case non-vue, 1 indique une case vue.
vus=np.zeros((2*25,2*28))

#ennemis contient les infos de chaque ennemi, à savoir sa position, sa position précédente et sa cible du moment (pour l'instant).
ennemis=[[[3,3],[0,0],[-1,-1]],[[3,22],[0,0],[-1,-1]]]

#joueur contient les infos du joueur, à savoir sa position (pour l'instant).
joueur=[17,3]
