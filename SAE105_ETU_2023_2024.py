"""
Programme SAE 105: Traitement de données:
Fichier: ville_france.csv contenant des informations sur les 36700 Villes de France
BUT1 : Année 2022-2023
@author: A compléter avec Votre NOM - Prénom - Groupe_TP
"""
# pour afficher la carte avec les villes
"""
import folium,branca
import matplotlib.pyplot as plt
import math
"""
import os
import random
import folium, branca
import matplotlib.pyplot as plt
from math import *
from colorama import *

#-----------------------------------------------------------
# Fonction qui extrait les 12 informations sur chaque ville
#-----------------------------------------------------------

def lire_fichier_csv(nomFich):
    """
    Cette fonction permet de LIRE les données du fichier villes_france.csv
    le fait d'utiliser readlines permet de récupérer une liste dont chaque élément correspond à une ville
    ainsi que toutes les données associées
    :param nomFich: fichier "villes_france.csv"
    :return: une liste "liste_villes" dont chaque élément est une str qui comporte toutes les données d'une ville
    (27 données par ville au total)
    """
    fich = open(nomFich,'r')
    liste_villes = fich.readlines()

    #print("Fin de l'Extraction des infos du fichier",nomFich)
    fich.close()
    return liste_villes

def extract_info_villes(uneListe):
    """
    Fonction qui extrait les 12 informations de la liste[str] extraite du fichier Excel
    :param : uneListe:
    :return: L: une liste dont chaque élément contient les 12 infos de la ville
    la taille de la liste L[] retournée est de 36700 villes
    """
    L= []
    temp = []
    for i in uneListe:
        temp.append(i.split(','))
    #print("taille = ",len(temp))

    """
    Il faut faire attention aux Départements de Corse : 2A et 2B
    et également aux département d'Outre-Mer : 971, 972, ...,977
    """
    for i in temp:
        # eval(..) transforme "Annecy" en Annecy, et "18.59" en 18.59 donc une chaîne de caractères sans les "..."
        # ensuite il faut transformer le type str() en int() ou float()
        # Pour tous les départements sauf la Corse 2A et 2B
        # et les territoires d'Outre-Mer : les derniers champs sont à 'NULL'
        if ((eval(i[1]) != '2A') and (eval(i[1]) != '2B')) and i[25] != 'NULL':
            L.append([int(eval(i[1])),      # numéro du Département
                    eval(i[3]),             # Nom de la ville en MAJUSCULE
                    eval(i[8]),             # Code postal
                    int(eval(i[14])),       # population en 2010
                    int(eval(i[15])),       # population en 1999
                    int(eval(i[16])),       # population en 2012
                    float(eval(i[17])),     # densité
                    float(eval(i[18])),     # surface
                    float(eval(i[19])),     # longitude
                    float(eval(i[20])),     # latitude
                    int(eval(i[25])),       # altitude min
                    int(eval(i[26]))])      # altitude max
        elif i[13] == 'NULL': # pour gérer les départements et territoires d'Outre-Mer : 971, 972, 974, ...
            L.append([int(eval(i[1])),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      "NULL",
                      "NULL"])
        else:
            L.append([eval(i[1]),
                      eval(i[3]),
                      eval(i[8]),
                      int(eval(i[14])),
                      int(eval(i[15])),
                      int(eval(i[16])),
                      float(eval(i[17])),
                      float(eval(i[18])),
                      float(eval(i[19])),
                      float(eval(i[20])),
                      i[25],
                      i[26]])


    return L

