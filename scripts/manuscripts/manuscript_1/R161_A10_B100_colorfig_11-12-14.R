library(ggplot2)

dir<-"~/Desktop/r/"
setwd(dir)

# Planting date
planting_date = as.POSIXct("2013-11-26")

green1<-read.table("vis_signal_green_10-20-2014_19:23:58.txt", sep=',', header=TRUE)
blue1<-read.table("vis_signal_blue_10-20-2014_19:23:58.txt", sep=',', header=TRUE)
red1<-read.table("vis_signal_red_10-20-2014_19:23:58.txt",sep=',', header=TRUE)

format_data=function(data){
  # Treatment column
  data$treatment <- NA
  data$treatment[grep("AA", data$barcode)] <- 100
  data$treatment[grep("AB", data$barcode)] <- 0
  data$treatment[grep("AC", data$barcode)] <- 0
  data$treatment[grep("AD", data$barcode)] <- 33
  data$treatment[grep("AE", data$barcode)] <- 66
  
  data$genotype <- NA
  data$genotype[grep("p1", data$barcode)] <- 'A10'
  data$genotype[grep("p2", data$barcode)] <- 'B100'
  data$genotype[grep("r1", data$barcode)] <- 'R20'
  data$genotype[grep("r2", data$barcode)] <- 'R70'
  data$genotype[grep("r3", data$barcode)] <- 'R98'
  data$genotype[grep("r4", data$barcode)] <- 'R102'
  data$genotype[grep("r5", data$barcode)] <- 'R128'
  data$genotype[grep("r6", data$barcode)] <- 'R133'
  data$genotype[grep("r7", data$barcode)] <- 'R161'
  data$genotype[grep("r8", data$barcode)] <- 'R187'
  
  data=data[grep('000A',data$barcode, invert=TRUE),]
  
  return(data)
}

green1<-format_data(green1)
blue1<-format_data(blue1)
red1<-format_data(red1)
g<-as.data.frame(green1)
b<-as.data.frame(blue1)
r<-as.data.frame(red1)
gb1<-merge(g,b,by=c("date_time","frame","barcode", "treatment","genotype","day"))
rgb2<-merge(gb1,r, by=c("date_time","frame","barcode", "treatment","genotype", "day"))
rgb1=subset(rgb2, select=-c(day))
rgb1$day=as.integer(rgb2$day) 

allday5=rgb1[(rgb1$day<=1),]

# function to take out the data that isn't going to be used as explainatory variables for PCA
pca_format=function(data){
  data_sub=subset(data, select=-c(day,frame,barcode,genotype,treatment,date_time))
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

allday5_channel=pca_format(allday5)
allday5_data=pca_nonzero(allday5_channel)
allday5_pca=go_pca(allday5_data)

write.table(allday5_pca$rotation, file="allday5_eigen.txt",quote=FALSE,sep='\t')

allday5_scores<-as.data.frame(allday5_pca$x)
allday5_scores$treatment=allday5$treatment
allday5_scores$genotype=allday5$genotype
allday5_scores$date_time=allday5$date_time
allday5_scores$barcode=allday5$barcode

allday5_scores$genotypenum <- NA
allday5_scores$genotypenum[grep("p1", allday5_scores$barcode)] <- 1
allday5_scores$genotypenum[grep("p2", allday5_scores$barcode)] <- 2
allday5_scores$genotypenum[grep("r1", allday5_scores$barcode)] <- 3
allday5_scores$genotypenum[grep("r2", allday5_scores$barcode)] <- 4
allday5_scores$genotypenum[grep("r3", allday5_scores$barcode)] <- 5
allday5_scores$genotypenum[grep("r4", allday5_scores$barcode)] <- 6
allday5_scores$genotypenum[grep("r5", allday5_scores$barcode)] <- 7
allday5_scores$genotypenum[grep("r6", allday5_scores$barcode)] <- 8
allday5_scores$genotypenum[grep("r7", allday5_scores$barcode)] <- 9
allday5_scores$genotypenum[grep("r8", allday5_scores$barcode)] <- 10

geno_sep<-allday5_scores[(allday5_scores$genotype=='A10'|allday5_scores$genotype=='B100'|allday5_scores$genotype=='R161'),]
cor.test(geno_sep$genotypenum, geno_sep$PC1, method="spearman")

rgb_geno<-data.frame(rgb=I(as.matrix(allday5_channel)),genotypenum=allday5_scores$genotypenum)
a10_rgb_geno<-pcr(genotypenum~rgb,data=rgb_geno)
summary(a10_rgb_geno)

plot1<-ggplot(allday5_scores,aes(x=PC1,y=PC2, color=factor(genotype)))+
  scale_colour_manual(values=c("#E69F00", "#808080","#808080","#808080","#808080", "#cc33cc","#808080","#808080","#808080","#808080"))+
  geom_point(size=2)+
  theme_bw()+
  labs(y= "PC2 (12.98%)", x="PC1(40.92%)")

plot2<-ggplot(allday5_scores,aes(x=PC1,y=PC2, color=factor(genotype)))+
  scale_colour_manual(values=c("#808080", "#10ce59","#808080","#808080","#808080", "#cc33cc","#808080","#808080","#808080","#808080"))+
  geom_point(size=2)+
  theme_bw()+
  labs( y= "PC2 (12.98%)", x="PC1(40.92%)")

library(gridExtra)
grid.arrange(plot1, plot2, ncol=2)

summary(allday5_pca)

################# Plot of Eigen Vector #####################

####note: The allday5_eigen.txt file needs to be fixed in 3 ways before it can be graphed:
#### 1) The headers need to be moved one cell over so they are over the right column (the explainatory_variables column is not labelled, so everything gets shifted over one)
#### 2) A header label needs to be added for the explainatory_variables column
#### 3) A number column should be added just to make sure things stay in order and to make the label skipping easier

eigen1<-read.table("allday5_eigen.txt",sep='\t', header=TRUE)

eigen_sub=subset(eigen1, select=c(number,explainatory_variables,PC1,PC2))
eigen_sub$color<-NA
eigen_sub$color[grep("green", eigen_sub$explainatory_variables)] <-"green"
eigen_sub$color[grep("red", eigen_sub$explainatory_variables)] <- "red"
eigen_sub$color[grep("blue", eigen_sub$explainatory_variables)] <- "blue"

label_bin<-c(as.list(as.character(eigen_sub$explainatory_variables)))
number_bins<-c(as.list(eigen_sub$number))
label_skip<- label_bin[seq(1, length(label_bin), 20)]
number_skip<- number_bins[seq(1, length(number_bins), 20)]

plot3<-ggplot(eigen_sub, aes(x=number, y=PC1, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number_skip, labels=label_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot4<-ggplot(eigen_sub, aes(x=number, y=PC2, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number_skip, labels=label_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

grid.arrange(plot3, plot4, nrow=2)

##################