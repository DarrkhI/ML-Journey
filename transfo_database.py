# -*- coding: utf-8 -*-
"""
Transformation de database

"""
#Libraries

import random
import csv 

#pour tester des morceaux de code et que le vecteur avec une donnée aleatoire ne change pas 
#à paritr du moment où vous l'avez lacé la premiere fois
#random.seed(10)

#FONCTIONS

#on ouvre / lit un fichier csv encodé en utf-8
def lecture_csv(fichier):
    lignes = []
    with open(fichier, 'r', encoding = 'utf-8') as fichier_csv :
      lecteur_csv = csv.reader(fichier_csv, delimiter=";")
      for ligne in lecteur_csv :
          lignes.append(ligne)
    return lignes

#on concatene toutes les matrices qui vont servir à l'apprentissage
def concatenation_GS(liste_bdd):
    base_complete = []
    for bdd in liste_bdd:
        for ind in range(len(bdd)):
            if bdd_2010[ind][2] == "Grand Slam":
                base_complete.append(bdd[ind])
    return base_complete

#on prend les infos qui nous interessent par joueur
def joueur_infos(ind_nom_joueur,ind2,ind3,ind4,ind5, bdd):
    infos = []
    for ligne in bdd:
            infos.append([ligne[ind_nom_joueur],ligne[ind2], ligne[ind3], ligne[ind4], ligne[ind5]])    
    return infos

#transformation d'une liste de listes en un fichier csv en utf-8
def ecriture(nom_fichier,bdd):
    with open(nom_fichier, 'w', newline='', encoding = 'utf-8') as fichier_csv:
        contenu = csv.writer(fichier_csv, delimiter=';')
        if type(bdd) is list :
            for ligne in bdd:
                if type(ligne) is list and len(ligne)>1 :
                    contenu.writerow(ligne)
                    
#concatenation des vecteurs et matrices
def modif_bdd(winner, loser, bdd_vierge):   
    for indice in range(len(winner)):
        ligne_bdd = []
        ligne_bdd.append(tournois[indice])
        ligne_bdd.append(surface[indice])
        ligne_bdd.append(Date[indice])
        ligne_bdd.append(Round[indice])
        if winner[indice][1] == "J1":
            for j in range(len(winner[indice][0])):
                ligne_bdd.append(winner[indice][0][j])
                ligne_bdd.append(loser[indice][0][j])                                
        elif winner[indice][1] == "J2":
            for j in range(len(winner[indice][0])):
                ligne_bdd.append(loser[indice][0][j])
                ligne_bdd.append(winner[indice][0][j])
            
        ligne_bdd.append(winner[indice][1])
        
        bdd_vierge.append(ligne_bdd)
    return bdd_vierge                    
 
#CORPS DU PROGRAMME

#travail sur les base de données
bdd_2010 = lecture_csv("2010.csv")
bdd_2011 = lecture_csv("2011.csv")
bdd_2012 = lecture_csv("2012.csv")
bdd_2013 = lecture_csv("2013.csv")
bdd_2014 = lecture_csv("2014.csv")
bdd_2015 = lecture_csv("2015.csv")
bdd_2016 = lecture_csv("2016.csv")
bdd_2017 = lecture_csv("2017.csv")
bdd_2018 = lecture_csv("2018.csv")

bdd = [bdd_2010, bdd_2011, bdd_2012, bdd_2013, bdd_2014, bdd_2015]

base_brute = concatenation_GS(bdd)

                ###############

#matrices avec les infos des maths par joueur gagnant/perdant
winner = joueur_infos(5,7,9,11, 13, base_brute)
loser = joueur_infos(6,8,10,12,14, base_brute)

#randomisation de l'attribution du J1/J2
random_j1j2 = [random.choice(("J1","J2")) for i in range(len(winner))]

#attribution J1/J2 par outcome
winner_num = [[x,y] for x,y in zip(winner,random_j1j2)]
loser_num = []
for indice in range(len(winner_num)):
    if winner_num[indice][1] == "J2":
        loser_num.append([loser[indice],"J1"])
    elif winner_num[indice][1] == "J1":
        loser_num.append([loser[indice],"J2"])
    
                   ###############
                    
#creation nouvelle bdd
bdd_entete = [["Tournament", "Surface", "Date", "Round", "J1", "J2", "J1Rank", "J2Rank", "J1Pts", "J2Pts", "B365J1", "B365J2", "PSJ1", "PSJ2","res"]]

#Creation vecteurs pas relatifs aux joueurs
tournois = [base_brute[i][0] for i in range(len(base_brute))]
surface = [base_brute[i][3] for i in range(len(base_brute))]
Date = [base_brute[i][1] for i in range(len(base_brute))]
Round = ["1st Round" for x in range(len(winner_num))] 
   

#dernieres manip : concatenation et transformation de la base finale en fichier csv   
base_finale = modif_bdd(winner_num, loser_num, bdd_entete)
#tennis_ = ecriture("tennis_2010_2015.csv", base_finale)   



