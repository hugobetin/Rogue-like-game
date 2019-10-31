import pygame
#import os
#os.chdir("C:\\Users\\User\\Documents\\Programmes perso\\Digimon donjon mystère\\Programme")
#Ces 2 lignes ne sont pas toujours nécessaires selon votre logiciel. Mettez l'adresse du classeur contenant les fichiers.

from IA import *
import Donnees as dn
from Map_generator import creer_etage
import Graphismes as gr

##Constante d'affichage et de fonctionnement
#Ces constantes servent pour le bon fonctionnement de pygame, et pour l'affichage de l'écran.
#Certaines constantes sont écrites en majuscule, c'était la typographie utilisée dans les templates pygame que j'ai conservée.


#Voici la taille de la fenêtre d'affichage.
WIDTH=dn.taille_ecran*dn.taille_case
HEIGHT=dn.taille_ecran*dn.taille_case
size=(WIDTH,HEIGHT)

screen=pygame.display.set_mode(size)        #Cette ligne crée un écran à afficher.
pygame.display.set_caption("Fan donjon mystère")           #Cette ligne donne un nom à la fenêtre.
clock = pygame.time.Clock()                 #Cette ligne crée une horloge.

screen.set_colorkey(dn.BLACK)                  #Cette ligne indique que la couleur de fond de l'écran est le noir.


##Variable d'action

done = False                    #done indique quand la fenêtre doit se fermer.
#Les 4 prochaines variables indiquent si une direction est voulue par le joueur.
droite=False
gauche=False
haut=False
bas=False
#mvt indique si le joueur a bougé pendant ce tour
mvt=False

init()              #init vient de IA.py, elle remet à zéro les données.
                    #Sans cette fonction, fermer et ouvrir la fenêtre font reprendre le jeu au même point.

while not done:
    #Màj automatique: si le joueur est sur un escalier, un nouvel étage est généré
    if dn.grille_vide[tuple(dn.joueur)]==3:
        init()
    
    
    #Evènements: Cette boucle traite les entrées de clavier et de souris et les stocke.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #Cliquer sur fermer (indispensable pour fermer la fenêtre).
            done= True
            
        elif event.type==pygame.KEYDOWN:    #Presser une touche
            if event.key==pygame.K_d:       #d=droite
                droite=True
            if event.key==pygame.K_w:       #z=haut
                haut=True
            if event.key==pygame.K_a:       #q=gauche
                gauche=True
            if event.key==pygame.K_s:       #s=bas
                bas=True
        if event.type==pygame.KEYUP:        #Relacher une touche
            if event.key==pygame.K_d:
                droite=False
            if event.key==pygame.K_w:
                haut=False
            if event.key==pygame.K_a:
                gauche=False
            if event.key==pygame.K_s:
                bas=False
    #Actualiser le jeu
    
    #Si l'une des commandes est pressée et que la direction est libre, avancer dans cette direction (ordre arbitraire). Noter si un mouvement a été effectué.
    if droite and dn.grille[dn.joueur[0],[dn.joueur[1]+1]] in [1,2,3]:
        dn.grille[dn.joueur[0],[dn.joueur[1]+1]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[1]+=1
        mvt=True
    elif gauche and dn.grille[dn.joueur[0],[dn.joueur[1]-1]] in [1,2,3]:
        dn.grille[dn.joueur[0],[dn.joueur[1]-1]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[1]+=-1
        mvt=True
    elif haut and dn.grille[dn.joueur[0]-1,[dn.joueur[1]]] in [1,2,3]:
        dn.grille[dn.joueur[0]-1,[dn.joueur[1]]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[0]+=-1
        mvt=True
    elif bas and dn.grille[dn.joueur[0]+1,[dn.joueur[1]]] in [1,2,3]:
        dn.grille[dn.joueur[0]+1,[dn.joueur[1]]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[0]+=1
        mvt=True
    else:
        mvt=False
    
    #Si le joueur a bougé, les ennemis bougent aussi
    if mvt:
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))
        
    
    #Actualiser la carte:
    #On vérifie si on est dans une salle
    salle=dn.grille_vide[dn.joueur[0],dn.joueur[1]] in [1,3]
    
    #On adapte le champs de vision selon si l'on est dans une salle ou non
    if salle:       #Dans une salle, on voit la salle +1 case
        vision=[dn.joueur[0]-1,dn.joueur[0]+1,dn.joueur[1]-1,dn.joueur[1]+1]
        while dn.grille_vide[vision[0],dn.joueur[1]] in [1,3]:
            vision[0]+=-1
        while dn.grille_vide[vision[1],dn.joueur[1]] in [1,3]:
            vision[1]+=1
        while dn.grille_vide[dn.joueur[0],vision[2]] in [1,3]:
            vision[2]+=-1
        while dn.grille_vide[dn.joueur[0],vision[3]] in [1,3]:
            vision[3]+=1
            
    else:           #Dans un couloir, on voit à 2 cases
        vision[0]=dn.joueur[0]-2
        vision[1]=dn.joueur[0]+2
        vision[2]=dn.joueur[1]-2
        vision[3]=dn.joueur[1]+2
    
    #On note comme vue chaque case du champs de vision et ses arrêtes(voir Donnees.py)
    for i in range(vision[0],vision[1]+1):
        for j in range(vision[2],vision[3]+1):
            dn.vus[1+2*i,1+2*j]=1
            dn.vus[1+2*i,2*j]=1
            dn.vus[1+2*i,2+2*j]=1
            dn.vus[2*i,1+2*j]=1
            dn.vus[2+2*i,1+2*j]=1
    
    #Actualiser les graphismes
    gr.afficher_ecran(screen,vision)
    
    # Attendre un peu pour reboucler (10 pour 1/10 seconde).
    clock.tick(10)

#Pour fermer la fenêtre si l'on clique sur le bouton, très important.
pygame.quit()

