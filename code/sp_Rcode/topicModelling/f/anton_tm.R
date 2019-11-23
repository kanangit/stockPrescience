# when it asks if you want compilation, say n
install.packages("stm")
#install.packages("devtools")

#devtools::install_github("mikajoh/stmprinter")

#from https://github.com/wesslen/Topic-Modeling-Workshop-with-R
#packages <- c("quanteda","tidyverse","topicmodels","stm","RColorBrewer","servr", 
              "LDAvis", "RJSONIO", "igraph","visNetwork")

#lapply(packages, install.packages(packages), character.only = TRUE)


library(stm)
#library(stmprinter)

#set working directory
setwd("/Users/kananovichv/Desktop/anton/")

#load the data
lexisall <- read.csv("all.csv",header = TRUE)

#pre-process text 
processed<-textProcessor(documents=lexisall$V5,metadata=lexisall)
meta<-processed$meta
vocab<-processed$vocab
docs<-processed$documents
out <- prepDocuments(docs,vocab,meta)

#use prep documents. 
docs<-out$documents 
vocab<-out$vocab
meta <-out$meta

#set random seed
set.seed(02138)

#lda with k=10
mod10all <-
  selectModel(
    docs,
    vocab,
    K = 10,
    data = meta,
    max.em.its = 1000,
    init.type = "LDA",
    runs = 10
  )

#lda with k=5
mod5all <-
  selectModel(
    docs,
    vocab,
    K = 5,
    data = meta,
    max.em.its = 1000,
    init.type = "LDA",
    runs = 5
  )

#lda with k=20
mod20all <-
  selectModel(
    docs,
    vocab,
    K = 20,
    data = meta,
    max.em.its = 1000,
    init.type = "LDA",
    runs = 10
  )

##compare topic labels
#get topic labels
labelTopics(mod10all$runout[[1]], topics=NULL, n = 10, frexweight = 0.5)
labelTopics(mod10all$runout[[2]], topics=NULL, n = 10, frexweight = 0.5)
labelTopics(mod15all$runout[[1]], topics=NULL, n = 10, frexweight = 0.5)
labelTopics(mod15all$runout[[2]], topics=NULL, n = 10, frexweight = 0.5)
labelTopics(mod20all$runout[[1]], topics=NULL, n = 10, frexweight = 0.5)
labelTopics(mod20all$runout[[2]], topics=NULL, n = 10, frexweight = 0.5)

# mean numbers for semantic coherence 
mean(mod10all$semcoh[[1]])
mean(mod10all$semcoh[[2]])
mean(mod15all$semcoh[[1]])
mean(mod15all$semcoh[[2]])
mean(mod20all$semcoh[[1]])
mean(mod20all$semcoh[[2]])

# mean numbers for exclusivity
mean(mod10all$exclusivity[[1]])
mean(mod10all$exclusivity[[2]])
mean(mod15all$exclusivity[[1]])
mean(mod15all$exclusivity[[2]])
mean(mod20all$exclusivity[[1]])
mean(mod20all$exclusivity[[2]])

##compare semantic coherence and exclusivity
#plot - we have 1 and 2 - those are two runouts
plotModels(mod10all)
plotModels(mod5all)
plotModels(mod20all)

# VK: analyse within topics:
topicQuality(mod10all$runout[[1]],docs)

#get topic thoughts - the most representative text on that topic
findThoughts(mod10all$runout[[1]], topics = c(1), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(2), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(3), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(4), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(5), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(6), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(7), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(8), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(9), texts = lexisall$V5)
findThoughts(mod10all$runout[[1]], topics = c(10), texts = lexisall$V5)

#save proportions of topics in each text in the corpus in a csv file
write.csv(mod5all$runout[[1]]$theta,"proportionsall5.csv",row.names=FALSE)