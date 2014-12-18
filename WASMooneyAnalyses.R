library(plyr)
library(dplyr)
library(ggplot2)
library(car)

#Load data
dat <- read.csv("WASMooneyAllVars.csv",header=T)

#Summarise By Mooney
datByMooney <- ddply(dat, c('Name'),summarise,
                                       rt=mean(RT, na.rm=T),
                                       acc=mean(isCorrect, na.rm=T),
                                       conf=mean(Conf, na.rm=T))

write.csv(datByMooney, "WASMooneyByPic.csv",row.names=F)

#CIs Function
getCIs<- function (x,n) {
  binom.test(round(x*n,0),n)$conf.int[1:2]
}

#ORDERING BY FREE NAMING
#vals = dat[ dat$Condition == 'Free Naming',]
#xvals = vals[with(vals, order(-Accuracy)), ]$MooneyName
#dat$mooneyReord <- factor(dat$MooneyName, levels = xvals)

#Compute CIs
CIs = sapply(datByMooney$acc,getCIs,n=20)
limits <- aes(ymin = CIs[1,], ymax=CIs[2,])

#Plot Data
##Style options for the graph
PimpMyPlot <- theme(text=element_text(size=14,family="Helvetica"))+
  theme(axis.line=element_line(colour='black'))+
  theme(axis.text=element_text(colour="black"))+
  theme(panel.grid.major.y=element_line(linetype='dotted',colour='grey50',size=0.3))+
  theme(panel.grid.major.x=element_line(linetype='dashed',colour='grey50',size=0.3))+
  theme(panel.background=element_blank())

ggplot(datByMooney, aes(x=reorder(Name,-acc),y=acc))+
  geom_point(size=3)+
  geom_errorbar(limits,width=.2)+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  labs(x ="Picture",y="Accuracy")+
  #scale_colour_manual(values=c("#e41a1c",'#377eb8'))+
  #scale_y_continuous(expand = c(0,0))+
  #coord_cartesian(ylim=c(0,1))+
  theme(legend.position="none")+
  PimpMyPlot