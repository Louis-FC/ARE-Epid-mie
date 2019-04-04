import numpy as np
import random
import matplotlib.pyplot as plt
import time
#import imageio
###############################################################################
couleurs_etat=['green','blue','red'] #Couleurs disponibles à la modélisation
couleurs_comportement=['green','green','orange','orange','yellow','red']
NB_LIGNES=50 #Nombre de lignes du tableau
NB_COLONNES=50 #Nombre de colonnes du tableau
t0 = time.time() # Temps initial du programme

PROB_INFECTE = 0.1 #Probabilité d'être infecté au premier tour
PROB_REMISSION = 0.05 #Probabilité d'être en rémission au premier tour
PROB_COMPORTEMENT_2 = 1 #Probabilité d'avoir le comportement 2
PROB_COMPORTEMENT_4 = 0 #Probabilité d'avoir le comportement 4
PROB_COMPORTEMENT_5 = 0 #Probabilité d'avoir le comportement 5
PROB_INFECTE_INCREMENTATION = [0.75,0.9,0.5,0.65,0.75,0.5] #Probabilité d'incrémenter son compteur pour passer d'infécté à personne en rémission selon le comportement
PROB_REMISSION_INCREMENTATION = [0.75,0.9,0.5,0.65,0.75,0.5] #Probabilité d'incrémenter son compteur pour passer de personne en rémission à personne saine selon le comportement
TAUX_INFECTION = [6,8,4,5,6,4] #Valeur minimum d'infection autour du sujet pour infecter celui-ci selon son comportement
TAUX_REINFECTION = [4,5,3,4,4,3] #Nombre d'infectés minimums necéssaires à la réinfection du sujet si celui-ci est en rémission selon son comportement
TEMPS_INFECTE = [3,2,5,4,3,5] #Nombre de tours nécessiares à une infecté pour passer en rémission selon son comportement
TEMPS_REMISSION = [3,2,5,4,3,5] #Nombre de tours nécessiares à une personne en rémission pour redevenir saine selon son comportement
TEMPS_IMMUNISE = 3 #Nombre de tours d'immunité à la fin d'une infection
NB_REINFECTION=2 #Nombre de réinfections possible avant l'immunité du sujet
###############################################################################

def rand_prob_infecte(prob1, prob2):
    #Définie un nombre aleatoire selon une loi de probabilité
    """Prob doit être donnée en frequence"""
    res = random.random()
    if res>prob1+prob2:
        return 0
    if res>prob2:
        return 1
    return 2
        
###############################################################################

def rand_prob_comportement(prob1, prob2, prob3):
    res = random.random()
    if res>prob1+prob2+prob3:
        return 0
    if res>prob2+prob3:
        return 2
    if res>prob3:
        return 4
    return 5

###############################################################################


def ini_plateau(ligne,colonne):
    #Initialise un plateau de jeu de la taille indiquée
    plateau = np.zeros([4,ligne,colonne]).astype(int)
    for l in range(ligne):
        for c in range(colonne):
            plateau[0][l][c]=rand_prob_infecte(PROB_REMISSION, PROB_INFECTE)
            plateau[3][l][c]=rand_prob_comportement(PROB_COMPORTEMENT_2,PROB_COMPORTEMENT_4,PROB_COMPORTEMENT_5)
    return plateau



###############################################################################

def incrementation_alea(prob):
    res = random.random()
    if res>prob:
        return 0
    return 1


###############################################################################

