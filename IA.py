import numpy as np
import random as rd
import Donnees as dn
import Map_generator as mg

##IA
#Rq: pour désigner un PNJ (allié ou ennemi), j'utilise pion. Pour le joueur, j'utilise personnage ou joueur. Ennemi est à comprendre en contexte, selon le point de vue.


#Sur les 4 mouvements possibles, cette fonction indique lesquels doivent être tentés et selon quel degré de priorité
def prio_mouvement(ennemi):
    x,y=dn.ennemis[ennemi][0]
    x_prec,y_prec=dn.ennemis[ennemi][1]
    x_cible,y_cible=dn.ennemis[ennemi][2]
    
    #delta_x et delta_y indique la position relative de la cible par rapport au pion
    delta_x=x-x_cible
    delta_y=y-y_cible
    
    haut=(x-1,y)
    bas=(x+1,y)
    gauche=(x,y-1)
    droite=(x,y+1)
    
    #Rq: le pion ne sera jamais sur sa cible car, si elle est atteinte, elle est annulée
    #S'il n'y a pas de cible, le pion tente en priorité un mouvement qui ne le ramène pas en arrière
    if x_cible==0 and y_cible==0:
            mvt_possibles=[bas,droite,gauche,haut]
            if (x_prec, y_prec) in mvt_possibles:
                mvt_possibles.remove((x_prec,y_prec))
                return [mvt_possibles,[(x_prec,y_prec)]]
            else:
                return [mvt_possibles]
    
    #S'il y a une cible, le pion se dirige globalement vers elle
    if abs(delta_x)>abs(delta_y):           #Par exemple, si la cible est plus loin horizontalement que verticalement,
        if delta_x>0:                       #Qu'elle est à gauche
            if delta_y>0:                   #Et au-dessus,
                return [[haut],[gauche],[droite],[bas]]     #Alors la priorité est celle-ci
            elif delta_y<0:
                return [[haut],[droite],[gauche],[bas]]
            else:
                return [[haut],[droite,gauche],[bas]]       #Si deux actions sont équivalentes (en terme de distance à la cible), elles ont la même priorité
        elif delta_x<0:
            if delta_y>0:
                return [[bas],[gauche],[droite],[haut]]
            elif delta_y<0:
                return [[bas],[droite],[gauche],[haut]]
            else:
                return [[bas],[droite,gauche],[haut]]
    elif abs(delta_x)<abs(delta_y):
        if delta_y>0:
            if delta_x>0:
                return [[gauche],[haut],[bas],[droite]]
            elif delta_x<0:
                return [[gauche],[bas],[haut],[droite]]
            else:
                return [[gauche],[haut,bas],[droite]]
        elif delta_y<0:
            if delta_x>0:
                return [[droite],[haut],[bas],[gauche]]
            elif delta_x<0:
                return [[droite],[bas],[haut],[gauche]]
            else:
                return [[droite],[bas,haut],[gauche]]
    else:
        if delta_x>0 and delta_y>0:
            return [[gauche,haut],[bas,droite]]
        elif delta_x>0 and delta_y<0:
            return [[droite,haut],[bas,gauche]]
        elif delta_x<0 and delta_y>0:
            return [[gauche,bas],[haut,droite]]
        elif delta_x<0 and delta_y<0:
            return [[droite,bas],[haut,gauche]]
    

