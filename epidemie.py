import numpy as np
import random

###############################################################################

PROB = 0.2
TAUX_INFECTION = 8
TAUX_REINFECTION = 4
TEMPS_INFECTE = 4
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
    plateau = np.zeros([2,ligne,colonne]).astype(int)
    for l in range(ligne):
        for c in range(colonne):
            plateau[0][l][c]=rand_prob_infecte(PROB)
    return plateau

#print(ini_plateau(6,10))


###############################################################################

def matrice_voisins(l,c,plateau,):
    """Extrait la matrice 3x3 autour de la coordonée choisie, 
    puis applique à la cellule centrale les règles d'évolution,
    et retourne la liste contenant son état et son compteur après l'évolution"""
    
    
    #EXTRACTION
        #Création d'un plateau 3x3
    nbr_ligne=plateau.shape[1]
    nbr_colonne=plateau.shape[2]
    matrice=np.zeros([2,3,3], dtype=int)
    
        #Remplissage du nouveau plateau
    for x in range(3):
        for y in range(3):
            matrice[0][x][y] = plateau[0][(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne]
            matrice[1][x][y] = plateau[1][(l+x-1)%nbr_ligne][(c+y-1)%nbr_colonne]
    
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
        if somme>=TAUX_INFECTION:
            matrice[0][1][1]=2        
    
        #Personne infectée
    else:
        if matrice[0][1][1]==2:
            if matrice[1][1][1]==TEMPS_INFECTE:
                matrice[0][1][1]=1
                matrice[1][1][1]=0
            else:
                matrice[1][1][1]+=1
        
        #Personne en rémission
        else:
            if matrice[0][1][1]==1:
                if nb_infectes>=TAUX_REINFECTION:
                    matrice[0][1][1]=2
                    matrice[1][1][1]=0
                else:
                    if matrice[1][1][1]==TEMPS_REMISSION:
                        matrice[0][1][1]=0
                        matrice[1][1][1]=0
                    else:
                        matrice[1][1][1]+=1
                        
                        
    #Retour de la liste résultat
    etat=matrice[0][1][1]
    compteur=matrice[1][1][1]
    return [etat,compteur]

#plateau=ini_plateau(5,10)
#print(plateau)
#print(matrice_voisins(2,2,plateau))
    


###############################################################################


def evolution(plateau):
#    Génère la grille à l'étape suivante
    new_plateau = np.zeros(plateau.shape).astype(int)
    ligne=new_plateau.shape[1]
    colonne=new_plateau.shape[2]
    for l in range(ligne):
        for c in range(colonne):
            new_plateau[0][l][c]=matrice_voisins(l,c,plateau)[0]
            new_plateau[1][l][c]=matrice_voisins(l,c,plateau)[1]    
    return new_plateau 

#plateau=ini_plateau(25,25)
#print(plateau)
#print(evolution(plateau))


###############################################################################






































