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
rgb1=subset(rgb2, select=-c(day, date_time, frame, barcode, treatment, genotype))

rgb_data<-data.frame(rgb2=I(as.matrix(rgb1)),treatment=rgb2$treatment,genotype=rgb2$genotype,date_time=rgb2$date_time, day=as.integer(rgb2$day))

library(pls)

a10_17_18_pcr<-pcr(treatment~rgb2,data=rgb_data[(rgb_data$treatment==100|rgb_data$treatment==33)& (rgb_data$genotype=='A10') & (rgb_data$day==6 |rgb_data$day==7),])
summary(a10_17_18_pcr)

a10_25_26_pcr<-pcr(treatment~rgb2,data=rgb_data[(rgb_data$treatment==100|rgb_data$treatment==33)& (rgb_data$genotype=='A10') & (rgb_data$day==14 |rgb_data$day==15),])
summary(a10_25_26_pcr)

################

shapes_table<-read.table("vis_snapshots.txt",sep='\t', header=TRUE)
shapes_table$barcode=shapes_table$plant_id
shapes_table$date_time=shapes_table$datetime

rgb_shapes<-merge(rgb2,shapes_table,by=c("date_time","barcode"))
rgb_shapes$day=as.integer(rgb_shapes$day)

day17_18<-rgb_shapes[(rgb_shapes$treatment==100|rgb_shapes$treatment==33)& (rgb_shapes$genotype=='A10') & (rgb_shapes$day==6 |rgb_shapes$day==7),]
day25_26<-rgb_shapes[(rgb_shapes$treatment==100|rgb_shapes$treatment==33)& (rgb_shapes$genotype=='A10') & (rgb_shapes$day==14 |rgb_shapes$day==15),]


