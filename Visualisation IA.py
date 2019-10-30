import pygame
#import os
#os.chdir("C:\\Users\\User\\Documents\\Programmes perso\\Digimon donjon mystère\\Programme")
#Ces 2 lignes ne sont pas toujours nécessaires selon votre logiciel. Mettez l'adresse du classeur contenant les fichiers.
from IA import *
import Donnees as dn
from Map_generator import creer_etage

##Constante d'affichage et de fonctionnement
#Ces constantes servent pour le bon fonctionnement de pygame, et pour l'affichage de l'écran.
#Certaines constantes sont écrites en majuscule, c'était la typographie utilisée dans les templates pygame.

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

#Voici la taille de la fenêtre d'affichage.
WIDTH=7*75
HEIGHT=7*75
size=(WIDTH,HEIGHT)

screen=pygame.display.set_mode(size)        #Cette ligne crée un écran à afficher.
pygame.display.set_caption("RPG")           #Cette ligne donne un nom à la fenêtre.
clock = pygame.time.Clock()                 #Cette ligne crée une horloge.

screen.set_colorkey(BLACK)                  #Cette ligne indique que la couleur de fond de l'écran est le noir.

#Ces variables indiquent la taille de la carte
width_map=20
height_map=20

##Variable d'action

done = False                    #done indique quand la fenêtre doit se fermer.
#Les 4 prochaines variables indiquent si une direction est voulue par le joueur.
droite=False
gauche=False
haut=False
bas=False
#mvt indique si le joueur a bougé pendant ce tour
mvt=False

init(width_map,height_map)              #init vient de IA.py, elle remet à zéro les données.
                    #Sans cette fonction, fermer et ouvrir la fenêtre font reprendre le jeu au même point.

while not done:
    #Màj automatique: si le joueur est sur un escalier, un nouvel étage est généré
    if dn.grille_vide[tuple(dn.joueur)]==3:
        init(width_map,height_map)
    
    
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
        x1,x2,y1,y2=dn.joueur[0]-1,dn.joueur[0]+1,dn.joueur[1]-1,dn.joueur[1]+1
        while dn.grille_vide[x1,dn.joueur[1]] in [1,3]:
            x1+=-1
        while dn.grille_vide[x2,dn.joueur[1]] in [1,3]:
            x2+=1
        while dn.grille_vide[dn.joueur[0],y1] in [1,3]:
            y1+=-1
        while dn.grille_vide[dn.joueur[0],y2] in [1,3]:
            y2+=1
            
    else:           #Dans un couloir, on voit à 2 cases
        x1=dn.joueur[0]-2
        x2=dn.joueur[0]+2
        y1=dn.joueur[1]-2
        y2=dn.joueur[1]+2
    
    #On note comme vue chaque case du champs de vision et ses arrêtes(voir Donnees.py)
    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            dn.vus[1+2*i,1+2*j]=1
            dn.vus[1+2*i,2*j]=1
            dn.vus[1+2*i,2+2*j]=1
            dn.vus[2*i,1+2*j]=1
            dn.vus[2+2*i,1+2*j]=1
    
    #Actualiser les graphismes
    x=dn.joueur[0]
    y=dn.joueur[1]
    #L'écran est une grille de 7*7 centrée sur le personnage.
    #On dessine d'abord le fond à l'aide de grille_vide.
    for i in range(7):
        for j in range(7):
            if dn.grille_vide[x-3+i,y-3+j]==3:
                pygame.draw.rect(screen, L_BLUE, [j*75, i*75, 75,75])
            elif dn.grille_vide[x-3+i,y-3+j]==1 or dn.grille_vide[x-3+i,y-3+j]==2:
                pygame.draw.rect(screen, BEIGE,[j*75, i*75, 75,75])
            else:
                pygame.draw.rect(screen, GREEN,[j*75, i*75, 75,75])
    #On met ensuite le personnage au centre.
    pygame.draw.circle(screen, YELLOW, [int(3.5*75), int(3.5*75)],int(0.5*75))
    #Puis on dessine les ennemis.
    for e in dn.ennemis:
        pygame.draw.circle(screen, RED, [int((e[0][1]-y+3+0.5)*75), int((e[0][0]-x+3+0.5)*75)],int(0.5*75))
    
    #Enfin, on dessine la carte.
    for i in range(width_map+1):
        for j in range(height_map+1):
            #Pour chaque case, on vérifie s'il y a un escalier. S'il y en a un, on le marque d'un carré bleu ciel
            if dn.grille_vide[3+i,3+j]==3 and dn.vus[1+2*(3+i),1+2*(3+j)]:
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,25+1+i*5),(30-1+j*5,25+1+i*5))
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,30-1+i*5),(30-1+j*5,30-1+i*5))
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,25+1+i*5),(25+1+j*5,30-1+i*5))
                pygame.draw.line(screen,L_BLUE,(30-1+j*5,25+1+i*5),(30-1+j*5,30-1+i*5))
            #Ensuite, on trace en blanc les murs, verticaux ou horizontaux selon leurs coordonnées.
            if dn.vus[2*(3+i),1+2*(3+j)] and dn.murs[2*i,1+2*j]:
                pygame.draw.line(screen,WHITE,(25+j*5,25+i*5),(30+j*5,25+i*5))
            if dn.vus[1+2*(3+i),2*(3+j)] and dn.murs[1+2*i,2*j]:
                pygame.draw.line(screen,WHITE,(25+j*5,25+i*5),(25+j*5,30+i*5))
    #On place le personnage sur la carte, et les ennemis en vue.
    pygame.draw.circle(screen, YELLOW, [int(25+(y-3+0.5)*5)+1, int(25+(x-3+0.5)*5)+1],2)
    for e in dn.ennemis:
        if e[0][0]<=x2 and e[0][0]>=x1 and e[0][1]<=y2 and e[0][1]>=y1:
            pygame.draw.circle(screen, RED, [int(25+(e[0][1]-3+0.5)*5)+1, int(25+(e[0][0]-3+0.5)*5)+1],2)
    
    #On affiche l'écran actualisé.
    pygame.display.flip()
    # Attendre un peu pour reboucler (10 pour 1/10 seconde).
    clock.tick(10)

#Pour fermer la fenêtre si l'on clique sur le bouton, très important.
pygame.quit()

