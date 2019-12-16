import pygame

#import os
#os.chdir("C:\\Users\\User\\Documents\\Programmes perso\\Digimon donjon mystère\\Programme")
#Ces 2 lignes ne sont pas toujours nécessaires selon votre logiciel. Mettez l'adresse du classeur contenant les fichiers.

#Même si le chemin est dans la variable dossier (voir Donnees.py), le fichier n'a pas encore pu être importé. Le chemin entier est donc nécessaire ici.

pygame.init()

import Donnees as dn

##Constante d'affichage et de fonctionnement
#Ces constantes servent pour le bon fonctionnement de pygame, et pour l'affichage de l'écran.
#Certaines constantes sont écrites en majuscule, c'était la typographie utilisée dans les templates pygame que j'ai conservée.


#Voici la taille de la fenêtre d'affichage.
WIDTH=dn.taille_ecran*dn.taille_case
HEIGHT=dn.taille_ecran*dn.taille_case
size=(WIDTH,HEIGHT)

screen=pygame.display.set_mode(size)        #Cette ligne crée un écran à afficher.
pygame.display.set_caption("Donjon mystère")           #Cette ligne donne un nom à la fenêtre.

screen.set_colorkey(dn.BLACK)                  #Cette ligne indique que la couleur de fond de l'écran est le noir.

#Ces bibliothèques ne peuvent être appelées qu'après avoir initialisé screen
import Graphismes as gr
from IA import *

##Variable d'action

done1 = False                    #done1 et done2 indique quand la fenêtre doit se fermer.
done2 = False

#Les prochaines variables indiquent si une direction est voulue par le joueur.
droite=False
gauche=False
haut=False
bas=False
rien=False

#atk indique si le joueur veut attaquer devant lui.
atk=False

#action indique si le joueur a bougé pendant ce tour
action=False



#Cette fonction est ici car je n'ai pas encore décidé où la garder.
#Elle sera certainement remplacée dans une version future du code.
def kill(x,y):
    dn.joueur["etat"]="attack"
    dn.joueur["horloge"]=0
    for e in dn.ennemis:
        if e[0][0]==x and e[0][1]==y:
            #L'animation se déroule sur 4 frames:
            #D'abord, le personnage initie l'attaque et la cible se tourne vers l'attaquant
            if dn.joueur["direction"]=="right":
                e["direction"]="left"
            elif dn.joueur["direction"]=="left":
                e["direction"]="right"
            elif dn.joueur["direction"]=="down":
                e["direction"]="up"
            elif dn.joueur["direction"]=="up":
                e["direction"]="down"
            gr.afficher_ecran(screen,vision)
            pygame.time.delay(150)
            
            #Puis l'attaquant lance l'attaque
            dn.joueur["horloge"]=1
            gr.afficher_ecran(screen,vision)
            pygame.time.delay(150)
            
            #Ensuite, l'attaquant touche la cible, qui réagit
            dn.joueur["horloge"]=2
            e["etat"]="dammage"
            e["horloge"]=0
            gr.afficher_ecran(screen,vision)
            pygame.time.delay(150)
            
            #Enfin, l'attaquant se remet en place et la cible tombe au sol
            dn.joueur["etat"]="still"
            e["horloge"]=1
            gr.afficher_ecran(screen,vision)
            pygame.time.delay(150)
            
            #La cible est ensuite détruite
            dn.grille[x,y]=dn.grille_vide[x,y]
            dn.ennemis.remove(e)
    dn.joueur["etat"]="still"

##Boucles
#Pour l'instant, la première boucle affiche l'écran-titre et la seconde fait tourner le jeu.
#Plus tard, les boucles seront contenues dans des fonctions indépendantes, et la fonction voulue sera appelée selon une variable d'état du jeu.


