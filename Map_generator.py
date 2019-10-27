import numpy as np
import random as rd

#Utilisation de BSP: on scinde recursivement la map en feuilles jusqu'à une certaine taille et on remplit chaque feuille

#Ces variables sont là pour tester le programme
width_map=20
height_map=20

##Définition de classe
class Leaf:
    def __init__(self,X,Y,width,height):
        self.x,self.y=X,Y        #Position de la feuille (coin sup gauche)
        self.width=width         #Largeur de la feuille
        self.height=height       #Longueur de la feuille
        self.left_child=None      #L'enfant gauche de la feuille (s'il y en a un), aussi une feuille
        self.right_child=None     #L'enfant droit de la feuille (s'il y en a un), aussi une feuille
        self.room=None           #La salle de la feuille (s'il y en a une), au format [x,y,width,height]
        self.min_feuille=6               #Taille min d'une feuille, emplacement min pour une coupure
    
    #Comment générer des sous-feuilles
    def split(self):
        #On décide dans quel sens séparer la feuille
        #Si une direction est dominante, on la réduit. Sinon, on choisit au hasard
        split_hori=rd.choice([True,False])
        if self.width/self.height>=1.25:
            split_hori=False
        if self.height/self.width>=1.25:
            split_hori=True
        
        #On vérifie qu'on peut créer deux feuilles pas trop petites
        if split_hori:
            max_feuille=self.height-self.min_feuille
        else:
            max_feuille=self.width-self.min_feuille
        #max_feuille: emplacement max pour une coupure. Doit être supérieur à min_feuille pour pouvoir couper.
        if max_feuille<=self.min_feuille:
            return(False)
        
        split=rd.randint(self.min_feuille,max_feuille)   #Où est la coupe?
        #Créer les enfants
        if split_hori:
            self.left_child=Leaf(self.x,self.y,self.width,split)
            self.right_child=Leaf(self.x,self.y+split,self.width,self.height-split)
        else:
            self.left_child=Leaf(self.x,self.y,split,self.height)
            self.right_child=Leaf(self.x+split,self.y,self.width-split,self.height)
        return (True)
    
    def choisir_salle(self):            #Cette fonction renvoie toutes les salles de la feuille dans un ordre aléatoire
        if self.left_child==None:
            return([self.room])
        else:
            rooms=self.left_child.choisir_salle()+self.right_child.choisir_salle()
            rd.shuffle(rooms)
            return(rooms)

##Découpage des feuilles
#Cette partie génère un découpage d'une carte en feuilles


def creer_feuilles(width_map,height_map):
    root=Leaf(0,0,width_map,height_map)     #Root est la feuille original, c'est-à-dire toute la carte
    feuilles=[root]
    split=True
    while split:        #On reste dans la boucle tant que l'on réussit à découper
        split=False
        feuilles2=[]
        for leaf in feuilles:       #Pour chaque feuille à traiter:
            if leaf!=None :         #Si elle est non vide,
                if leaf.split():    #Et si on arrive à la découper,
                    feuilles2=feuilles2+[leaf.left_child,leaf.right_child]       #Alors les enfants doivent être traités
                    split=True      #Et on a réussit une séparation
                else:                       #Si on ne peut pas la découper, on la garde quand même pour avoir la liste complète des feuilles élémentaires. La séparation n'est pas validée
                    feuilles2+=[leaf]
        feuilles=feuilles2          #On actualise la liste des feuilles à traiter
    return(root,feuilles)

"""
root,feuilles=creer_feuilles(width_map,height_map)
"""
##Visualisation des feuilles
#Cette partie sert à visualiser les feuilles précédement découpées. Elle ne sert pas au jeu, mais à vérifier la pertinence des feuilles générées

def voir_feuilles(root,feuilles):
    carte=np.zeros((root.width,root.height))
    for leaf in feuilles:
        for i in range(leaf.width):
            carte[leaf.x+i,leaf.y]=1
            carte[leaf.x+i,leaf.y+leaf.height-1]=1
        for i in range(leaf.height):
            carte[leaf.x,leaf.y+i]=1
            carte[leaf.x+leaf.width-1,leaf.y+i]=1
    print(carte)

"""
voir_feuilles(width_map,height_map,feuilles)
"""
##Création des salles
#Cette partie va créer une carte et y générer des salles aléatoires (une dans chaque feuille)

