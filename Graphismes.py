import pygame
import pygame.draw as dr
import Donnees as dn
from Font import font, tracer_message

##Afficher l'écran

def afficher_ecran(screen,vision):
    x=dn.joueur[0]
    y=dn.joueur[1]
    #On dessine d'abord le fond d'écran.
    draw_background(screen,vision)
    
    #On met ensuite le personnage au centre, et les ennemis à l'écran autour.
    draw_charac(screen, vision, "joueur", 0.5*dn.taille_ecran, 0.5*dn.taille_ecran)
    for e in dn.ennemis:
        draw_charac(screen, vision, "ennemi", e[0][0]-(x-3)+0.5, e[0][1]-(y-3)+0.5)
        #-(x/y-3) pour avoir la postion par rapport au bord de l'écran
        #+0.5 pour être sur le centre d'une case, et non sur un coin
        #la virgule n'est pas génante car draw_charac convertie en entier après le calcul
    
    #On dessine la carte.
    draw_map(screen,vision)
    
    #On dessine le reste de l'UI.
    draw_UI(screen)

    #Enfin, on affiche l'écran actualisé.
    pygame.display.flip()
    


def draw_background(screen,vision):
    #Cette fonction parcours grille_vide autour de la position du joueur, et dessine la case appropriée.
    x=dn.joueur[0]
    y=dn.joueur[1]
    for i in range(dn.taille_ecran):
        for j in range(dn.taille_ecran):
            if dn.grille_vide[x-3+i,y-3+j]==3:
                dr.rect(screen, dn.L_BLUE, [j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])
            elif dn.grille_vide[x-3+i,y-3+j]==0:
                dr.rect(screen, dn.palette[0],[j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])
            else:
                dr.rect(screen, dn.palette[1],[j*dn.taille_case, i*dn.taille_case, dn.taille_case,dn.taille_case])


def draw_charac(screen, vision, charac, x, y):
    dr.circle(screen, dn.sprites[charac], [int(y*dn.taille_case), int(x*dn.taille_case)], int(0.5*dn.taille_case))


def draw_map(screen, vision):
    x=dn.joueur[0]
    y=dn.joueur[1]
    for i in range(dn.width_map+1):
        for j in range(dn.height_map+1):
            #Pour chaque case, on vérifie s'il y a un escalier. S'il y en a un, on le marque d'un carré bleu ciel
            if dn.grille_vide[3+i,3+j]==3 and dn.vus[1+2*(3+i),1+2*(3+j)]:
                dr.line(screen,dn.L_BLUE,(25+1+j*5,25+1+i*5),(30-1+j*5,25+1+i*5))
                dr.line(screen,dn.L_BLUE,(25+1+j*5,30-1+i*5),(30-1+j*5,30-1+i*5))
                dr.line(screen,dn.L_BLUE,(25+1+j*5,25+1+i*5),(25+1+j*5,30-1+i*5))
                dr.line(screen,dn.L_BLUE,(30-1+j*5,25+1+i*5),(30-1+j*5,30-1+i*5))
            #Ensuite, on trace en blanc les murs, verticaux ou horizontaux selon leurs coordonnées.
            if dn.vus[2*(3+i),1+2*(3+j)] and dn.murs[2*i,1+2*j]:
                dr.line(screen,dn.WHITE,(25+j*5,25+i*5),(30+j*5,25+i*5))
            if dn.vus[1+2*(3+i),2*(3+j)] and dn.murs[1+2*i,2*j]:
                dr.line(screen,dn.WHITE,(25+j*5,25+i*5),(25+j*5,30+i*5))
    #On place le personnage sur la carte, et les ennemis en vue.
    dr.circle(screen, dn.YELLOW, [int(25+(y-3+0.5)*5)+1, int(25+(x-3+0.5)*5)+1],2)
    for e in dn.ennemis:
        if e[0][0]<=vision[1] and e[0][0]>=vision[0] and e[0][1]<=vision[3] and e[0][1]>=vision[2]:
            dr.circle(screen, dn.RED, [int(25+(e[0][1]-3+0.5)*5)+1, int(25+(e[0][0]-3+0.5)*5)+1],2)

def draw_UI(screen):
    tracer_message(screen,'E.'+str(dn.etage),2,dn.taille_ecran*dn.taille_case-35)
