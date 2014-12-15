library(ggplot2)

dir<-"~/Desktop/r/"
setwd(dir)

# Planting date
planting_date = as.POSIXct("2013-11-26")

signal<-read.table("flu_signal_burnin2.sqlite3_10-24-2014_02:05:21.txt", sep=',', header=TRUE)

format_data=function(data){
  # Treatment column
  data$treatment <- NA
  data$treatment[grep("AA", data$plant_id)] <- 100
  data$treatment[grep("AB", data$plant_id)] <- 0
  data$treatment[grep("AC", data$plant_id)] <- 0
  data$treatment[grep("AD", data$plant_id)] <- 33
  data$treatment[grep("AE", data$plant_id)] <- 66
  
  data$genotype <- NA
  data$genotype[grep("p1", data$plant_id)] <- 'A10'
  data$genotype[grep("p2", data$plant_id)] <- 'B100'
  data$genotype[grep("r1", data$plant_id)] <- 'R20'
  data$genotype[grep("r2", data$plant_id)] <- 'R70'
  data$genotype[grep("r3", data$plant_id)] <- 'R98'
  data$genotype[grep("r4", data$plant_id)] <- 'R102'
  data$genotype[grep("r5", data$plant_id)] <- 'R128'
  data$genotype[grep("r6", data$plant_id)] <- 'R133'
  data$genotype[grep("r7", data$plant_id)] <- 'R161'
  data$genotype[grep("r8", data$plant_id)] <- 'R187'
  
  data$day<-NA
  data$day<-as.integer((data$date_time-1385445600)/86400) 
  
  data=data[grep('000A',data$plant_id, invert=TRUE),]
  
  return(data)
}


signal1<-format_data(signal)
signal2<-as.data.frame(signal1)

####################100% Watering Graph#########################

flu100=signal2[signal2$treatment==100 & signal2$genotype=='A10' | signal2$treatment==100 & signal2$genotype=='B100',]

# function to take out the data that isn't going to be used as explainatory variables for PCA
pca_format=function(data){
  data_sub=subset(data, select=-c(plant_id,date_time,peak_bin,median_bin,num_bins,genotype,treatment,day))
  return(data_sub)
}

pca_nonzero=function(data_sub){
  col_sum=colSums(data_sub)
  channel_data=data_sub[,col_sum!=0]
  return(channel_data)
}

go_pca=function(channel_data){
  channel_pca=prcomp(channel_data,center=TRUE, scale=TRUE)
}

flu100_channel=pca_format(flu100)
flu100_data=pca_nonzero(flu100_channel)
flu100_pca=go_pca(flu100_data)

write.table(flu100_pca$rotation, file="flu100_loadings.txt",quote=FALSE,sep='\t')

flu100_scores<-as.data.frame(flu100_pca$x)
flu100_scores$treatment=flu100$treatment
flu100_scores$genotype=flu100$genotype
flu100_scores$date_time=flu100$date_time
flu100_scores$day=flu100$day


plot1 <- ggplot(flu100_scores,aes(x=PC1,y=PC2, color=factor(genotype)))+
  geom_point(size=2)+
  scale_colour_manual(values=c("#cc33cc", "#00cc99"))+
  theme_bw()+
  labs(title="FLU Signal: 100% FC", y= "PC2 (11.29%)", x="PC1(50.99%)")

plot2<-ggplot(flu100_scores,aes(x=PC1,y=PC2, color=(date_time)))+
  scale_colour_gradient(high="orange", low="blue")+
  geom_point(size=2)+
  theme_bw()+
  labs(title="Flu Signal: 100% FC", y= "PC2 (11.29%)", x="PC1(50.99%)")

library(gridExtra)
grid.arrange(plot1, plot2, ncol=2)

####################33% Watering Graph#########################

flu33=signal2[signal2$treatment==33 & signal2$genotype=='A10' | signal2$treatment==33 & signal2$genotype=='B100',]

# function to take out the data that isn't going to be used as explainatory variables for PCA
pca_format=function(data){
  data_sub=subset(data, select=-c(plant_id,date_time,peak_bin,median_bin,num_bins,genotype,treatment,day))
  return(data_sub)
}

pca_nonzero=function(data_sub){
  col_sum=colSums(data_sub)
  channel_data=data_sub[,col_sum!=0]
  return(channel_data)
}

go_pca=function(channel_data){
  channel_pca=prcomp(channel_data,center=TRUE, scale=TRUE)
}

