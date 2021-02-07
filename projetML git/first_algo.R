#your working directory :
#setwd("~PROJET 2021/projet ML")

library(rpart)
library(rpart.plot)
library(readr)
library(tidyverse)

set.seed(123)

#csv2 : csv file in the european format ; ie decimal point is "," and separator is ; 
db_complete <- read.csv2("Tennis_preparation_donnees/source/final_db2_2010-2018.csv",
                        na = "empty" , header = TRUE)


#####PREPARATION#########

#adding an id for each match 
db_complete$id <- 1:nrow(db_complete)

#changing the name because of some bug 
names(db_complete)[1] <- "Tournament"

#handle the na values 
db_complete$J2Rank <- gsub("N/A", 0, db_complete$J2Rank)
db_complete$J2Pts <- gsub("N/A", 0, db_complete$J2Pts)
db_complete$J1Rank <- gsub("N/A", 0, db_complete$J1Rank)
db_complete$J1Pts <- gsub("N/A", 0, db_complete$J1Pts)

#string to numbers
db_complete$J2Rank<- as.numeric(db_complete$J2Rank)
db_complete$J2Pts <- as.numeric(db_complete$J2Pts)
db_complete$J1Rank<- as.numeric(db_complete$J1Rank)
db_complete$J1Pts <- as.numeric(db_complete$J1Pts)

#We add some hopefully useful columns 
db_complete$DRank <- abs(db_complete$J1Rank - db_complete$J2Rank)
db_complete$DPts <- abs(db_complete$J1Pts - db_complete$J2Pts)
db_complete$Dset1 <- abs(db_complete$J1set1 - db_complete$J2set1)
db_complete$Dset2 <- abs(db_complete$J1set2 - db_complete$J2set2)
db_complete$Dset3 <- abs(db_complete$J1set3 - db_complete$J2set3)

#check if all is ok
View(db_complete)

#####PREPARATION Switched dataset#########

db_complete2 <- read.csv2("Tennis_preparation_donnees/source/final_db2_2010-2018_switch.csv",
                          na = "empty" , header = TRUE)


#adding an id for each match 
db_complete2$id <- 1:nrow(db_complete2)

#changing the name because of some bug 
names(db_complete2)[1] <- "Tournament"

#handle the na values 
db_complete2$J2Rank <- gsub("N/A", 0, db_complete2$J2Rank)
db_complete2$J2Pts <- gsub("N/A", 0, db_complete2$J2Pts)
db_complete2$J1Rank <- gsub("N/A", 0, db_complete2$J1Rank)
db_complete2$J1Pts <- gsub("N/A", 0, db_complete2$J1Pts)

#string to numbers
db_complete2$J2Rank<- as.numeric(db_complete2$J2Rank)
db_complete2$J2Pts <- as.numeric(db_complete2$J2Pts)
db_complete2$J1Rank <- as.numeric(db_complete2$J1Rank)
db_complete2$J1Pts <- as.numeric(db_complete2$J1Pts)

#We add some hopefully useful columns 
db_complete2$DRank <- abs(db_complete2$J1Rank - db_complete2$J2Rank)
db_complete2$DPts <- abs(db_complete2$J1Pts - db_complete2$J2Pts)
db_complete2$Dset1 <- abs(db_complete2$J1set1 - db_complete2$J2set1)
db_complete2$Dset2 <- abs(db_complete2$J1set2 - db_complete2$J2set2)
db_complete2$Dset3 <- abs(db_complete2$J1set3 - db_complete2$J2set3)

#check if all is ok
View(db_complete2)


#######Sample#########

#We cut the db in two, one training dataset and a testing one
#85% of entry in the train dataset th rest for testing
train <- db_complete %>% dplyr::sample_frac(.85) 
#nrow(train) 
test  <- dplyr::anti_join(db_complete, train, by = 'id') #~303 row

train2 <- db_complete2 %>% dplyr::sample_frac(.85) 
test2  <- dplyr::anti_join(db_complete2, train, by = 'id') #~303 row

#######Algorithm###########

control <- rpart.control(cp = 0.007)
train$res <- as.factor(train$res)
tree <- rpart(res ~Tournament+ Surface + J1Rank + J2Rank + J1Pts + J2Pts
              + DRank + DPts + Dset1 + Dset2 + Dset3, data = train, control = control, parms = list(split="gini"))

#graph of the tree
#rpart.plot(tree, tweak = 1)

#######RESULTS##########

#accuracy of the model
predtrain <- predict(tree, train, type = c("class"))
results <- train$res
mat <- table(predtrain, results)
accuracytrain <- round(((mat[1,1]+mat[2,2])/(length(predtrain))), 3)
accuracytrain

#accuracy of the predictions on the test dataset
pred_test <- predict(tree, test, type = c("class"))
result_test <- test$res
mat_test <- table(pred_test, result_test)
accuracy_test <- ((mat_test[1,1]+mat_test[2,2])/length(pred_test))
round(accuracy_test, 3)

#Test model and its accuracy with switched dataset (player P1 is now P2 and vice versa)
pred_test2 <- predict(tree, test2, type = c("class"))
length(which(pred_test == pred_test2))
pred_test_final <- pred_test[-which(pred_test==pred_test2)]
results_final <- result_test[-which(pred_test==pred_test2)]
table_final <- table(pred_test_final, results_final)
accuracy_final <- ((table_final[1,1]+table_final[2,2])/(length(pred_test_final)))
round(accuracy_final, 3)


#test which prediction is the same regardless of which player is player1 or player2 
a <- pred_test
a2 <- pred_test2
same <- rep(99, length(a))
for(i in 1:length(a)){
  if(a[i]==a2[i]){
    same[i] = 1
  }
  else{
    same[i]= 0
  }
}
gain=rep(99,nrow(test))

#compute the net gain if we did bet on the outcomes the model predicted 
#(if and only if the prediction was the same whether a player was player 1 or 2) 
mise=1
a=pred_test
b=test$res
for(i in 1:nrow(test)){
  if(a[i]==b[i]&&b[i]=="P1"&&same[i]==0){
    gain[i]=(test[i,"PSJ1"]-1)*mise #we take the pinnacle odds as baseline
  }
  else if(a[i]==b[i]&&b[i]=="P1"&&same[i]==1){
    gain[i]=0
  }
  else if(a[i]==b[i]&&b[i]=="P2"&&same[i]==0){
    gain[i]=(test[i,"PSJ2"]-1)*mise
  }
  else if(a[i]==b[i]&&b[i]=="P2"&&same[i]==1){
    gain[i]=0
  }
  else if(a[i]!=b[i]&&same[i]==1){
    gain[i]=0
  }
  else if(a[i]!=b[i]&&same[i]==0){
    gain[i]=-mise
  }
}
#round(gain,2)
sum(gain)

