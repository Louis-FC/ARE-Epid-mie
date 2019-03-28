import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
###############################################################################
t0 = time.time() # Temps initial du programme
PROB = 0.2 #Probabilité d'être infecté au premier tour
TAUX_INFECTION = 8 #Valeur minimum d'infection autour du sujet pour infecter celui-ci
TAUX_REINFECTION = 4 #Nombre d'infectés minimums necéssaires à la réinfection du sujet si celui-ci est en rémission
TEMPS_INFECTE = 4 #Nombre de tours nécessiares à une infecté pour passer en rémission
TEMPS_REMISSION = 4 #Nombre de tours nécessiares à une personne en rémission pour redevenir saine
couleurs=['green','blue','red'] #Couleurs disponibles à la modélisation
NB_LIGNES=50 #Nombre de lignes du tableau
NB_COLONNES=50 #Nombre de colonnes du tableau
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
    matrice[1][1][1] = plateau[1][l][c]
    
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

plateau=ini_plateau(NB_LIGNES,NB_COLONNES)
print(plateau)
#print(plateau)
#print(evolution(plateau))


###############################################################################

def afficher(plateau):
    """Affiche sur un graphique en 2D les points d'un plateau pssé en argument"""
    # Récupère la taille du plateau pour pouvoir le parcourir
    ligne=plateau.shape[1]
    colonne=plateau.shape[2]
    for l in range(ligne):
        for c in range(colonne):
            """ Affiche le point de coordonnée l,c de la couleur qui lui est associé""" 
            plt.scatter(c,-l,c=couleurs[plateau[0][l][c]])
            """ Notez l'inversion du l et du c dans les coordonnées ainsi que
            l'apparition d'un signe - devant le l afin de respecter la configuration
            d'affichage des array numpy"""
    plt.show()
    
#afficher(plateau)

for i in range(10):
    plateau=evolution(plateau)
    afficher(plateau) 


tf = time.time() #Temps final
print(tf - t0) #Affiche la durée d'execution du programme

"""
Liste des choses à faire :
    - Nouvelle matrice pour les comportements
    - Matrice pour le nombre de réinfection (ou modification des règles)
    - Mise en place d'une part d'aléatoire dans la rémission  + ajout d'un temps d'immunité pendant la rémission.




