flu33_channel=pca_format(flu33)
flu33_data=pca_nonzero(flu33_channel)
flu33_pca=go_pca(flu33_data)

write.table(flu33_pca$rotation, file="flu33_loadings.txt",quote=FALSE,sep='\t')

flu33_scores<-as.data.frame(flu33_pca$x)
flu33_scores$treatment=flu33$treatment
flu33_scores$genotype=flu33$genotype
flu33_scores$date_time=flu33$date_time
flu33_scores$day=flu33$day


plot1 <- ggplot(flu33_scores,aes(x=PC1,y=PC2, color=factor(genotype)))+
  geom_point(size=2)+
  scale_colour_manual(values=c("#cc33cc", "#00cc99"))+
  theme_bw()+
  labs(title="FlU Signal: 33% FC", y= "PC2 (12.39%)", x="PC1(52.71%)")

plot2<-ggplot(flu33_scores,aes(x=PC1,y=PC2, color=(date_time)))+
  scale_colour_gradient(high="orange", low="blue")+
  geom_point(size=2)+
  theme_bw()+
  labs(title="Flu Signal: 33% FC", y= "PC2 (12.39%)", x="PC1(52.71%)")

library(gridExtra)
grid.arrange(plot1, plot2, ncol=2)


##################All Genotypes first 4 days ##########################

allday4=signal2[(signal2$day<=12) & (signal2$genotype=='A10'|signal2$genotype=='B100'|signal2$genotype=='R161'),]


# function to take out the data that isn't going to be used as explainatory variables for PCA
pca_format=function(data){
  data_sub=subset(data, select=-c(plant_id,date_time,peak_bin,median_bin,num_bins,genotype,treatment,day))
  return(data_sub)
}

pca_nonzero=function(data_sub){
  col_sum=colSums(data_sub)
  channel_data=data_sub[,col_sum!=0]
  return(channel_data)
}

go_pca=function(channel_data){
  channel_pca=prcomp(channel_data,center=TRUE, scale=TRUE)
}

allday4_channel=pca_format(allday4)
allday4_data=pca_nonzero(allday4_channel)
allday4_pca=go_pca(allday4_data)

write.table(allday4_pca$rotation, file="allday4_loadings.txt",quote=FALSE,sep='\t')

allday4_scores<-as.data.frame(allday4_pca$x)
allday4_scores$treatment=allday4$treatment
allday4_scores$plant_id=allday4$plant_id
allday4_scores$genotype=allday4$genotype
allday4_scores$date_time=allday4$date_time
allday4_scores$day=allday4$day
allday4_scores$median=allday4$median_bin


plot1 <- ggplot(allday4_scores,aes(x=PC1,y=PC2, color=factor(genotype)))+
  geom_point(size=2)+
  scale_colour_manual(values=c("#E69F00", "#10ce59", "#cc33cc"))+
  theme_bw()+
  scale_x_continuous(lim=c(-10,20))+
  scale_y_continuous(lim=c(-30,30))+  
  labs( y= "PC2 (17.11%)", x="PC1(24.75%)")+
  theme(legend.background = element_rect(),legend.position=c(.5,.5))

plot5<-ggplot(allday4, aes(factor(genotype), median_bin, color=factor(genotype) ))+
  scale_colour_manual(values=c("#E69F00", "#10ce59", "#cc33cc"))+
  geom_boxplot()+
  scale_y_continuous(lim=c(0.65,0.8))+ 
  theme_bw()+
  theme(legend.background = element_rect(),legend.position=c(0.5,.5))
  
plot1

library(gridExtra)
grid.arrange(plot1, plot5, ncol=2)

eigen1<-read.table("allday4_loadings.txt",sep='\t', header=TRUE)

eigen_sub=subset(eigen1, select=c(number,explainatory_variables,PC1,PC2))

label_bin<-c(as.list(as.character(eigen_sub$explainatory_variables)))
number_bins<-c(as.list(eigen_sub$number))
label_skip<- label_bin[seq(1, length(label_bin), 10)]
number_skip<- number_bins[seq(1, length(number_bins), 10)]

plot3<-ggplot(eigen_sub, aes(x=number, y=PC1))+
  geom_point()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number_skip, labels=label_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot4<-ggplot(eigen_sub, aes(x=number, y=PC2))+
  geom_point()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number_skip, labels=label_skip) +
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

grid.arrange(plot3, plot4, nrow=2)

plot5<-ggplot(allday4, aes(factor(genotype), median_bin ))+
    geom_boxplot()+
    scale_y_continuous(lim=c(0.5,0.8))+ 
    theme_bw()

