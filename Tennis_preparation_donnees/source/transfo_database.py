# -*- coding: utf-8 -*-
"""
Database transformation
author: @Darrkhl
"""
#Libraries

import random
import csv 
import os

#random.seed(10)

#FUNCTIONS
         
#we take all the .CSV files of a specific folder, for each of them we only keep the rows we need
def get_all_csv(directory, delim):
    db = []
    for filename in os.listdir(directory):        
        path = (directory + '/' + filename)
        if path.endswith(".csv"):
            file = []
            with open(path, 'r', encoding = 'utf-8-sig') as csv_file :
                reader_csv = csv.reader(csv_file, delimiter=delim)
                for line in reader_csv :
                    file.append(line)                           
                db.append(file)    
        continue                   
    return db

#we only work on the grand slam matches
def select_series(db, column = "Series", series = "Grand Slam"):
    final_db = []   
    for file in db:
        temp_db = []
        if len(file) > 0:                     
            temp_db.append(file[0])
            for line in file:
                if line[file[0].index(column)] == series:
                    temp_db.append(line)   
                
        final_db.append(temp_db)
    return final_db

#we keep only the columns (entered in the desired order) we are interested in
def selected_columns(db, *columns):
     final_db = []         
     #header for our final db     
     col = [c for c in columns]
     final_db.append(col)
     
     for file in db:
         ind = [file[0].index(el) for el in col]         
         for line in file[1:]:
             new_line = [line[i] for i in ind]              
             final_db.append(new_line)        
    
     return final_db

#(if relevant) we only consider a specific round of play
def select_round(db, Round = "1st Round"):    
    ind = db[0].index("Round")      
    final_db = [line for line in db[1:] if line[ind] == Round]    
    final_db.insert(0, db[0])
    return final_db
 
#(if relevant) we only consider player ranked under a set number
def select_players_ranks(db, max_rank = 11):   
    ind = [db[0].index("WRank"), db[0].index("LRank")]
    final_db = []
    for line in db[1:]:
        try :        
            if int(line[ind[0]]) < max_rank :
                pass
            else : 
                final_db.append(line)
        except ValueError:
            final_db.append(line)
    final_db.insert(0, db[0])
    return final_db
     
#randomisation of the attribution : player 1/2 
def randomisation_player(db, win = "Winner", name1 = "P1", name2 = "P2"):  
    random_p1p2 = [random.choice((name1,name2)) for i in range(len(db[1:]))]         
    winner = [db[1:][i][db[0].index(win)] for i in range(len(db[1:]))]              
    return [[x,y] for x,y in zip(winner,random_p1p2)]   

#first step : transform the structure of the db, we're left with only Player 1 or 2 
#no reference to winner or loser 
def rename_type(db, list_winner, *columns_winner):
    final_db = []        
    ind_col_w = [db[0].index(c) for c in columns_winner]
    ind_col_l = [i+1 for i in ind_col_w ]
    
    for i_win in range(len(list_winner)):        
        if list_winner[i_win][1] == "P1":
            play1 = [db[1:][i_win][index_win] for index_win in ind_col_w]                        
            play2 = [db[1:][i_win][index_los] for index_los in ind_col_l]     
              
            temp = []
            for el in range(len(ind_col_w)) :
                temp.append(play1[el])
                temp.append(play2[el])   
            temp.append("P1")
            
        elif list_winner[i_win][1] == "P2":
            play1 = [db[1:][i_win][index_los] for index_los in ind_col_l] 
            play2 = [db[1:][i_win][index_win] for index_win in ind_col_w]                                                              
            temp = []
            for el in range(len(ind_col_l)) :
                temp.append(play1[el])
                temp.append(play2[el])     
            temp.append("P2")
                
        final_db.append(temp)        
    return final_db

#merge player infos with match info with 
def concat(header, db_total, player_info, general_col = 4):
    final_db = [header]
    
    for ind in range(len(db_total[1:])):
        temp = []
        for j in range(general_col):
            temp.append(db_total[1:][ind][j])
        for k in range(len(player_info[0])):
            temp.append(player_info[ind][k])
            
        final_db.append(temp)
    return final_db

