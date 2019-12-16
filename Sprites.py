import pygame
import pygame.draw as dr

import Donnees as dn




ecran_titre=pygame.image.load(dn.dossier + "Images\\Ecran titre.png").convert()

personnages=pygame.image.load(dn.dossier + "Images\\Personnages.png").convert()
types_images=["0","1","2", "a 0", "a 1", "a 2", "d 0", "d 1"]    #multiple for animation, a for attack, d for dammage

im_charac={}

j_bas=pygame.Surface((dn.taille_case,dn.taille_case))
j_bas.set_colorkey(dn.BACK)
dr.circle(j_bas,dn.YELLOW,(int(0.5*dn.taille_case),int(0.5*dn.taille_case)),int(0.5*dn.taille_case))
dr.rect(j_bas, dn.BLACK,((0.5-0.05-0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
dr.rect(j_bas, dn.BLACK,((0.5-0.05+0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
im_charac["0 down 0"]=j_bas

im_charac["0 left 0"]=pygame.transform.rotate(j_bas,270)
im_charac["0 up 0"]=pygame.transform.rotate(j_bas,180)
im_charac["0 right 0"]=pygame.transform.rotate(j_bas,90)



e_bas=pygame.Surface((dn.taille_case,dn.taille_case))
e_bas.set_colorkey(dn.BACK)
dr.circle(e_bas,dn.RED,(int(0.5*dn.taille_case),int(0.5*dn.taille_case)),int(0.5*dn.taille_case))
dr.rect(e_bas, dn.BLACK,((0.5-0.05-0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
dr.rect(e_bas, dn.BLACK,((0.5-0.05+0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
im_charac["1 down 0"]=e_bas

im_charac["1 left 0"]=pygame.transform.rotate(e_bas,270)
im_charac["1 up 0"]=pygame.transform.rotate(e_bas,180)
im_charac["1 right 0"]=pygame.transform.rotate(e_bas,90)

e_bas2=pygame.Surface((dn.taille_case,dn.taille_case))
e_bas2.set_colorkey(dn.BACK)
dr.circle(e_bas2,dn.ORANGE,(int(0.5*dn.taille_case),int(0.5*dn.taille_case)),int(0.5*dn.taille_case))
dr.rect(e_bas2, dn.BLACK,((0.5-0.05-0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
dr.rect(e_bas2, dn.BLACK,((0.5-0.05+0.1)*dn.taille_case, (0.5+0.3)*dn.taille_case,0.1*dn.taille_case,0.1*dn.taille_case))
im_charac["1 down d 0"]=e_bas2

im_charac["1 left d 0"]=pygame.transform.rotate(e_bas2,270)
im_charac["1 up d 0"]=pygame.transform.rotate(e_bas2,180)
im_charac["1 right d 0"]=pygame.transform.rotate(e_bas2,90)




def extraire_charac(source, charac, x, y):
    #Je n'ai pas pu raccourcir cette ligne en l=[[pygame.Surface((150,150))]*8]*3
    #car cela entrainait des bugs d'addresse
    l=[[pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150))],[pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150))],[pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150)),pygame.Surface((150,150))]]
    for d in range(3):
        for i in range(8):
            s=pygame.Surface((150,150))
            l[d][i].blit(personnages, [-(x+1 +d*(dn.taille_case*2+1)),(y-1 -i*(dn.taille_case*2+1))])
            l[d][i].set_colorkey(dn.WHITE)
            if d==0 :
                im_charac[charac + " down " + types_images[i]]=l[d][i]
            elif d==1:
                im_charac[charac + " up " + types_images[i]]=l[d][i]
            else:
                im_charac[charac + " left " + types_images[i]]=l[d][i]
                im_charac[charac + " right " + types_images[i]]=pygame.transform.flip(l[d][i],True, False)

extraire_charac(personnages, "loup", 0,0)
extraire_charac(personnages, "gobelin", 453,0)