#Cette fonction détermine pour un ennemi donné l'action qu'il doit faire
def choix_action(ennemi):
    x,y=dn.ennemis[ennemi][0]
    x_prec,y_prec=dn.ennemis[ennemi][1]
    x_cible,y_cible=dn.ennemis[ennemi][2]
    
    #étape 1: le pion est-il dans une salle?
    salle=(dn.grille_vide[x,y] in [1,3])
    
    
    #étape 2, en salle: la salle + les murs sont vus
    if salle:
        x1,x2,y1,y2=x-1,x+1,y-1,y+1
        while dn.grille_vide[x1,y] in [1,3]:
            x1+=-1
        while dn.grille_vide[x2,y] in [1,3]:
            x2+=1
        while dn.grille_vide[x,y1] in [1,3]:
            y1+=-1
        while dn.grille_vide[x,y2] in [1,3]:
            y2+=1
    
    #étape 2, en couloir: tout est vu à 2 cases
    else:
        x1=x-2
        x2=x+2
        y1=y-2
        y2=y+2
    vision=dn.grille[x1:x2+1,y1:y2+1]
    
    
    #étape 3, en salle: si des ennemis est là, le pion se dirige vers l'ennemi le plus proche. Sinon, il va vers une sortie, si possible différente de celle dont il vient
    if salle:
        ennemis=[]
        sorties=[]
        #Le pion cherche des ennemis et les sorties de la salle dans son champs de vision
        for i in range(x2-x1+1):
            for j in range(y2-y1+1):
                if vision[i,j]==4:
                    ennemis.append((i+x1,j+y1))
                if (i==0 or j==0 or i==x2-x1 or j==y2-y1) and vision[i,j]:
                    sorties.append((i+x1,j+y1))
        
        #Si des ennemis est là (pour l'instant le personnage), il désigne le plus proche comme une cible.
        if ennemis:
            cible=0
            distance=abs(x-ennemis[0][0])+abs(y-ennemis[0][1])
            for i in range(len(ennemis)-1):
                if abs(x-ennemis[i][0])+abs(y-ennemis[i][1])<distance:
                    cible=i
                    distance=abs(x-ennemis[i][0])+abs(y-ennemis[i][1])
            x_cible=ennemis[cible][0]
            y_cible=ennemis[cible][1]
            if distance==1:
                return('r')
        
        #Sinon, si la cible n'est pas une sortie, on choisit une cible parmi les sorties (sauf celle dont le pion vient)
        else:
            if (x_cible,y_cible) not in sorties:
                if sorties==[(x_prec,y_prec)]:
                    x_cible,y_cible=x_prec,y_prec
                else:
                    if (x_prec,y_prec) in sorties:
                        sorties.remove((x_prec,y_prec))
                    x_cible,y_cible=rd.choice(sorties)
    
    #étape 3, en couloir: s'il y a un ennemi, le pion va vers lui. Sinon, il avance sans revenir en arrière
    else:
        
        ennemis=[]
        for i in range(5):
            for j in range(5):
                if vision[i,j]==4:
                    ennemis.append((i,j))
        
        if ennemis:
            cible=0
            distance=abs(2-ennemis[0][0])+abs(2-ennemis[0][1])
            for i in range(len(ennemis)-1):
                if abs(2-ennemis[i][0])+abs(2-ennemis[i][1])<distance:
                    cible=i
                    distance=abs(2-ennemis[i][0])+abs(2-ennemis[i][1])
            x_cible=x1+ennemis[cible][0]
            y_cible=y1+ennemis[cible][1]
            if distance==1:
                return ('r')
        else:
            x_cible=0
            y_cible=0
            
    #étape 4: on attribue la cible et on établit les mouvements prioritaires
    dn.ennemis[ennemi][2]=[x_cible,y_cible]
    priorite=prio_mouvement(ennemi)
    
    #étape 5: on choisit un mouvement et on renvoie l'instruction correspondante
    for liste in priorite:
        l=len(liste)
        i=0
        while i<l:  #on parcourt la liste en retirant les mouvements impossibles
            if dn.grille[liste[i]] in [1,2,3]:
                i+=1
            else:
                liste.remove(liste[i])
                l+=-1
        if liste!=[]:       #Puis on choisit un mouvement au hasard s'il en reste une possible
            x_suivant,y_suivant=rd.choice(liste)
            if (x_suivant,y_suivant)==(x+1,y):
                return('x+')
            elif (x_suivant,y_suivant)==(x-1,y):
                return('x-')
            elif (x_suivant,y_suivant)==(x,y+1):
                return('y+')
            elif (x_suivant,y_suivant)==(x,y-1):
                return('y-')
    return('r')         #Si aucune action n'est possible, le pion ne fait rien
        
                
#Cette fonction modifie les données selon l'action effectuée par l'ennemi
def suivre_instruction(ennemi,instruction):
    x,y=dn.ennemis[ennemi][0]
    x_prec,y_prec=dn.ennemis[ennemi][1]
    
    #Si l'instruction est un mouvement, on modifie la grille et les informations du pion
    if instruction[0]=='x':
        if instruction[1]=='+':
            dn.grille[x][y]=dn.grille_vide[x][y]
            dn.grille[x+1][y]=5
            x,x_prec=x+1,x
            y_prec=y
        else:
            dn.grille[x][y]=dn.grille_vide[x][y]
            dn.grille[x-1][y]=5
            x,x_prec=x-1,x
            y_prec=y
    elif instruction[0]=='y':
        if instruction[1]=='+':
            dn.grille[x][y]=dn.grille_vide[x][y]
            dn.grille[x][y+1]=5
            y,y_prec=y+1,y
            x_prec=x
        else:
            dn.grille[x][y]=dn.grille_vide[x][y]
            dn.grille[x][y-1]=5
            y,y_prec=y-1,y
            x_prec=x
    
    dn.ennemis[ennemi][0]=[x,y]
    dn.ennemis[ennemi][1]=[x_prec,y_prec]



##Données

#Cette fonction sert à initier Donnees.py. Voir ce fichier pour plus de détails.
def init():
    #grille_vide contient juste ce qui ne change pas durant l'exploration de l'étage
    dn.grille_vide,dn.grille=mg.creer_etage(dn.width_map,dn.height_map)
    
    #murs est une carte indiquant les murs, il sert à tracer la mini-map
    dn.murs=np.zeros((2*(dn.width_map+1),2*(dn.height_map+1)))
    for i in range(dn.width_map):
        for j in range(dn.height_map):
            if dn.grille[3+i,3+j]:
                if not dn.grille[2+i,3+j]:
                    dn.murs[2*i][1+2*j]=1
                if not dn.grille[4+i,3+j]:
                    dn.murs[2+2*i][1+2*j]=1
                if not dn.grille[3+i,2+j]:
                    dn.murs[1+2*i][2*j]=1
                if not dn.grille[3+i,4+j]:
                    dn.murs[1+2*i][2+2*j]=1
                    
    #vus est une carte des zones entrées au moins une fois dans le champs de vision. Il sert à savoir quelle partie de la mini-map révéler
    dn.vus=np.zeros((2*(dn.width_map+1+3),2*(dn.height_map+1+3)))