def creer_salles(root,feuilles):
    carte=np.zeros((root.width,root.height))
    taille_min=4                    #Cette constante indique les dimensions minimum qu'une salle peut avoir
    
    #D'abord, il faut créer les salles
    for leaf in feuilles:           #Pour chaque feuille:
        #Je veux qu'une salle rentre strictement dans une feuille, donc les dimmensions de la salle doivent être inférieures à celles de la feuille -2
        width=rd.randint(taille_min,leaf.width-2)
        height=rd.randint(taille_min,leaf.height-2)
        
        #De même pour les coordonnées, on doit avoir x>leaf.x et x+width< leaf.x+leaf.width (de même pour y et height)
        x=rd.randint(leaf.x+1,leaf.x+leaf.width-width-1)
        y=rd.randint(leaf.y+1,leaf.y+leaf.height-height-1)
        
        #Ensuite, on note la salle dans la feuille et on trace la salle sur la carte
        leaf.room=[x,y,width,height]
        for i in range(x,x+width):
            for j in range(y,y+height):
                carte[i,j]=1
    
    return(carte)

"""
carte=creer_salles(root,feuilles)
"""
##Création des couloirs
#Cette fonction va prendre la carte et l'arbre entier pour pouvoir créer des couloirs entre les enfants

def creer_couloirs(leaf,carte):
    #Cette fonction est récursive: pour une feuille, on traite chaque enfant (s'il y en a), puis on les relie. S'il n'y a pas d'enfants, on ne fait rien
    if leaf.left_child!=None:
        #D'abord, on crée les couloirs internes à chaque enfant
        creer_couloirs(leaf.left_child,carte)
        creer_couloirs(leaf.right_child,carte)
        
        #Ensuite, on prend une salle dans chaque enfant
        room1=(leaf.left_child.choisir_salle())[0]
        room2=(leaf.right_child.choisir_salle())[0]
        #On désigne un point aléatoire dans chaque salle
        x1=rd.randint(room1[0],room1[0]+room1[2]-1)
        y1=rd.randint(room1[1],room1[1]+room1[3]-1)
        x2=rd.randint(room2[0],room2[0]+room2[2]-1)
        y2=rd.randint(room2[1],room2[1]+room2[3]-1)
        #Et on relie les 2 points par une droite ou un L selon l'alignement
        if x1==x2:
            for i in range(min(y1,y2),max(y1,y2)):
                if carte[x1,i]==0:
                    carte[x1,i]=2
        elif y1==y2:
            for i in range(min(x1,x2),max(x1,x2)):
                if carte[i,y1]==0:
                    carte[i,y1]=2
        else:
            xa,xb,ya,yb=rd.choice([(x1,x2,y2,y1),(x2,x1,y1,y2)])     #On choisit la forme du L au hasard
            
            for i in range(min(xa,xb),max(xa,xb)+1):
                if carte[i,ya]==0:
                    carte[i,ya]=2
            for i in range(min(ya,yb),max(ya,yb)+1):
                if carte[xa,i]==0:
                    carte[xa,i]=2

"""
creer_couloirs(root,carte)
"""
##Placer un escalier
#Un étage ne doit contenir qu'un unique escalier vers l'étage suivant. La sortie se fait par mort, abandon ou atteinte du dernier étage (aucun n'est encore implémenté)

def placer_escalier(root,carte):
    salle=(root.choisir_salle())[0]
    x=rd.randint(salle[0]+1,salle[0]+salle[2]-2)
    y=rd.randint(salle[1]+1,salle[1]+salle[3]-2)
    carte[x,y]=3

"""
placer_escalier(root,carte)
"""


##Creer un etage
#Cette partie intègre toutes les parties précédentes en une fonction
#Pour l'instant, ses seuls paramètres sont les dimmensions de l'étage

def creer_etage(width_map, height_map):
    root,feuilles=creer_feuilles(width_map,height_map)
    carte_vide=creer_salles(root,feuilles)
    creer_couloirs(root,carte_vide)
    placer_escalier(root,carte_vide)
    #On ajoute les bandes de 0 pour l'affichage
    carte_vide=np.concatenate((np.zeros((height_map,2)),carte_vide,np.zeros((height_map,2))),axis=1)
    carte_vide=np.concatenate((np.zeros((2,width_map+4)),carte_vide,np.zeros((2,width_map+4))),axis=0)
    return(carte_vide)

"""
carte=creer_etage(width_map,height_map)
print(carte)
"""



