import pygame
import os
os.chdir("C:\\Users\\User\\Documents\\Programmes perso\\Digimon donjon mystère\\Programme")
from IA import *
import Donnees as dn
from Map_generator import CreerEtage
##Constante d'affichage et de fonctionnement
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREY     = ( 124, 124, 124)
YELLOW   = ( 255, 255,   0)
RED      = ( 255,   0,   0)
GREEN    = (   0, 200,   0)
L_BLUE   = (   0, 255, 255)
D_BLUE   = (   0,  90, 180)
BEIGE    = ( 230, 200, 100)
WIDTH=7*75
HEIGHT=7*75
size=(WIDTH,HEIGHT)

screen=pygame.display.set_mode(size)
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

screen.set_colorkey(BLACK)

##Variable d'action
done = False
droite=False
gauche=False
haut=False
bas=False
mvt=False

init()

while not done:
    #Evènements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done= True
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d:
                droite=True
            if event.key==pygame.K_w:
                haut=True
            if event.key==pygame.K_a:
                gauche=True
            if event.key==pygame.K_s:
                bas=True
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                droite=False
            if event.key==pygame.K_w:
                haut=False
            if event.key==pygame.K_a:
                gauche=False
            if event.key==pygame.K_s:
                bas=False
    #Actualiser le jeu
    
    #Si l'une des commandes est pressée et que la direction est libre, avancer dans cette direction (ordre arbitraire)
    if droite and dn.grille[dn.joueur[0],[dn.joueur[1]+1]] in [1,2,3]:
        dn.grille[dn.joueur[0],[dn.joueur[1]+1]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[1]+=1
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))    
    if gauche and dn.grille[dn.joueur[0],[dn.joueur[1]-1]] in [1,2,3]:
        dn.grille[dn.joueur[0],[dn.joueur[1]-1]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[1]+=-1
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))    
    if haut and dn.grille[dn.joueur[0]-1,[dn.joueur[1]]] in [1,2,3]:
        dn.grille[dn.joueur[0]-1,[dn.joueur[1]]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[0]+=-1
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))    
    if bas and dn.grille[dn.joueur[0]+1,[dn.joueur[1]]] in [1,2,3]:
        dn.grille[dn.joueur[0]+1,[dn.joueur[1]]]=4
        dn.grille[dn.joueur[0],[dn.joueur[1]]]=dn.grille_vide[dn.joueur[0]][dn.joueur[1]]
        dn.joueur[0]+=1
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))
    
    #Actualiser la vision:
    #On vérifie si on est dans une salle
    salle=False
    for i in [-1,1]:
        for j in [-1,1]:
            if dn.grille[dn.joueur[0]+i,dn.joueur[1]] and dn.grille[dn.joueur[0],dn.joueur[1]+j] and dn.grille[dn.joueur[0]+i,dn.joueur[1]+j]:
                salle=True
    
    if salle:
        x1,x2,y1,y2=dn.joueur[0]-1,dn.joueur[0]+1,dn.joueur[1]-1,dn.joueur[1]+1
        while (dn.grille[x1,dn.joueur[1]]!=0 and dn.grille[x1,dn.joueur[1]+1]!=0) or (dn.grille[x1,dn.joueur[1]]!=0 and dn.grille[x1,dn.joueur[1]-1]!=0):
            x1+=-1
        while (dn.grille[x2,dn.joueur[1]]!=0 and dn.grille[x2,dn.joueur[1]+1]!=0) or (dn.grille[x2,dn.joueur[1]]!=0 and dn.grille[x2,dn.joueur[1]-1]!=0):
            x2+=1
        while (dn.grille[dn.joueur[0],y1]!=0 and dn.grille[dn.joueur[0]+1,y1]!=0) or (dn.grille[dn.joueur[0],y1]!=0 and dn.grille[dn.joueur[0]-1,y1]!=0):
            y1+=-1
        while (dn.grille[dn.joueur[0],y2]!=0 and dn.grille[dn.joueur[0]+1,y2]!=0) or (dn.grille[dn.joueur[0],y2]!=0 and dn.grille[dn.joueur[0]-1,y2]!=0):
            y2+=1
            
    else:
        x1=dn.joueur[0]-2
        x2=dn.joueur[0]+2
        y1=dn.joueur[1]-2
        y2=dn.joueur[1]+2

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
    for i in range(7):
        for j in range(7):
            if dn.grille_vide[x-3+i,y-3+j]==3:
                pygame.draw.rect(screen, L_BLUE, [j*75, i*75, 75,75])
            elif dn.grille_vide[x-3+i,y-3+j]==1 or dn.grille_vide[x-3+i,y-3+j]==2:
                pygame.draw.rect(screen, BEIGE,[j*75, i*75, 75,75])
            else:
                pygame.draw.rect(screen, GREEN,[j*75, i*75, 75,75])
    pygame.draw.circle(screen, YELLOW, [int(3.5*75), int(3.5*75)],int(0.5*75))
    for e in dn.ennemis:
        pygame.draw.circle(screen, RED, [int((e[0][1]-y+3+0.5)*75), int((e[0][0]-x+3+0.5)*75)],int(0.5*75))
    
    for i in range(19):
        for j in range(22):
            if dn.grille_vide[3+i,3+j]==4 and dn.vus[1+2*(3+i),1+2*(3+j)]:
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,25+1+i*5),(30-1+j*5,25+1+i*5))
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,30-1+i*5),(30-1+j*5,30-1+i*5))
                pygame.draw.line(screen,L_BLUE,(25+1+j*5,25+1+i*5),(25+1+j*5,30-1+i*5))
                pygame.draw.line(screen,L_BLUE,(30-1+j*5,25+1+i*5),(30-1+j*5,30-1+i*5))
            if dn.vus[2*(3+i),1+2*(3+j)] and dn.murs[2*i,1+2*j]:
                pygame.draw.line(screen,WHITE,(25+j*5,25+i*5),(30+j*5,25+i*5))
            if dn.vus[1+2*(3+i),2*(3+j)] and dn.murs[1+2*i,2*j]:
                pygame.draw.line(screen,WHITE,(25+j*5,25+i*5),(25+j*5,30+i*5))
    pygame.draw.circle(screen, YELLOW, [int(25+(y-3+0.5)*5)+1, int(25+(x-3+0.5)*5)+1],2)
    for e in dn.ennemis:
        if e[0][0]<=x2 and e[0][0]>=x1 and e[0][1]<=y2 and e[0][1]>=y1:
            pygame.draw.circle(screen, RED, [int(25+(e[0][1]-3+0.5)*5)+1, int(25+(e[0][0]-3+0.5)*5)+1],2)
    pygame.display.flip()
        # Attendre un peu pour reboucler
    clock.tick(10)

#Pour fermer la fenêtre si l'on clique sur le bouton, très important
pygame.quit()

