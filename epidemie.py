import numpy as np
import random

###############################################################################

PROB = 0.2
TAUX_INFECTION = 8
TEMPS_INFECTE = 7
TEMPS_REMISSION = 4
###############################################################################

def rand_prob_infecte(prob):
    #Définie un nombre aleatoire selon une loi de probabilité
    """Prob doit être donnée en frequence"""
    res = random.random()
    if res>prob:
        return 0
    return 2
        
###############################################################################


def ini_plateau(ligne,colonne):
    #Initialise un plateau de jeu de la taille indiquée
    plateau = np.zeros([ligne,colonne,2]).astype(int)
    for l in range(ligne):
        for c in range(colonne):
            plateau[l][c]=(rand_prob_infecte(PROB),0)
    return plateau

#print(ini_plateau(6,10))


###############################################################################

def matrice_voisins(l,c,plateau,):
    nbr_ligne=plateau.shape[0]
    nbr_colonne=plateau.shape[1]
    matrice=np.zeros([3,3,2], dtype=int)
    for x in range(3):
        for y in range(3):
            print("matri", matrice)
            matrice[x][y][0] = plateau[(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne][0]
        #   print(plateau[(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne][0])
         #  print(matrice[x][y])
    return matrice

plateau=ini_plateau(10,10)
print(plateau)
print(matrice_voisins(0,0,plateau))

#FONCTION A TERMINER







###############################################################################

"""
def evolution(plateau):
#    Initialisation d'une nouvelle grille
    new_plateau = np.zeros(plateau.shape).astype(int)
   
    
    
    
    
    
    
    
    
    
    
    
    
    
 # Coin superieur gauche
    if plateau[0][0][0] == 0:
        if plateau[0][1][0]+plateau[1][0][0]+plateau[1][1][0] >= TAUX_INFECTION:
               new_plateau[0][0][0] = 2
        else:
            new_plateau[0][0][0] = 0
    if plateau[0][0][0] == 2:
        if plateau[0][0][1] == TEMPS_INFECTE:
            new_plateau[0][0][0] = 1
            new_plateau[0][0][1] = 0
        else:
            new_plateau[0][0][0] = 2
            new_plateau[0][0][1] = plateau[0][0][1] +1
    if plateau[0][0][0] == 1:
        
    
    return voisins 


#print(evolution(np.zeros([5,5])))
"""