#Cette boucle sert à afficher l'écran titre. On en sort en appuyant sur espace
while not done1:
    gr.ecran_titre(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #Cliquer sur fermer (indispensable pour fermer la fenêtre).
            done1 = True
            done2 = True
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                done1 = True

init()              #init vient de IA.py, elle lance un nouvel étage.
                    #Sans cette fonction, fermer et ouvrir la fenêtre font reprendre le jeu au même point.
dn.etage=1

#Cette boucle fait tourner le jeu dans le labyrinthe
while not done2:
    #Màj automatique: si le joueur est sur un escalier, un nouvel étage est généré
    if dn.grille_vide[tuple(dn.joueur["position"])]==3:
        dn.etage+=1
        init()
    
    #Evènements: Cette boucle traite les entrées de clavier et de souris et les stocke.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #Cliquer sur fermer (indispensable pour fermer la fenêtre).
            done2 = True
            
        elif event.type==pygame.KEYDOWN:    #Presser une touche
            if event.key==pygame.K_d:       #d=droite
                droite=True
                dn.joueur["direction"]="right"
            if event.key==pygame.K_w:       #z=haut
                haut=True
                dn.joueur["direction"]="up"
            if event.key==pygame.K_a:       #q=gauche
                gauche=True
                dn.joueur["direction"]="left"
            if event.key==pygame.K_s:       #s=bas
                bas=True
                dn.joueur["direction"]="down"
            if event.key==pygame.K_KP1:     #1 du pavé numérique: passer
                rien=True
            if event.key==pygame.K_KP2:     #2 du pavé numérique: attaquer
                atk=True
        if event.type==pygame.KEYUP:        #Relacher une touche
            if event.key==pygame.K_d:
                droite=False
            if event.key==pygame.K_w:
                haut=False
            if event.key==pygame.K_a:
                gauche=False
            if event.key==pygame.K_s:
                bas=False
            if event.key==pygame.K_KP1:
                rien=False
            if event.key==pygame.K_KP2:
                atk=False
    #Actualiser le jeu
    
    #Si l'une des commandes est pressée et que l'action correspondante est possible, elle est effectuée.
    #Si la touche 1 du pavé numérique est enfoncée, le jeu considère qu'une action a été effectué même si rien n'a été fait.
    action=False
    if droite and dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]+1]] in [1,2,3]:
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]+1]]=4
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]]]= dn.grille_vide[dn.joueur["position"][0]][dn.joueur["position"][1]]
        dn.joueur["position"][1]+=1
        dn.joueur["etat"]="walk"
        action=True
        dn.joueur["direction"]="right"
    elif gauche and dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]-1]] in [1,2,3]:
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]-1]]=4
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]]]= dn.grille_vide[dn.joueur["position"][0]][dn.joueur["position"][1]]
        dn.joueur["position"][1]+=-1
        dn.joueur["etat"]="walk"
        action=True
        dn.joueur["direction"]="left"
    elif haut and dn.grille[dn.joueur["position"][0]-1,[dn.joueur["position"][1]]] in [1,2,3]:
        dn.grille[dn.joueur["position"][0]-1,[dn.joueur["position"][1]]]=4
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]]]= dn.grille_vide[dn.joueur["position"][0]][dn.joueur["position"][1]]
        dn.joueur["position"][0]+=-1
        dn.joueur["etat"]="walk"
        action=True
        dn.joueur["direction"]="up"
    elif bas and dn.grille[dn.joueur["position"][0]+1,[dn.joueur["position"][1]]] in [1,2,3]:
        dn.grille[dn.joueur["position"][0]+1,[dn.joueur["position"][1]]]=4
        dn.grille[dn.joueur["position"][0],[dn.joueur["position"][1]]]= dn.grille_vide[dn.joueur["position"][0]][dn.joueur["position"][1]]
        dn.joueur["position"][0]+=1
        dn.joueur["etat"]="walk"
        action=True
        dn.joueur["direction"]="down"
    elif atk:
        if (dn.joueur["direction"]=="right"):
            kill(dn.joueur["position"][0],dn.joueur["position"][1]+1)
        elif (dn.joueur["direction"]=="left"):
            kill(dn.joueur["position"][0],dn.joueur["position"][1]-1)
        elif (dn.joueur["direction"]=="up"):
            kill(dn.joueur["position"][0]-1,dn.joueur["position"][1])
        elif (dn.joueur["direction"]=="down"):
            kill(dn.joueur["position"][0]+1,dn.joueur["position"][1])
    
    elif rien:
        action=True
        dn.joueur["etat"]="still"
        dn.joueur["horloge"]=0
    else:
        dn.joueur["etat"]="still"
        dn.joueur["horloge"]=0
        
    
    #Si le joueur a agit, les ennemis agissent aussi
    if action:
        for ennemi in range(len(dn.ennemis)):
            suivre_instruction(ennemi,choix_action(ennemi))
            
    else:
        for e in dn.ennemis:
            e["etat"]="still"
            e["horloge"]=0
    
    #Actualiser la carte:
    #On vérifie si on est dans une salle
    salle=dn.grille_vide[dn.joueur["position"][0],dn.joueur["position"][1]] in [1,3]
    
    #On adapte le champs de vision selon si l'on est dans une salle ou non, et on actualise la vision
    if salle:       #Dans une salle, on voit la salle +1 case
        vision=[dn.joueur["position"][0]-1,dn.joueur["position"][0]+1,dn.joueur["position"][1]-1,dn.joueur["position"][1]+1]
        while dn.grille_vide[vision[0],dn.joueur["position"][1]] in [1,3]:
            vision[0]+=-1
        while dn.grille_vide[vision[1],dn.joueur["position"][1]] in [1,3]:
            vision[1]+=1
        while dn.grille_vide[dn.joueur["position"][0],vision[2]] in [1,3]:
            vision[2]+=-1
        while dn.grille_vide[dn.joueur["position"][0],vision[3]] in [1,3]:
            vision[3]+=1
            
        #On note comme vue chaque case du champs de vision et ses arrêtes(voir Donnees.py)
        for i in range(vision[0],vision[1]+1):
            for j in range(vision[2],vision[3]+1):
                dn.vus[1+2*i,1+2*j]=1
                dn.vus[1+2*i,2*j]=1
                dn.vus[1+2*i,2+2*j]=1
                dn.vus[2*i,1+2*j]=1
                dn.vus[2+2*i,1+2*j]=1
    
    else:           #Dans un couloir, on voit à un peu plus d'une case cases
    
        for i in range(6):
            for j in range(6):
                if not(i in [0,5] and j in [0,5]):
                    dn.vus[1+2*dn.joueur["position"][0]-5+i+j,1+2*dn.joueur["position"][1]+i-j]=1
        
        vision=[dn.joueur["position"][0]-2,dn.joueur["position"][0]+2,dn.joueur["position"][1]-2,dn.joueur["position"][1]+2]
    
    #Actualiser les graphismes
    dn.joueur["horloge"]=(dn.joueur["horloge"]+1)%3
    for e in dn.ennemis:
        e["horloge"]=(e["horloge"]+1)%3
    gr.afficher_ecran(screen,vision)

    # Attendre un peu pour reboucler (10 pour 1/10 seconde).
    pygame.time.delay(120)

#Pour fermer la fenêtre si l'on clique sur le bouton, très important.
pygame.display.quit()
pygame.quit()


