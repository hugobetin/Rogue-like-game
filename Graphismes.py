import pygame
import pygame.draw as dr
import Donnees as dn
from Font import font, tracer_message
import Sprites as sp

##Afficher l'écran titre

def ecran_titre(screen):
    screen.blit(sp.ecran_titre,[0,0])
    pygame.display.update()

##Afficher l'écran de jeu

def afficher_ecran(screen,vision):
    x=dn.joueur["position"][0]
    y=dn.joueur["position"][1]
    #On dessine d'abord le fond d'écran.
    draw_background(screen,vision)
    
    #On met ensuite le personnage au centre, et les ennemis à l'écran autour.
    draw_charac(screen, dn.joueur, 3, 3)
    for e in dn.ennemis:
        draw_charac(screen, e, e[0][0]-(x-3), e[0][1]-(y-3))
        #-(x/y-3) pour avoir la postion par rapport au bord de l'écran
        #+0.5 pour être sur le centre d'une case, et non sur un coin
        #la virgule n'est pas génante car draw_charac convertie en entier après le calcul
    
    #On dessine la carte.
    draw_map(screen,vision)
    
    #On dessine le reste de l'UI.
    draw_UI(screen)

    #Enfin, on affiche l'écran actualisé.
    pygame.display.update()
    


def draw_background(screen,vision):
    #Cette fonction parcours grille_vide autour de la position du joueur, et dessine la case appropriée.
    x=dn.joueur["position"][0]
    y=dn.joueur["position"][1]
    for i in range(dn.taille_ecran):
        for j in range(dn.taille_ecran):
            if dn.grille_vide[x-3+i,y-3+j]==3:
                dr.rect(screen, dn.L_BLUE, [j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])
            elif dn.grille_vide[x-3+i,y-3+j]==0:
                dr.rect(screen, dn.palette[0],[j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])
            else:
                dr.rect(screen, dn.palette[1],[j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])




def draw_charac(screen, charac, x, y):
    if charac["etat"]=="dammage":
        screen.blit(sp.im_charac[charac["type"]+" "+charac["direction"]+ " d "+str(charac["horloge"])],[int((y-0.5)*dn.taille_case), int((x-0.5)*dn.taille_case)])
    elif charac["etat"]=="attack":
        screen.blit(sp.im_charac[charac["type"]+" "+charac["direction"]+ " a "+str(charac["horloge"])],[int((y-0.5)*dn.taille_case), int((x-0.5)*dn.taille_case)])
    elif charac["etat"]=="still":
        screen.blit(sp.im_charac[charac["type"]+" "+charac["direction"]+ " 1"],[int((y-0.5)*dn.taille_case), int((x-0.5)*dn.taille_case)])
    elif charac["etat"]=="walk":
        n=charac["horloge"]
        screen.blit(sp.im_charac[charac["type"]+" "+charac["direction"]+ " " +str(n)],[int((y-0.5)*dn.taille_case), int((x-0.5)*dn.taille_case)])


def draw_map(screen, vision):
    x=dn.joueur["position"][0]
    y=dn.joueur["position"][1]
    for i in range(dn.width_map+1):
        for j in range(dn.height_map+1):
            #Pour chaque case, on vérifie s'il y a un escalier. S'il y en a un, on le marque d'un carré bleu ciel
            if dn.grille_vide[3+i,3+j]==3 and dn.vus[1+2*(3+i),1+2*(3+j)]:
                dr.line(screen,dn.L_BLUE,(25+1+j*7,25+1+i*7),(32-1+j*7,25+1+i*7))
                dr.line(screen,dn.L_BLUE,(25+1+j*7,32-1+i*7),(32-1+j*7,32-1+i*7))
                dr.line(screen,dn.L_BLUE,(25+1+j*7,25+1+i*7),(25+1+j*7,32-1+i*7))
                dr.line(screen,dn.L_BLUE,(32-1+j*7,25+1+i*7),(32-1+j*7,32-1+i*7))
            #Ensuite, on trace en blanc les murs, verticaux ou horizontaux selon leurs coordonnées.
            if dn.vus[2*(3+i),1+2*(3+j)] and dn.murs[2*i,1+2*j]:
                dr.line(screen,dn.WHITE,(25+j*7,25+i*7),(32+j*7,25+i*7))
            if dn.vus[1+2*(3+i),2*(3+j)] and dn.murs[1+2*i,2*j]:
                dr.line(screen,dn.WHITE,(25+j*7,25+i*7),(25+j*7,32+i*7))
    #On place le personnage sur la carte, et les ennemis en vue.
    dr.circle(screen, dn.YELLOW, [int(25+(y-3+0.5)*7)+1, int(25+(x-3+0.5)*7)+1],3)
    for e in dn.ennemis:
        if e[0][0]<=vision[1] and e[0][0]>=vision[0] and e[0][1]<=vision[3] and e[0][1]>=vision[2]:
            dr.circle(screen, dn.RED, [int(25+(e[0][1]-3+0.5)*7)+1, int(25+(e[0][0]-3+0.5)*7)+1],3)

def draw_UI(screen):
    tracer_message(screen,'E.'+str(dn.etage),0.5,2,2)