#====================================================================
# Compte le Nombre de villes en fonction de l'indicatif téléphonique
#====================================================================
def appelNombre_Villes_Indicatif(indTel, unelisteInfo):
    """
        A compléter
    """
    reg_01 = ["75","77","78","91","92","93","94","95"]
    reg_02 = ["14","18","22","27","28","29","35","36","37","41","44","45","49","50","53","56","61","72","76","85","974","976"]
    reg_03 = ["2","8","10","21","25","39","51","52","54","55","57","58","59","60","62","67","68","70","71","80","88","89","90"]
    reg_04 = ["1","3","4","5","6","7","11","13","15","2A","2B","26","30","34","38","42","43","48","63","66","69","73","74","83","84"]
    reg_05 = ["9","12","16","17","19","23","24","31","32","33","40","46","47","64","65","79","81","82","86","87","971","972","973","975","977","978"]
    listes_reg = [reg_01, reg_02, reg_03, reg_04, reg_05]

    liste_dept = listes_reg[int(indTel[1:])-1]
    # int(indTel[1:]) -> Récupère le deuxième caractère de l'indice téléphonique et le converti en entier.
    # -1 -> soustrais 1 à la valeur de l'indice téléphonique
    # EXEMPLE : 01 -> 1 -> 0
    # listes_reg[...] on récupère la valeur correspondant à la liste.
    # D'où le "-1" comme l'indexation d'une liste commence à 0 et celui de l'indice téléphonique à 01.
    # On fait -1 pour récupérer la valeur correspondante dans la liste.

    return extract_villes_depart_indicatif(liste_dept, unelisteInfo)

