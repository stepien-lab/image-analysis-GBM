library(dplyr)
library(ggplot2)
library(tibble)

ABM <- read.csv("~/Desktop/Cross_PCF_ABM_Cancer Cells_MDSCs.csv")
ABM_CM <- subset(ABM, select = -c(X, MDSCsCancer.Cells, r, r2) )

CM1 <- read.csv("~/Desktop/CM1.csv")
CM2 <- read.csv("~/Desktop/CM2.csv")
CM3 <- read.csv("~/Desktop/CM3.csv")

CM <- cbind(CM1, CM2, CM3)
names(CM)[1] <- "t1"
names(CM)[2] <- "t2"
names(CM)[3] <- "t3"

cor(CM)
lmod <- lm(t1~., data=CM)
summary(lmod)

ABM_CM <- cbind(CM, ABM_CM)
names(ABM_CM)[4] <- "model"

cor(ABM_CM)
lmod2 <- lm(model~.,data=ABM_CM)
summary(lmod2)