#take the final database and switch which player is player 1/player 2 (in order to measure where our model depends on player1/2)
def switchp1_p2(db_p1p2, general_col = 4, type1 = "P1", type2 = "P2"):
    final_db = [db_p1p2[0]]
    for ind in range(len(db_p1p2[1:])):
        temp = []
        for j in range(general_col):
            temp.append(db_p1p2[1:][ind][j])
        for k in range(general_col+1,len(db_p1p2[0]), 2):
            temp.append(db_p1p2[1:][ind][k])
            temp.append(db_p1p2[1:][ind][k-1])
        if db_p1p2[1:][ind][-1] == type1:
            temp.append(type2)
        else :
            temp.append(type1)
        
        final_db.append(temp)
    return final_db

      
#transform a list of lists into a csv file utf-8 encoded 
def list_to_csv(file_name,db, delim):
    with open(file_name, 'w', newline='', encoding = 'utf-8-sig') as csv_file:
        content = csv.writer(csv_file, delimiter=delim)
        if type(db) is list :
            for line in db:
                if type(line) is list and len(line)>1 :
                    content.writerow(line)
                    
##############################################################################                                 
 
#CORE PROGRAM 

#First phase on raw data

all_csv = get_all_csv(directory = "../csv", delim = ";")
grand_slams = select_series(all_csv, column = "Series", series = "Grand Slam")

#for example 1 
#gs_reduced = selected_columns(grand_slams, "Tournament", "Surface", "Date", "Round", "Winner", "Loser", "WRank", "LRank", "WPts", "LPts", "B365W", "B365L", "PSW", "PSL")

#for example 2
gs_reduced2 = selected_columns(grand_slams, "Tournament", "Surface", "Date", "Round", "Winner", "Loser","W1", "L1", "W2", "L2", "W3", "L3",  "WRank", "LRank", "WPts", "LPts", "B365W", "B365L", "PSW", "PSL")

            #######################
  
#Final phase on processed data 

#Example 1 with just basic data

#gs_1stRound = select_round(gs_reduced, Round = "1st Round")
#gs_1stRound_rank11plus = select_players_ranks(gs_1stRound, max_rank = 11)
#winner = randomisation_player(gs_1stRound_rank11plus)
#player12_infos = rename_type(gs_1stRound_rank11plus, winner, 'Winner', 'WRank', 'WPts', "B365W","PSW")
#db_header = ["Tournament", "Surface", "Date", "Round", "J1", "J2", "J1Rank", "J2Rank", "J1Pts", "J2Pts", "B365J1", "B365J2", "PSJ1", "PSJ2","res"]
#final_db = concat(db_header, gs_1stRound_rank11plus, player12_infos, general_col= 4)
#file_final_db = list_to_csv("final_db_2010-2018.csv", final_db)
#final_db_p1p2switch = switchp1_p2(final_db, general_col = 4, type1 = "P1", type2 = "P2")
#file_final_db_switch = list_to_csv("final_db_2010-2018_switch.csv", final_db_p1p2switch)


#Example with basic info +  columns of number of games won per sets for winner /loser 

gs_1stRound2 = select_round(gs_reduced2, Round = "1st Round")
gs_1stRound_rank11plus2 = select_players_ranks(gs_1stRound2, max_rank = 11)
winner2 = randomisation_player(gs_1stRound_rank11plus2)
player12_infos2 = rename_type(gs_1stRound_rank11plus2, winner2, 'Winner', "W1", "W2", "W3",'WRank', 'WPts', "B365W","PSW")
db_header2 = ["Tournament", "Surface", "Date", "Round", "J1", "J2", "J1set1", "J2set1", "J1set2", "J2set2", "J1set3", "J2set3", "J1Rank", "J2Rank", "J1Pts", "J2Pts", "B365J1", "B365J2", "PSJ1", "PSJ2","res"]
final_db2 = concat(db_header2, gs_1stRound_rank11plus2, player12_infos2, general_col= 4)
#file_final_db2 = list_to_csv("final_db2_2010-2018.csv", final_db2)
final_db_p1p2switch2 = switchp1_p2(final_db2, general_col = 4, type1 = "P1", type2 = "P2")
#file_final_db_switch2 = list_to_csv("final_db2_2010-2018_switch.csv", final_db_p1p2switch2)