pca_format=function(data){
  data_sub=subset(data, select=-c(day,frame,barcode,genotype,treatment,date_time,plant_id,datetime,sv_area,tv_area,centroid_height,solidity,perimeter,centroid_x,centroid_y,longest_axis,height_above_bound,height_below_bound,above_bound_area, percent_above_bound_area,below_bound_area,percent_below_bound_area,outlier,boundary_line))
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


############# Day  17 and 18 after planting for A10 ###############

day17_18_channel=pca_format(day17_18)
day17_18_data=pca_nonzero(day17_18_channel)
day17_18_pca=go_pca(day17_18_data)
summary(day17_18_pca)

day17_18_scores<-as.data.frame(day17_18_pca$x)
day17_18_scores$treatment=day17_18$treatment
day17_18_scores$genotype=day17_18$genotype
day17_18_scores$date_time=day17_18$date_time
day17_18_scores$day=day17_18$day
day17_18_scores$barcode=day17_18$barcode
day17_18_scores$sv_area=day17_18$sv_area
day17_18_scores$height_above_bound=day17_18$height_above_bound

cor.test(day17_18_scores$treatment, day17_18_scores$PC1, method="spearman")
cor.test(day17_18_scores$date_time, day17_18_scores$PC1, method="spearman")
cor.test(day17_18_scores$sv_area, day17_18_scores$PC1, method="spearman")
cor.test(day17_18_scores$height_above_bound, day17_18_scores$PC1, method="spearman")

cor.test(day17_18_scores$treatment, day17_18_scores$PC2, method="spearman")
cor.test(day17_18_scores$date_time, day17_18_scores$PC2, method="spearman")
cor.test(day17_18_scores$sv_area, day17_18_scores$PC2, method="spearman")
cor.test(day17_18_scores$height_above_bound, day17_18_scores$PC2, method="spearman")

rgb17_18_biomass<-data.frame(rgb=I(as.matrix(day17_18_channel)),treatment=day17_18$treatment,genotype=day17_18$genotype,date_time=day17_18$date_time, day=day17_18$day, sv_area=day17_18$sv_area)
a10_17_18_biomass<-pcr(sv_area~rgb,data=rgb17_18_biomass)
summary(a10_17_18_biomass)

rgb17_18_height<-data.frame(rgb=I(as.matrix(day17_18_channel)),treatment=day17_18$treatment,genotype=day17_18$genotype,date_time=day17_18$date_time, day=day17_18$day, height_above_bound=day17_18$height_above_bound)
a10_17_18_height<-pcr(height_above_bound~rgb,data=rgb17_18_height)
summary(a10_17_18_height)

rgb17_18_treatment<-data.frame(rgb=I(as.matrix(day17_18_channel)),treatment=day17_18$treatment,genotype=day17_18$genotype,date_time=day17_18$date_time, day=day17_18$day)
a10_17_18_treatment<-pcr(treatment~rgb,data=rgb17_18_treatment)
summary(a10_17_18_treatment)

plot1<-ggplot(day17_18_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position=c(0.5,0.5))+
  labs(title="17 to 18 DAP", y= "PC2 (17.77%)", x="PC1(46.94%)")

plot2 <- ggplot(day17_18_scores,aes(x=factor(treatment),y=PC1, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position=c(0.5,0.5))+
  labs(title="Plant Color: A10 Day 17 to Day 18", y= "PC1", x="Treatment")

############# Day  25 and 26 after planting for A10 ###############

day25_26_channel=pca_format(day25_26)
day25_26_data=pca_nonzero(day25_26_channel)
day25_26_pca=go_pca(day25_26_data)
summary(day25_26_pca)

day25_26_scores<-as.data.frame(day25_26_pca$x)
day25_26_scores$treatment=day25_26$treatment
day25_26_scores$genotype=day25_26$genotype
day25_26_scores$date_time=day25_26$date_time
day25_26_scores$day=day25_26$day
day25_26_scores$barcode=day25_26$barcode
day25_26_scores$sv_area=day25_26$sv_area
day25_26_scores$height_above_bound=day25_26$height_above_bound

cor.test(day25_26_scores$treatment, day25_26_scores$PC1, method="spearman")
cor.test(day25_26_scores$date_time, day25_26_scores$PC1, method="spearman")
cor.test(day25_26_scores$sv_area, day25_26_scores$PC1, method="spearman")
cor.test(day25_26_scores$height_above_bound, day25_26_scores$PC1, method="spearman")

cor.test(day25_26_scores$treatment, day25_26_scores$PC2, method="spearman")
cor.test(day25_26_scores$date_time, day25_26_scores$PC2, method="spearman")
cor.test(day25_26_scores$sv_area, day25_26_scores$PC2, method="spearman")
cor.test(day25_26_scores$height_above_bound, day25_26_scores$PC2, method="spearman")

rgb25_26_shape<-data.frame(rgb=I(as.matrix(day25_26_channel)),treatment=day25_26$treatment,genotype=day25_26$genotype,date_time=day25_26$date_time, day=day25_26$day, sv_area=day25_26$sv_area)
a10_25_26_biomass<-pcr(sv_area~rgb,data=rgb25_26_shape)
summary(a10_25_26_biomass)

a10_25_26_treatment<-pcr(treatment~rgb,data=rgb25_26_shape)
summary(a10_25_26_treatment)

plot4<-ggplot(day25_26_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position=c(0.5,0.5))+
  labs(title="Plant Color: A10 Day 25 to Day 26", y= "PC2 (15.98%)", x="PC1(65.06%)")

plot5 <- ggplot(day25_26_scores,aes(x=factor(treatment),y=PC2, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position=c(0.5,0.5))+
  labs(title="Plant Color: A10 Day 25 to Day 26", y= "PC2", x="Treatment")

############ Graph all the  Scatter Plots ##############

library(gridExtra)
grid.arrange(plot1, plot2,plot4,plot5, nrow=2, ncol=2)

ggsave(plot1, file="plot1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot2, file="plot2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot4, file="plot3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot5, file="plot4.pdf", width=5, height=5, units="in", useDingbats=FALSE)


############ Graph all the Eigen Vectors ##############

write.table(day17_18_pca$rotation, file="a10_rgb17_18_eigen.txt",quote=FALSE,sep='\t')
write.table(day25_26_pca$rotation, file="a10_rgb25_26_eigen.txt",quote=FALSE,sep='\t')

####note: The allday5_eigen.txt file needs to be fixed in 3 ways before it can be graphed:
#### 1) The headers need to be moved one cell over so they are over the right column (the explainatory_variables column is not labelled, so everything gets shifted over one)
#### 2) A header label needs to be added for the explainatory_variables column
#### 3) A number column should be added just to make sure things stay in order and to make the label skipping easier


eigen1<-read.table("a10_rgb17_18_eigen.txt",sep='\t', header=TRUE)
eigen2<-read.table("a10_rgb25_26_eigen.txt",sep='\t', header=TRUE)

eigen1_sub=subset(eigen1, select=c(number,explainatory_variables,PC1,PC2))
eigen1_sub$color<-NA
eigen1_sub$color[grep("green", eigen1_sub$explainatory_variables)] <-"green"
eigen1_sub$color[grep("red", eigen1_sub$explainatory_variables)] <- "red"
eigen1_sub$color[grep("blue", eigen1_sub$explainatory_variables)] <- "blue"

label1_bin<-c(as.list(as.character(eigen1_sub$explainatory_variables)))
number1_bins<-c(as.list(eigen1_sub$number))
label1_skip<- label1_bin[seq(1, length(label1_bin), 20)]
number1_skip<- number1_bins[seq(1, length(number1_bins), 20)]

eigen2_sub=subset(eigen2, select=c(number,explainatory_variables,PC1,PC2))
eigen2_sub$color<-NA
eigen2_sub$color[grep("green", eigen2_sub$explainatory_variables)] <-"green"
eigen2_sub$color[grep("red", eigen2_sub$explainatory_variables)] <- "red"
eigen2_sub$color[grep("blue", eigen2_sub$explainatory_variables)] <- "blue"

label2_bin<-c(as.list(as.character(eigen2_sub$explainatory_variables)))
number2_bins<-c(as.list(eigen2_sub$number))
label2_skip<- label2_bin[seq(1, length(label2_bin), 20)]
number2_skip<- number2_bins[seq(1, length(number2_bins), 20)]

plot7<-ggplot(eigen1_sub, aes(x=number, y=PC1, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot8<-ggplot(eigen2_sub, aes(x=number, y=PC1, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

plot9<-ggplot(eigen1_sub, aes(x=number, y=PC2, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot10<-ggplot(eigen2_sub, aes(x=number, y=PC2, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

grid.arrange(plot7, plot8,plot9,plot10, nrow=2,ncol=2)




