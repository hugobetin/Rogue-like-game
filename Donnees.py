import numpy as np
import pygame


#Ce fichier doit contenir toutes les variables globales utilisées, qu'elles soient constantes ou variable.
#Il ne les contient pas encore toutes car les tests sont plus simples avec des variables dans les fichiers concernés. Je les déplace au fur et à mesure que le projet avance.

#dossier contient le chemin du dossier de mon jeux. Il est plus simple de le stocker ici que de le réécrire à chaque fois que je souhaite chercher une ressource
dossier="C:\\Users\\User\\Documents\\Programmes perso\\Donjon mystère\\"

##Constantes
#Ces variables indiquent la taille de la carte
width_map=20
height_map=20

#Ces variables servent à l'affichage, elles donnent la taille de la représentation d'une case et le nombre de cases affichées (en hauteur et largeur, l'écran est pour l'instant carré).
taille_case=75
taille_ecran=7

#Voici les couleurs que j'utilise pour l'instant. Elles sont codées en RGB.
BACK     = (   0,   0,   0)
BLACK    = (   1,   1,   1)
WHITE    = ( 255, 255, 255)
GREY     = ( 124, 124, 124)
YELLOW   = ( 255, 255,   0)
RED      = ( 255,   0,   0)
GREEN    = (   0, 200,   0)
L_BLUE   = (   0, 255, 255)
D_BLUE   = (   0,  90, 180)
BEIGE    = ( 230, 200, 100)
ORANGE   = ( 255, 150,   0)

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

#ennemis contient les infos de chaque ennemi, à savoir sa position, sa position précédente, sa cible du moment et sa direction (pour l'instant).
ennemis=[{0:[3,3],1:[0,0],2:[-1,-1],"direction":"down","type":"gobelin", "etat":"still"},
        {0:[3,22],1:[0,0],2:[-1,-1],"direction":"down","type":"gobelin", "etat":"still"}]

#joueur contient les infos du joueur, à savoir sa position (pour l'instant).
joueur={}
joueur["position"]=[17,3]
joueur["direction"]="down"
joueur["type"]="loup"

joueur["etat"]="still"    #peut être still, walk, attack, dammage
joueur["horloge"]=0
"""
joueur["dammage"]=False
joueur["attack"]=False
"""
#etage correspond au numéro de l'étage en cours.
etage=1