def matrice_voisins(l,c,plateau,):
    """Extrait la matrice 3x3 autour de la coordonée choisie, 
    puis applique à la cellule centrale les règles d'évolution,
    et retourne la liste contenant son état et son compteur après l'évolution"""
    
    
    #EXTRACTION
        #Création d'un plateau 3x3
    nbr_ligne=plateau.shape[1]
    nbr_colonne=plateau.shape[2]
    matrice=np.zeros([4,3,3], dtype=int)
    
        #Remplissage du nouveau plateau
    for x in range(3):
        for y in range(3):
            matrice[0][x][y] = plateau[0][(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne]
            matrice[3][x][y] = plateau[3][(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne]
    matrice[1][1][1] = plateau[1][l][c]
    matrice[2][1][1] = plateau[2][l][c]
    
    #ANALYSE DU TABLEAU
#On initialise la somme à l'opposé de la valeur de la cellule centrale
#pour que cette valeur s'annule lorsqu'on parcourt le tableau
    somme=-matrice[0][1][1]
    nb_infectes=0
    for x in range(3):
        for y in range(3):
            somme+=matrice[0][x][y]
            if matrice[0][x][y]==2:
                nb_infectes+=1
    
    #EVOLUTION
        #Personne saine
    if matrice[0][1][1]==0:
        if matrice[1][1][1]==0:
            if somme>=TAUX_INFECTION[matrice[3][1][1]]:
                matrice[0][1][1]=2
        else:
            matrice[1][1][1]-=1
    
        #Personne infectée
    else:
        if matrice[0][1][1]==2:
            if matrice[1][1][1]==TEMPS_INFECTE[matrice[3][1][1]]:
                matrice[0][1][1]=1
                matrice[1][1][1]=0
            else:
                matrice[1][1][1]+=incrementation_alea(PROB_INFECTE_INCREMENTATION[matrice[3][1][1]])
        
        #Personne en rémission
        else:
            if matrice[0][1][1]==1:
                if matrice[1][1][1]==TEMPS_REMISSION[matrice[3][1][1]]:
                    matrice[0][1][1]=0
                    matrice[1][1][1]=TEMPS_IMMUNISE
                    matrice[2][1][1]=0
                else:
                    if matrice[2][1][1]<NB_REINFECTION:
                        if nb_infectes>=TAUX_REINFECTION[matrice[3][1][1]]:
                            matrice[0][1][1]=2
                            matrice[1][1][1]=0
                            matrice[2][1][1]+=1
                        else:
                            matrice[1][1][1]+=incrementation_alea(PROB_REMISSION_INCREMENTATION[matrice[3][1][1]])
                    else:
                        matrice[1][1][1]+=incrementation_alea(PROB_REMISSION_INCREMENTATION[matrice[3][1][1]])
                        
    #Retour de la liste résultat
    etat=matrice[0][1][1]
    timer=matrice[1][1][1]
    reinfection=matrice[2][1][1]
    comportement=matrice[3][1][1]
    return [etat,timer,reinfection,comportement]



###############################################################################


def evolution(plateau):
#    Génère la grille à l'étape suivante
    new_plateau = np.zeros(plateau.shape).astype(int)
    ligne=new_plateau.shape[1]
    colonne=new_plateau.shape[2]
    for l in range(ligne):
        for c in range(colonne):
            voisins=matrice_voisins(l,c,plateau)
            new_plateau[0][l][c]=voisins[0]
            new_plateau[1][l][c]=voisins[1]
            new_plateau[2][l][c]=voisins[2]
    return new_plateau 


###############################################################################

def sauvegarder_image_etat(plateau,etape):
    """Affiche sur un graphique en 2D les points d'un plateau pssé en argument"""
    # Récupère la taille du plateau pour pouvoir le parcourir
    ligne=plateau.shape[1]
    colonne=plateau.shape[2]
    for l in range(ligne):
        for c in range(colonne):
            """ Affiche le point de coordonnée l,c de la couleur qui lui est associé""" 
            plt.scatter(c,-l,c=couleurs_etat[plateau[0][l][c]])
            """ Notez l'inversion du l et du c dans les coordonnées ainsi que
            l'apparition d'un signe - devant le l afin de respecter la configuration
            d'affichage des array numpy"""
    #nom_image=("Imagerie//etape_{}.png".format(etape))
    #plt.savefig(nom_image)
    plt.show()
    #return nom_image

###############################################################################

def sauvegarder_image_comportement(plateau):
    ligne=plateau.shape[1]
    colonne=plateau.shape[2]
    for l in range(ligne):
        for c in range(colonne):
            """ Affiche le point de coordonnée l,c de la couleur qui lui est associé""" 
            plt.scatter(c,-l,c=couleurs_comportement[plateau[3][l][c]])
            """ Notez l'inversion du l et du c dans les coordonnées ainsi que
            l'apparition d'un signe - devant le l afin de respecter la configuration
            d'affichage des array numpy"""
    nom_image=("Imagerie//comportement.png")
    plt.savefig(nom_image)
    plt.show()

###############################################################################
def creation_gif(plateau, nbr_etapes):
    images=[]
    for i in range(nbr_etapes):
        plateau=evolution(plateau)
        image=sauvegarder_image_etat(plateau,i) 
        images.append(imageio.imread(image))
    imageio.mimsave('Imagerie/animation.gif',images, duration=1)

###############################################################################

plateau=ini_plateau(NB_LIGNES,NB_COLONNES)
print(plateau)

sauvegarder_image_comportement(plateau)

for i in range(25):
    sauvegarder_image_etat(plateau,i)
    plateau=evolution(plateau)



tf = time.time() #Temps final
print(tf - t0) #Affiche la durée d'execution du programme

#%%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def gen_img():
    """
    """
    
    img_np = np.random.randint(0,255, 100).reshape(10,10)
    img = plt.imshow(img_np)
    
    return img

fig = plt.figure()

ims = []
for i in range(10):
    img = gen_img()
    ims.append([img])
    
anim = animation.ArtistAnimation(fig, ims)
    
    
#%%











"""
Liste des choses à faire :
    - Créer des clusters de comportements
"""
