plot5

box<-boxplot( median_bin~genotype,allday4,plot=FALSE)

box_median=box$stats[3,]

height=c(60.03234836, 50.36523921, 55.50627181, 67.70970796, 99.47041657, 45.0074111, 74.2259854, 92.20594637,73.63765863, 87.35038875)
         
plot(x=box_median,y=height)         
cor.test(x=box_median,y=height)
         
         
height_table<-read.table("vis_snapshots.txt",sep='\t', header=TRUE)
height_table$date_time=height_table$datetime

##########################################

signal_height<-merge(signal2,height_table,by=c("date_time","plant_id")) 
signal100<-signal_height[ (signal_height$treatment==100 |signal_height$treatment==33),]

plot6<-ggplot(signal100,aes(y=height_above_bound, x=median_bin ))+
  geom_point(size=1)+
  theme_bw()+
  stat_smooth(method="lm",formula=y~poly(x,2),se=FALSE, size=1)+
  annotate("text", x = 0.5, y = 5, label = "Spearman Correlation: p-value < 2.2e-16 rho=-0.852")

plot6

cor.test(signal100$height_above_bound, signal100$median_bin, method="spearman")
         
       
############## A10 ##################

flu100=signal2[(signal2$treatment==100 | signal2$treatment==33)& (signal2$genotype=='A10'|signal2$genotype=='B100'|signal2$genotype=='R161'),]

# function to take out the data that isn't going to be used as explainatory variables for PCA
pca_format=function(data){
  data_sub=subset(data, select=-c(plant_id,date_time,peak_bin,median_bin,num_bins,genotype,treatment,day))
  return(data_sub)
}

pca_nonzero=function(data_sub){
  col_sum=colSums(data_sub)
  channel_data=data_sub[,col_sum!=0]
  return(channel_data)
}

go_pca=function(channel_data){
  channel_pca=prcomp(channel_data,center=TRUE, scale=TRUE)
}

flu100_channel=pca_format(flu100)
flu100_data=pca_nonzero(flu100_channel)
flu100_pca=go_pca(flu100_data)

write.table(flu100_pca$rotation, file="flu100_loadings.txt",quote=FALSE,sep='\t')

flu100_scores<-as.data.frame(flu100_pca$x)
flu100_scores$treatment=flu100$treatment
flu100_scores$genotype=flu100$genotype
flu100_scores$date_time=flu100$date_time
flu100_scores$day=flu100$day
flu100_scores$plant_id=flu100$plant_id
flu_height<-merge(flu100_scores,height_table,by=c("date_time","plant_id")) 

plot1 <- ggplot(flu_height,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=2)+
  theme_bw()+
  labs(title="FLU Signal: A10", y= "PC2 (8.966%)", x="PC1(52.68%)")

plot2<-ggplot(flu_height,aes(x=PC1,y=PC2, color=(genotype)))+
  scale_colour_manual(values=c("#E69F00", "#10ce59", "#cc33cc"))+  
  geom_point(size=2)+
  theme_bw()+
  labs(title="Flu Signal: A10", y= "PC2 (8.966%)", x="PC1(52.68%)")

plot3<-ggplot(flu_height,aes(x=PC1,y=PC2, color=(height_above_bound)))+
  scale_colour_gradient(high="orange", low="blue")+
  geom_point(size=2)+
  theme_bw()+
  labs(title="Flu Signal: A10", y= "PC2 (8.966%)", x="PC1(52.68%)")

plot4<-ggplot(flu_height,aes(x=PC1,y=PC2, color=(date_time)))+
  scale_colour_gradient(high="orange", low="blue")+
  geom_point(size=2)+
  theme_bw()+
  labs(title="Flu Signal: A10", y= "PC2 (8.966%)", x="PC1(52.68%)")

library(gridExtra)
grid.arrange(plot1, plot2, plot3, plot4, nrow=2, ncol=2)

library(ggplot2)

dir<-"~/Desktop/r/"
setwd(dir)

fakeplant<-read.table("3dplant_data.txt", sep='\t', header=TRUE)

cor.test(fakeplant$Median_Fv.Fm, fakeplant$Height, method="pearson")

plot1 <- ggplot(fakeplant,aes(x=Median_Fv.Fm,y=Height))+
  geom_point(size=2)+
  stat_smooth(method="lm", se=TRUE)+
  annotate("text",x=0.72, y=1, label="r=-0.976")+
  theme_bw()+
  theme(legend.background = element_rect(),legend.position=c(.5,.5))

plot1