#--------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
#--------------------------------------------------------
def extract_villes_depart_indicatif(listeDept, listeInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction de l'indicatif téléphonique (01 = Île-de-France, 02 = Nord-Ouest, ...

    :param listeDept: qui est la liste des départements ayant cet indicatif
    :param listeInfo: liste du nom de villes
    :return: nbVilles = nombre de villes
    """
    increment = 0
    villes = []

    with open(f"NE02.txt", "w", encoding="utf-8") as my_file: 

        for ville in listeInfo:
            if str(ville[0]) in listeDept: # Si l'indicatif téléphonique est dans la liste listeDept.
                increment += 1 # Est utilisé pour écrire (dans le fichier NE02.txt) cette ville est la combientième trouvée. 
                villes.append(ville) # Ajoute la ville trouvé dans la liste villes.

                my_file.write(f"{increment} {ville[1]} ({ville[0]})\n") # Ecrit dans le fichier NE02.txt des informations. 

    return len(villes)

#--------------------------------------------------------
# Procédure qui permet d'appeler la fonction
# qui extrait les informations sur les villes
#---------------------------------------------------------
def appelExtractionVilles():
    #print("Extraction des informations des Villes de France")
    listeVillesFr = lire_fichier_csv("villes_france.csv")
    #print("une ligne = ",listeVillesFr[0])

    # la liste info contient les 12 Informations retenues pour la suite du programme
    info = extract_info_villes(listeVillesFr)

    return info

#==========================================================
# Recherche les infos d'une Ville dans la liste
#==========================================================
def rechercheVille(name,listeVilles):
    """
    :param name: nom de la ville recherchée doit être en MAJUSCULE
    :param listeVilles: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """

    #Recherche une ville par son nom dans la liste générale.
    for ville in listeVilles:
        if name == ville[1]:
            return ville
    

# --------------------------------------------------------
# Fonction extract_villes_depart_indicatif(listeInfo)
# --------------------------------------------------------
def extract_villes_NumDepart(numDept, listeInfo):
    """
    Fonction qui extrait l'ensemble des villes pour chaque département,
    en fonction du numéro du Département

    :param numDept: numéro du département
    :param listeVilles: liste des noms de villes
    :return: nbVilles = nombre de villes du département
    """
    villes_dep = []

    with open(f"villes_n°{numdDept}.txt", "w", encoding="utf-8") as f:
        for ville in listeInfo: #On parcours la listeInfo
            if ville[0] == numDept: #Si le numéro de département est égal.

                villes_dep.append(ville) #Ajoute la ville dans la liste villes_dep
                f.write(f"{ville}\n") #Ecrit la ville dans le fichier ville_n°Numdept.txt

    return len(villes_dep), villes_dep #On retourne la taille de la liste (nb de villes) et la liste des villes du département.

# ================================================
# Fonctions Utiles pour le Tri Bulle lié à la POPULATION
# ================================================
def unPassage(tab):
    """
    Fonction complémentaire l'algorithme tribulle.
    """
    for i in range (len(tab)-1):
        if tab[i][3] > tab[i+1][3]:
            tab[i], tab[i+1] = tab[i+1], tab[i] 
    return tab

def triBulle(liste):
    for i in range(len(liste)):
        liste = unPassage(liste)
    return liste

def MinMax5_villes_Habitants(listeInfoDept):
    """
    :param numDept:
    :param lstVillesDepart:

        recherche de 5 villes ayant le MOINS d'habitants dans un tableau
        recherche de 5 villes ayant le PLUS d'habitants dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
    """
    liste_min5 = triBulle(listeInfoDept)[0:5] #On récupère les 5 premières villes de la liste triée.
    liste_top5 = triBulle(listeInfoDept)[len(listeInfoDept)-5:len(listeInfoDept)] #On récupère les 5 dernières villes de la liste triée.

    with open("Min5Villes_n°14.txt", "w", encoding="utf-8") as f:
        for i in liste_min5: #On parcours la liste des 5 villes avec le moins d'habitants
            f.write(f"{i}\n") #On écris la ville dans le fichier texte Top5Villes_n°14.txt
            
    with open("Top5Villes_n°14.txt", "w", encoding="utf-8") as f:
        for i in liste_top5: #On parcours la liste des 5 villes avec le plus d'habitants
            f.write(f"{i}\n") #On écris la ville dans le fichier texte Top5Villes_n°14.txt

#-------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la population MAX, et 5 ayant la population MIN)
#-------------------------------------------------------------------------
def mapTenVilles(maxPopul, minPopul):
    """
    :param maxPop: fichier contenant les 5 villes de forte densité
    :param minPop: fichier contenant les 5 villes de faible densité
    :return:
    """
    with open(maxPopul, "r") as f_max:
        villes_max = f_max.readlines() # On lis les lignes du fichier.

    with open(minPopul, "r") as f_min:
        villes_min = f_min.readlines() # On lis les lignes du fichier.

    LATS = []
    LONGS = []
    TEMPS = []
    coords = (46.539758, 2.430331)
    
    for i in villes_max+villes_min: # On concatène les liste pour en parcourir une seule. (Moins de complexité)
        i = i.split(",") # On split la string récupérée par des virgules pour récupérer les valeurs de la "liste" qui est en str. 
        
        #On ajoute les valeurs dans la liste LONGS, LATS, TEMPS.
        LONGS.append(float(i[8]))
        LATS.append(float(i[9]))
        TEMPS.append(float(i[6]))
        
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(TEMPS), vmax=max(TEMPS))
    map1.add_child(cm)

    for lat, lng, size, color in zip(LATS, LONGS, TEMPS, TEMPS):
        folium.CircleMarker(
            location=[lat, lng],
            radius=size/100,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)

    map1.save(outfile='densite_ville.html')
    print("Traitement Terminée, le fichier s'apelle densite_ville.html")

def unPassage_modifier(tab):
    """
    Fonction complémentaire l'algorithme tribulle modifée.
    """
    for i in range (len(tab)-1):
        if tab[i][0] > tab[i+1][0]:
            tab[i], tab[i+1] = tab[i+1], tab[i] 
    return tab

def triBulle_modifier(liste):
    for i in range(len(liste)):
        liste = unPassage_modifier(liste)
    return liste

def MinMax10Accroissement(lstVillesDepart):
    """
    :param lstVillesDepart:

        recherche de 10 villes ayant la plus FORTE BAISSE de sa population entre 1999 et 2012
        recherche de 10 villes ayant le plus FORT ACCROISSEMENT de sa population entre 1999 et 2012
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 10 premières valeurs et 10 dernières valeurs
    """
    liste_accroissement = []
    value = 0
    
    for i in lstVillesDepart:
        value = i[5]-i[4] # Soustraction pour évaluer l'accroisement.
        liste_accroissement.append([value, i])
        
    liste_accroissement_trie = triBulle_modifier(liste_accroissement)[len(liste_accroissement)-10:len(liste_accroissement)] #On récupère les 10 dernière valeurs de la liste triée.
    liste_baisse_trie = triBulle_modifier(liste_accroissement)[0:10] #On récupère les 10 premières valeurs de la liste triée.
    
    
    with open("TopAcc10Villes_n°Dept.txt", "w", encoding="utf-8") as f:
        for i in liste_accroissement_trie:
            f.write(f"{i[1][0]}, {i[1][1]}, {i[0]}\n") # Ecriture des valeurs intéréssantes (des villes) dans le fichier TopAcc10Villes_n°Dept.txt.
            
    with open("TopBaisse10Villes_n°Dept.txt", "w", encoding="utf-8") as f:
        for i in liste_baisse_trie:
            f.write(f"{i[1][0]}, {i[1][1]}, {i[0]}\n") # Ecriture des valeurs intéréssantes (des villes) dans le fichier TopBaisse10Villes_n°Dept.txt.

def MinMax5Alt_Dept(listeInfoDept):
    """
    :param lstVillesDepart:

        recherche de 5 villes ayant la plus FAIBLE différence d'altitude dans un tableau
        recherche de 5 villes ayant la plus FORTE différence d'altitude dans un tableau
        on peut trier la liste par ordre croissant
        *** On IMPOSE le TRI BULLE vu au TP7 ****
        puis extraire les 5 premières valeurs
        Numéro du département = lstVillesDepart[0][0]
    """
    DiffAlt_liste = []

    # Même principe que le fonction ci-dessus MinMax10Accroissement(...). Juste optimisée.
    for ville in listeInfoDept:
        DiffAlt_liste.append([ville[11]-ville[10], ville]) 
    
    DiffAlt_liste_trie = triBulle_modifier(DiffAlt_liste)
    MaxdiffAlt = DiffAlt_liste_trie[len(DiffAlt_liste)-5:len(DiffAlt_liste)]
    MindiffAlt = DiffAlt_liste_trie[0:5] 
    
    with open("Top5Alt_n°14.txt", "w", encoding="utf-8") as f:
        for i in MaxdiffAlt:
            f.write(f"{i[1][0]}, {i[1][1]}, {i[1][8]}, {i[1][9]}, {i[0]}\n")
            
    with open("Min5Alt_n°14.txt", "w", encoding="utf-8") as f:
        for i in MindiffAlt:
            f.write(f"{i[1][0]}, {i[1][1]}, {i[1][8]}, {i[1][9]}, {i[0]}\n")

#-------------------------------------------------------------------------
# Procédure qui permet d'afficher sur une carte OpenStreetMap
# les 10 villes (5 ayant la différence d'ALTITUDE MAX
# et 5 ayant la différence d'ALTITUDE MIN)
#-------------------------------------------------------------------------
def mapTenAlt(maxAlt, minAlt):
    """
    :param maxAlt: fichier contenant les 5 villes de forte différence d'altitude
    :param minAlt: fichier contenant les 5 villes de faible différence d'altitude
    :return:
    """
    
    # EXACTEMENT le même principe que la fonction mapTenVilles(...).
    with open(maxAlt, 'r') as f:
        value_maxAlt = f.readlines()
    
    with open(minAlt, 'r') as f:
        value_minAlt = f.readlines()
        
    LONGS = []
    LATS = []
    TEMPS = []
    coords = (46.539758, 2.430331)
    
    for i in value_maxAlt+value_minAlt:
        i = i.split(",")
        LONGS.append(float(i[2]))
        LATS.append(float(i[3]))
        TEMPS.append(int(i[4]))
        
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(TEMPS), vmax=max(TEMPS))
    map1.add_child(cm)

    for lat, lng, size, color in zip(LATS, LONGS, TEMPS, TEMPS):
        folium.CircleMarker(
            location=[lat, lng],
            radius=size/50,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)

    map1.save(outfile='altitudes_ville.html')
    print("Traitement Terminée, le fichier s'apelle altitudes_ville.html")
    


#===================================================================
# Construction de l'HISTOGRAMME
#===================================================================
def traceHistoVilles(listeInfoDept):
    habitants_2010 = []
    moyenne = 0
    ecartype = 0
    
    for ville in listeInfoDept:
        habitants_2010.append(ville[3])
        moyenne += ville[3]
    
    moyenne = moyenne/len(listeInfoDept)
    for i in listeInfoDept:
        ecartype += (i[3]-moyenne)**2
    ecartype = sqrt(ecartype/len(listeInfoDept))
    print(f"La valeur de l'ecart type est de : {ecartype}")
    print(f"La moyenne d'habitants est de : {moyenne}")
    
    plt.hist(habitants_2010,bins=100, color='blue', edgecolor='red')
    plt.title(f"nombre de villes en fonction de leur population")
    plt.xlabel("Population")
    plt.ylabel("Nombre de villes")
    plt.show()

#====================================================================
# Distance EUCLIDIENNE entre 2 villes (en km)
#====================================================================
def dist_Euclidienne(ville1, ville2):
    # Méthode par le calcul de Pythagore : https://www.bibmath.net/dico/index.php?action=affiche&quoi=./d/distance.html#:~:text=La%20distance%20euclidienne%20%3A%20d2,1−y2%7C2.
    Xa, Xb = ville1[8], ville2[8]
    Ya, Yb = ville1[9], ville2[9]

    distance = sqrt((Xb - Xa)**2 + (Yb - Ya)**2)

    return distance*10**2

#====================================================================
# Distance GEODESIQUE (surface de la terre) entre 2 villes (en km)
# Formule de Haversine
#====================================================================
def dist_GEOdesique(ville1, ville2):
    # calcul par la méthode HAVERSINE : http://villemin.gerard.free.fr/aGeograp/Distance.htm
    LONa, LONb = radians(ville1[8]), radians(ville2[8])
    LATa, LATb = radians(ville1[9]), radians(ville2[9]) # On converti en RADIAN car sinon les valeur son éronée. (Formule)

    a = sin((LATb - LATa)/2)**2 + (cos(LATa) * cos(LATb) * sin((LONb - LONa)/2)**2)
    c = 2*atan2(sqrt(a), sqrt(1-a))
    d = 6371*c

    return d

#===============================================================
# ETAPE 5 : Parcours Ville1 ==> Ville2
#===============================================================

#=================================================================
# Recherche un ensemble de villes distante de R km dans une liste
#=================================================================
def ensembleVilles(ville1, rayon, listeInfo):
    """
    :param name: centre = ville avec les 12 infos
    :param rayon: distance de la ville retenue
    :param listeInfo: liste de toutes les villes
    :return: listeVilles[i] : la ville recherchée
    """
    listeVillesTrouvees = []
    
    while len(listeVillesTrouvees) <= 50: # Tant qu'on à pas trouver au minimum 50 villes dans le rayon (Marge pour éviter toute erreur).
        for ville in listeInfo:
            if isInDisque(ville1, ville, rayon): # Si la ville est dans le disque de rayon "rayon".
                listeVillesTrouvees.append(ville) #Ajoute alors la ville dans la liste : listeVillesTrouvees.
           
        rayon += 1
             
    return listeVillesTrouvees

def plusProche(listeVillesTrouvees, ville2): 
    min_distance = 1000
    VillePlusProche = None

    for ville in listeVillesTrouvees: # On parcours la liste des listeVillesTrouvees.
        distance = dist_GEOdesique(ville, ville2) # Calcul la distance géodésique entre deux villes.

        if distance < min_distance: # Si la distance géodésique est plus petite que la min_distance actuelle.

            min_distance = distance # La nouvelle min_distance est distance.
            VillePlusProche = ville # La nouvelle VillePlusProche est la ville avec la plus petite distance. 

    return VillePlusProche

def isInDisque(ville, uneVille, rayon):

    if dist_GEOdesique(ville, uneVille) < rayon: # Si la ville est dans le disque de rayon "rayon".
        return True
    else: 
        return False


#===================================================================
# ETAPE 5 : Plus court chemin entre les 2 Villes vil1 et vil2
#===================================================================
def parcoursVilles(vil1, vil2, listeRef, rayon):
    Final = None
    ListeParcourt = []

    with open("parcours.txt", 'w') as f: # On ouvre le fichier parcours.txt.
        while Final != vil2: # Tant que la ville parcourue n'est pas la ville finale.

            liste = ensembleVilles(vil1, rayon, listeRef) # On récupère la liste des villes autour de vil1.
            vil1 = plusProche(liste, vil2) # On met la ville la plus proche dans le rayon de le ville finale dans la variable "vil1".
            
            Final = vil1 # On met la ville parcourue dans la vaiable Final.
            
            ListeParcourt.append(vil1) # On ajoute la ville dans le liste ListeParcourt.

            f.write(f"Ville traversée : {Final}\n")
            print("Ville traversée :", Final[1])

    return ListeParcourt


#----------------------------------------------------------------------------------
# On sauvegarde le trajet dans un fichier html pour l'afficher dans un navigateur
#----------------------------------------------------------------------------------
def map_trajet(villes_traversees):
    # Même principe que la fonction mapTenAlt(...) sans le split.

    LONGS = []
    LATS = []
    TEMPS = []
    coords = (46.539758, 2.430331)
    
    for ville in villes_traversees:
        
        LONGS.append(ville[8])
        LATS.append(ville[9])
        TEMPS.append(10)

        
    map1 = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min(TEMPS), vmax=max(TEMPS))
    map1.add_child(cm)

    for lat, lng, size, color in zip(LATS, LONGS, TEMPS, TEMPS):
        folium.CircleMarker(
            location=[lat, lng],
            radius=size,
            color=cm(color),
            fill=True,
            fill_color=cm(color),
            fill_opacity=0.6
        ).add_to(map1)

    map1.save(outfile='map_parcours.html')

#===============================================================
# AFFICHE MENU
#===============================================================

def afficheMENU():
    print("\n================ MENU ==================")
    print("taper 1: Nombre de villes en fonction de l'indicatif téléphonique")
    print("taper 2: Extraire des Statistiques des Villes d’un département")
    print("taper 3: Distance Euclidienne et Géodésique entre 2 villes")
    print("taper 4: Plus court chemin entre 2 villes")
    print("F: pour finir")


def afficheSOUS_MENU(unDepartement):
    print("\n================ SOUS MENU : STATISTIQUES du Département ", unDepartement, "==================")
    print("taper 1: Lister les 5 Villes ayant le plus/le moins d'habitants")
    print("taper 2: Afficher les 10 Villes en fonction de la DENSITE sur une carte")
    print("taper 3: Lister les 10 Villes ayant le plus fort/faible taux d'accroissement")
    print("taper 4: HISTOGRAMME des villes par habitants")
    print("taper 5: Lister les 5 Villes ayant la différence d'altitude max/min")
    print("taper 6: Afficher les 10 Villes en fonction de l'ALTITUDE sur une carte")
    print("Q: pour Quitter le sous-menu")


def verifError(ville1, ville2):
    if ville1 is None and ville2 is None:
        return True, f"{Back.RED}ERREUR{Back.RESET} {Fore.RED}{Style.BRIGHT}La 1ère ville et la 2ème ville n'existent pas.{Style.RESET_ALL}{Fore.RESET}"
    if ville1 is None:
        return True, f"{Back.RED}ERREUR{Back.RESET} {Fore.RED}{Style.BRIGHT}La 1ère ville n'existe pas.{Style.RESET_ALL}{Fore.RESET}"
    if ville2 is None:
        return True, f"{Back.RED}ERREUR{Back.RESET} {Fore.RED}{Style.BRIGHT}La 2ème ville n'existe pas.{Style.RESET_ALL}{Fore.RESET}"
    return False, 

#=============================================================================================
# Programme principal
# Appel de la procédure afficheMENU()
#=============================================================================================
fini = False
while fini == False:
    afficheMENU()
    choix = input("votre choix: ")
    if choix == '1':
        # Pour débuter il faut extraire des informations du fichier CSV
        listeInfo = appelExtractionVilles()
        #=====================================

        indTel = input(f"{Fore.CYAN}Quel indicatif Téléphonique souhaitez-vous ? {Fore.RESET}")
        print(f"Voici le nombre de ville de l'indicatif {indTel} : {appelNombre_Villes_Indicatif(indTel, listeInfo)}")
    elif choix == '2':
        print(f"\n{Fore.CYAN}**** Nombre de Villes par Département *****{Fore.RESET}")
        numdDept = int(input("Donner le numéro du département : "))
        listeInfo = appelExtractionVilles()
        nb_villes, liste_villes_dep = extract_villes_NumDepart(numdDept, listeInfo)
        print(f"il y a {nb_villes} villes.")
        #=====================================
        finiBis = False
        while finiBis == False:
            # ==> Changer le numéro du Département <==
            afficheSOUS_MENU(numdDept)
            choixBis = input("votre choix: ")
            if choixBis == '1':
                print(f"\n{Fore.CYAN}appel de la stat1 : Min/Max Habitants : 5 villes{Fore.RESET}\n")
                MinMax5_villes_Habitants(liste_villes_dep)
            elif choixBis == '2':
                print(f"\n{Fore.CYAN}appel de la stat2: Afficher les 10 villes (DENSITE) sur la carte{Fore.RESET}\n")
                MinMax5_villes_Habitants(liste_villes_dep)
                mapTenVilles("Top5Villes_n°14.txt", "Min5Villes_n°14.txt")
            elif choixBis == '3':
                print(f"\n{Fore.CYAN}appel de la stat3: ACCROISSEMENT/BAISSE population entre 1999 et 2012{Fore.RESET}\n")
                MinMax10Accroissement(liste_villes_dep)
            elif choixBis == '4':
                print(f"\n{Fore.CYAN}appel de la stat4 : HISTOGRAMME du nombre des Villes par habitants{Fore.RESET}\n")
                traceHistoVilles(liste_villes_dep)
            elif choixBis == '5':
                print(f"\n{Fore.CYAN}appel de la stat5 : ALTITUDE Min/Max : 5 villes{Fore.RESET}\n")
                MinMax5Alt_Dept(liste_villes_dep)
            elif choixBis == '6':
                print(f"\n{Fore.CYAN}appel de la stat6: Afficher les 10 villes (ALTITUDE) sur la carte{Fore.RESET}\n")
                MinMax5Alt_Dept(liste_villes_dep)
                mapTenAlt("Top5Alt_n°14.txt", "Min5Alt_n°14.txt")
            else:
                finiBis = True

    elif choix == '3':
        listeInfo = appelExtractionVilles()
        ville_depart, ville_arrivee = input("Entrez la ville de départ : ").upper(), input("Entrez la ville d'arrivée : ").upper()
        ville1, ville2 = rechercheVille(ville_depart, listeInfo), rechercheVille(ville_arrivee, listeInfo)

        verification = verifError(ville1, ville2)
        if verification[0]:
            print(verification[1])
            break
            
        print(f"\n{Fore.CYAN}Distance Euclidiene entre 2 villes{Fore.RESET}")
        print(f"La distance en kilomètres est : {Fore.GREEN}{round(dist_Euclidienne(ville1, ville2), 2)}{Fore.RESET}")

        print(f"\n{Fore.CYAN}Distance Géodésique entre 2 villes{Fore.RESET}")
        print(f"La distance Géodésique en kilomètres est : {Fore.GREEN}{round(dist_GEOdesique(ville1, ville2), 1)}{Fore.RESET}")

    elif choix == '4':
        print(f"\n{Fore.CYAN}Plus court chemin entre 2 villes{Fore.RESET}")
        listeInfo = appelExtractionVilles()
        ville_depart, ville_arrivee = input(f"Entrez la ville de départ : ").upper(), input("Entrez la ville d'arrivée : ").upper()
        ville1, ville2 = rechercheVille(ville_depart, listeInfo), rechercheVille(ville_arrivee, listeInfo)

        verification = verifError(ville1, ville2)
        if verification[0]:
            print(verification[1])
            break
        
        villes_traversees = parcoursVilles(ville1, ville2, listeInfo, 1)
        map_trajet(villes_traversees)

        print(f"{Fore.GREEN}*** Traitement terminé, Map réalisée sous le nom map_parcours.html ***{Fore.RESET}")
    elif choix == '5':
        print("\nAppel de la fonction4\n")
    elif choix == 'F':
        fini = True

#print("Fin du programme")