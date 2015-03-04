library(ggplot2)
library(pls)

dir<-"~/Desktop/r/"
setwd(dir)


#Set the planting date
  
# Planting date
planting_date = as.POSIXct("2013-11-26")

#Read in the R,G,B color data and merge the tables

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

#Read in the shapes data and merge it with the RGB data
  
shapes_table<-read.table("vis_snapshots.txt",sep='\t', header=TRUE)
shapes_table$barcode=shapes_table$plant_id
shapes_table$date_time=shapes_table$datetime

rgb_shapes<-merge(rgb2,shapes_table,by=c("date_time","barcode"))
rgb_shapes$day=as.integer(rgb_shapes$day)

#Subset the shape-RGB data
  
#Day 6 and 7 of the experiment is day 17 and 18 after planting
day17_18<-rgb_shapes[(rgb_shapes$treatment==100|rgb_shapes$treatment==33)& (rgb_shapes$genotype=='A10') & (rgb_shapes$day==6 |rgb_shapes$day==7),]
#Day 14 and 15 of the experiment is day 14 and 15 after planting
day25_26<-rgb_shapes[(rgb_shapes$treatment==100|rgb_shapes$treatment==33)& (rgb_shapes$genotype=='A10') & (rgb_shapes$day==14 |rgb_shapes$day==15),]


#Format the RGB data for PCA
  
pca_format=function(data){
  data_sub=subset(data, select=-c(extent_x, extent_y,day,frame,barcode,genotype,treatment,date_time,plant_id,datetime,sv_area,tv_area,solidity,perimeter,centroid_x,centroid_y,longest_axis,height_above_bound,height_below_bound,above_bound_area, percent_above_bound_area,below_bound_area,percent_below_bound_area,outlier,boundary_line))
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


#PCA on 17-18 DAP RGB Data
  
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

cor.test(day17_18_scores$treatment, day17_18_scores$PC2, method="spearman")

rgb17_18_treatment<-data.frame(rgb=I(as.matrix(day17_18_channel)),treatment=day17_18$treatment,genotype=day17_18$genotype,date_time=day17_18$date_time, day=day17_18$day)
a10_17_18_treatment<-pcr(treatment~rgb,data=rgb17_18_treatment)
summary(a10_17_18_treatment)

plot1<-ggplot(day17_18_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="RGB: 17 to 18 DAP", y= "PC2 (17.77%)", x="PC1(46.94%)")

plot2 <- ggplot(day17_18_scores,aes(x=factor(treatment),y=PC1, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="RGB: A10 Day 17 to Day 18", y= "PC1", x="Treatment")


#PCA on 25-26 DAP RGB data
  
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

cor.test(day25_26_scores$treatment, day25_26_scores$PC2, method="spearman")

a10_25_26_treatment<-pcr(treatment~rgb,data=rgb25_26_shape)
summary(a10_25_26_treatment)


#Plot 17-18 DAP and 25-26 DAP RGB data for A10

#This is Figure 6 in the main text of the paper. Figure 6 is reproduced here so that comparisons can be made between RGB, HSV, and LAB color-space below.
  
plot4<-ggplot(day25_26_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="RGB: A10 Day 25 to Day 26", y= "PC2 (15.98%)", x="PC1(65.06%)")

plot5 <- ggplot(day25_26_scores,aes(x=factor(treatment),y=PC2, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="RGB: A10 Day 25 to Day 26", y= "PC2", x="Treatment")

############ Graph all the  Scatter Plots ##############

library(gridExtra)
grid.arrange(plot1, plot2,ncol=2)
grid.arrange(plot4,plot5,ncol=2)

ggsave(plot1, file="RGB_earlylate_plot1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot2, file="RGB_earlylate_plot2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot4, file="RGB_earlylate_plot3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot5, file="RGB_earlylate_plot4.pdf", width=5, height=5, units="in", useDingbats=FALSE)


#Format data for eigen vectors and plot eigen vector
  
day17_18_table = as.data.frame(day17_18_pca$rotation)
day17_18_table$explanatory_variables = rownames(day17_18_table)
day17_18_table$number<-NA
countrow=nrow(day17_18_table)
number<- seq(from = 1, to = countrow, by = 1)
day17_18_table$number<-as.data.frame(number)

day25_26_table = as.data.frame(day25_26_pca$rotation)
day25_26_table$explanatory_variables = rownames(day25_26_table)
day25_26_table$number<-NA
countrow1=nrow(day25_26_table)
number1<- seq(from = 1, to = countrow1, by = 1)
day25_26_table$number<-as.data.frame(number1)

eigen1=day17_18_table
eigen2=day25_26_table

eigen1_sub=subset(eigen1, select=c(number,explanatory_variables,PC1,PC2))
eigen1_sub$color<-NA
eigen1_sub$color[grep("green", eigen1_sub$explanatory_variables)] <-"green"
eigen1_sub$color[grep("red", eigen1_sub$explanatory_variables)] <- "red"
eigen1_sub$color[grep("blue", eigen1_sub$explanatory_variables)] <- "blue"

label1_bin<-c(as.list(as.character(eigen1_sub$explanatory_variables)))
count_label1=nrow(eigen1_sub$number)
number1_bins<-c(as.list(seq(from=1, to= count_label1, 1)))
label1_skip<-label1_bin[seq(1, length(label1_bin), 20)]
number1_skip<- number1_bins[seq(1, length(number1_bins), 20)]

eigen2_sub=subset(eigen2, select=c(number,explanatory_variables,PC1,PC2))
eigen2_sub$color<-NA
eigen2_sub$color[grep("green", eigen2_sub$explanatory_variables)] <-"green"
eigen2_sub$color[grep("red", eigen2_sub$explanatory_variables)] <- "red"
eigen2_sub$color[grep("blue", eigen2_sub$explanatory_variables)] <- "blue"

label2_bin<-c(as.list(as.character(eigen2_sub$explanatory_variables)))
count_label2=nrow(eigen2_sub$number)
number2_bins<-c(as.list(seq(from=1, to= count_label2, 1)))
label2_skip<-label2_bin[seq(1, length(label2_bin), 20)]
number2_skip<- number2_bins[seq(1, length(number2_bins), 20)]

plot6<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot7<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), eigen2_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

plot8<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot9<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), y=eigen2_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("blue","green","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

ggsave(plot6, file="RGB_earlylate_eigen1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot7, file="RGB_earlylate_eigen2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot8, file="RGB_earlylate_eigen3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot9, file="RGB_earlylate_eigen4.pdf", width=5, height=5, units="in", useDingbats=FALSE)

#Read in the HSV data
  
hue1<-read.table("vis_signal_hue_02-10-2015_16:41:15.txt", sep=',', header=TRUE)
saturation1<-read.table("vis_signal_saturation_02-10-2015_16:41:15.txt", sep=',', header=TRUE)
value1<-read.table("vis_signal_value_02-10-2015_16:41:15.txt",sep=',', header=TRUE)

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

hue1<-format_data(hue1)
saturation1<-format_data(saturation1)
value1<-format_data(value1)
h<-as.data.frame(hue1)
s<-as.data.frame(saturation1)
v<-as.data.frame(value1)
hs1<-merge(h,s,by=c("date_time","frame","barcode", "treatment","genotype","day"))
hsv2<-merge(hs1,v, by=c("date_time","frame","barcode", "treatment","genotype", "day"))
hsv1=subset(hsv2, select=-c(day, date_time, frame, barcode, treatment, genotype))

hsv_data<-data.frame(hsv2=I(as.matrix(hsv1)),treatment=hsv2$treatment,genotype=hsv2$genotype,date_time=hsv2$date_time, day=as.integer(hsv2$day))


#Read in the shapes data and merge it with the HSV data
  
shapes_table<-read.table("vis_snapshots.txt",sep='\t', header=TRUE)
shapes_table$barcode=shapes_table$plant_id
shapes_table$date_time=shapes_table$datetime

hsv_shapes<-merge(hsv2,shapes_table,by=c("date_time","barcode"))
hsv_shapes$day=as.integer(hsv_shapes$day)

#Subset the shape-HSV data
  
#Day 6 and 7 of the experiment is day 17 and 18 after planting
hsv_day17_18<-hsv_shapes[(hsv_shapes$treatment==100|hsv_shapes$treatment==33)& (hsv_shapes$genotype=='A10') & (hsv_shapes$day==6 |hsv_shapes$day==7),]
#Day 14 and 15 of the experiment is day 14 and 15 after planting
hsv_day25_26<-hsv_shapes[(hsv_shapes$treatment==100|hsv_shapes$treatment==33)& (hsv_shapes$genotype=='A10') & (hsv_shapes$day==14 |hsv_shapes$day==15),]


#PCA on 17-18 DAP HSV data
  
hsv_day17_18_channel=pca_format(hsv_day17_18)
hsv_day17_18_data=pca_nonzero(hsv_day17_18_channel)
hsv_day17_18_pca=go_pca(hsv_day17_18_data)
summary(hsv_day17_18_pca)

hsv_day17_18_scores<-as.data.frame(hsv_day17_18_pca$x)
hsv_day17_18_scores$treatment=hsv_day17_18$treatment
hsv_day17_18_scores$genotype=hsv_day17_18$genotype
hsv_day17_18_scores$date_time=hsv_day17_18$date_time
hsv_day17_18_scores$day=hsv_day17_18$day
hsv_day17_18_scores$barcode=hsv_day17_18$barcode
hsv_day17_18_scores$sv_area=hsv_day17_18$sv_area
hsv_day17_18_scores$height_above_bound=hsv_day17_18$height_above_bound

cor.test(hsv_day17_18_scores$treatment, hsv_day17_18_scores$PC1, method="spearman")

cor.test(hsv_day17_18_scores$treatment, hsv_day17_18_scores$PC2, method="spearman")

hsv17_18_treatment<-data.frame(hsv=I(as.matrix(hsv_day17_18_channel)),treatment=hsv_day17_18$treatment,genotype=hsv_day17_18$genotype,date_time=hsv_day17_18$date_time, day=hsv_day17_18$day)
hsv_a10_17_18_treatment<-pcr(treatment~hsv,data=hsv17_18_treatment)
summary(hsv_a10_17_18_treatment)

plot1<-ggplot(hsv_day17_18_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="HSV: 17 to 18 DAP", y= "PC2 (23.38%)", x="PC1(29.94%)")

plot2 <- ggplot(hsv_day17_18_scores,aes(x=factor(treatment),y=PC1, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="HSV: A10 Day 17 to Day 18", y= "PC1", x="Treatment")


#PCA on 25-16 DAP HSV data
  
############# Day  25 and 26 after planting for A10 ###############

hsv_day25_26_channel=pca_format(hsv_day25_26)
hsv_day25_26_data=pca_nonzero(hsv_day25_26_channel)
hsv_day25_26_pca=go_pca(hsv_day25_26_data)
summary(hsv_day25_26_pca)

hsv_day25_26_scores<-as.data.frame(hsv_day25_26_pca$x)
hsv_day25_26_scores$treatment=hsv_day25_26$treatment
hsv_day25_26_scores$genotype=hsv_day25_26$genotype
hsv_day25_26_scores$date_time=hsv_day25_26$date_time
hsv_day25_26_scores$day=hsv_day25_26$day
hsv_day25_26_scores$barcode=hsv_day25_26$barcode
hsv_day25_26_scores$sv_area=hsv_day25_26$sv_area
hsv_day25_26_scores$height_above_bound=hsv_day25_26$height_above_bound

cor.test(hsv_day25_26_scores$treatment, hsv_day25_26_scores$PC1, method="spearman")

cor.test(hsv_day25_26_scores$treatment, hsv_day25_26_scores$PC2, method="spearman")

hsv_25_26_shape<-data.frame(hsv=I(as.matrix(hsv_day25_26_channel)),treatment=hsv_day25_26$treatment,genotype=hsv_day25_26$genotype,date_time=hsv_day25_26$date_time, day=hsv_day25_26$day, sv_area=hsv_day25_26$sv_area)
hsv_a10_25_26_treatment<-pcr(treatment~hsv,data=hsv_25_26_shape)
summary(hsv_a10_25_26_treatment)


#Plot 17-18 DAP and 25-26 DAP HSV data for A10

#The interpretation of HSV results is consistent with RGB data. Color 25-26 DAP can be used to distinguish watering treatments but is not an earlier indication of water limitation than biomass 17-18 DAP
  
plot4<-ggplot(hsv_day25_26_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="HSV: A10 Day 25 to Day 26", y= "PC2 (31.71%)", x="PC1(44.54%)")

plot5 <- ggplot(hsv_day25_26_scores,aes(x=factor(treatment),y=PC2, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="HSV: A10 Day 25 to Day 26", y= "PC2", x="Treatment")

############ Graph all the  Scatter Plots ##############

library(gridExtra)
grid.arrange(plot1, plot2,ncol=2)
grid.arrange(plot4,plot5,ncol=2)

ggsave(plot1, file="hsv_earlylate_plot1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot2, file="hsv_earlylate_plot2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot4, file="hsv_earlylate_plot3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot5, file="hsv_earlylate_plot4.pdf", width=5, height=5, units="in", useDingbats=FALSE)

write.table(hsv_day17_18_pca$rotation, file="a10_hsv17_18_eigen.txt",quote=FALSE,sep='\t')
write.table(hsv_day25_26_pca$rotation, file="a10_hsv25_26_eigen.txt",quote=FALSE,sep='\t')


#Format data for eigen vectors and plot eigen vector
  
day17_18_table = as.data.frame(hsv_day17_18_pca$rotation)
day17_18_table$explanatory_variables = rownames(day17_18_table)
day17_18_table$number<-NA
countrow=nrow(day17_18_table)
number<- seq(from = 1, to = countrow, by = 1)
day17_18_table$number<-as.data.frame(number)

day25_26_table = as.data.frame(hsv_day25_26_pca$rotation)
day25_26_table$explanatory_variables = rownames(day25_26_table)
day25_26_table$number<-NA
countrow1=nrow(day25_26_table)
number1<- seq(from = 1, to = countrow1, by = 1)
day25_26_table$number<-as.data.frame(number1)

eigen1=day17_18_table
eigen2=day25_26_table

eigen1_sub=subset(eigen1, select=c(number,explanatory_variables,PC1,PC2))
eigen1_sub$color<-NA
eigen1_sub$color[grep("hue", eigen1_sub$explanatory_variables)] <-"hue"
eigen1_sub$color[grep("saturation", eigen1_sub$explanatory_variables)] <- "saturation"
eigen1_sub$color[grep("value", eigen1_sub$explanatory_variables)] <- "value"

label1_bin<-c(as.list(as.character(eigen1_sub$explanatory_variables)))
count_label1=nrow(eigen1_sub$number)
number1_bins<-c(as.list(seq(from=1, to= count_label1, 1)))
label1_skip<-label1_bin[seq(1, length(label1_bin), 20)]
number1_skip<- number1_bins[seq(1, length(number1_bins), 20)]

eigen2_sub=subset(eigen2, select=c(number,explanatory_variables,PC1,PC2))
eigen2_sub$color<-NA
eigen2_sub$color[grep("hue", eigen2_sub$explanatory_variables)] <-"hue"
eigen2_sub$color[grep("saturation", eigen2_sub$explanatory_variables)] <- "saturation"
eigen2_sub$color[grep("value", eigen2_sub$explanatory_variables)] <- "value"

label2_bin<-c(as.list(as.character(eigen2_sub$explanatory_variables)))
count_label2=nrow(eigen2_sub$number)
number2_bins<-c(as.list(seq(from=1, to= count_label2, 1)))
label2_skip<-label2_bin[seq(1, length(label2_bin), 20)]
number2_skip<- number2_bins[seq(1, length(number2_bins), 20)]

plot6<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("green","blue","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot7<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), eigen2_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("green","blue","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

plot8<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("green","blue","red"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot9<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), y=eigen2_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("green","blue","red"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

ggsave(plot6, file="hsv_earlylate_eigen1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot7, file="hsv_earlylate_eigen2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot8, file="hsv_earlylate_eigen3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot9, file="hsv_earlylate_eigen4.pdf", width=5, height=5, units="in", useDingbats=FALSE)


#PC1 and PC2 correlation between RGB and HSV

cor.test(day17_18_scores$PC1, hsv_day17_18_scores$PC1, method="spearman")
cor.test(day17_18_scores$PC2, hsv_day17_18_scores$PC2, method="spearman")

cor.test(day25_26_scores$PC1, hsv_day25_26_scores$PC1, method="spearman")
cor.test(day25_26_scores$PC2, hsv_day25_26_scores$PC2, method="spearman")

#Read in the LAB data
  
lightness1<-read.table("vis_signal_lightness_02-10-2015_16:49:44.txt", sep=',', header=TRUE)
gm1<-read.table("vis_signal_green-magenta_02-10-2015_16:49:44.txt", sep=',', header=TRUE)
by1<-read.table("vis_signal_blue-yellow_02-10-2015_16:49:44.txt",sep=',', header=TRUE)

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

lightness1<-format_data(lightness1)
gm1<-format_data(gm1)
by1<-format_data(by1)
l<-as.data.frame(lightness1)
gm<-as.data.frame(gm1)
by<-as.data.frame(by1)
la1<-merge(l,gm,by=c("date_time","frame","barcode", "treatment","genotype","day"))
lab2<-merge(la1,by, by=c("date_time","frame","barcode", "treatment","genotype", "day"))
lab1=subset(lab2, select=-c(day, date_time, frame, barcode, treatment, genotype))

lab_data<-data.frame(lab2=I(as.matrix(lab1)),treatment=lab2$treatment,genotype=lab2$genotype,date_time=lab2$date_time, day=as.integer(lab2$day))


#Read in the shapes data and merge it with the LAB data
  
shapes_table<-read.table("vis_snapshots.txt",sep='\t', header=TRUE)
shapes_table$barcode=shapes_table$plant_id
shapes_table$date_time=shapes_table$datetime

lab_shapes<-merge(lab2,shapes_table,by=c("date_time","barcode"))
lab_shapes$day=as.integer(lab_shapes$day)

#Subset the shape-LAB data
  
#Day 6 and 7 of the experiment is day 17 and 18 after planting
lab_day17_18<-lab_shapes[(lab_shapes$treatment==100|lab_shapes$treatment==33)& (lab_shapes$genotype=='A10') & (lab_shapes$day==6 |lab_shapes$day==7),]
#Day 14 and 15 of the experiment is day 14 and 15 after planting
lab_day25_26<-lab_shapes[(lab_shapes$treatment==100|lab_shapes$treatment==33)& (lab_shapes$genotype=='A10') & (lab_shapes$day==14 |lab_shapes$day==15),]

#PCA on 17-18 DAP LAB data
  
lab_day17_18_channel=pca_format(lab_day17_18)
lab_day17_18_data=pca_nonzero(lab_day17_18_channel)
lab_day17_18_pca=go_pca(lab_day17_18_data)
summary(lab_day17_18_pca)

lab_day17_18_scores<-as.data.frame(lab_day17_18_pca$x)
lab_day17_18_scores$treatment=lab_day17_18$treatment
lab_day17_18_scores$genotype=lab_day17_18$genotype
lab_day17_18_scores$date_time=lab_day17_18$date_time
lab_day17_18_scores$day=lab_day17_18$day
lab_day17_18_scores$barcode=lab_day17_18$barcode
lab_day17_18_scores$sv_area=lab_day17_18$sv_area
lab_day17_18_scores$height_above_bound=lab_day17_18$height_above_bound

cor.test(lab_day17_18_scores$treatment, lab_day17_18_scores$PC1, method="spearman")

cor.test(lab_day17_18_scores$treatment, lab_day17_18_scores$PC2, method="spearman")

lab17_18_treatment<-data.frame(lab=I(as.matrix(lab_day17_18_channel)),treatment=lab_day17_18$treatment,genotype=lab_day17_18$genotype,date_time=lab_day17_18$date_time, day=lab_day17_18$day)
lab_a10_17_18_treatment<-pcr(treatment~lab,data=lab17_18_treatment)
summary(lab_a10_17_18_treatment)

plot1<-ggplot(lab_day17_18_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="LAB: 17 to 18 DAP", y= "PC2 (23.30%)", x="PC1(32.85%)")

plot2 <- ggplot(lab_day17_18_scores,aes(x=factor(treatment),y=PC1, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="LAB: A10 Day 17 to Day 18", y= "PC1", x="Treatment")


#PCA on 25-26 DAP HSV data
  
############# Day  25 and 26 after planting for A10 ###############

lab_day25_26_channel=pca_format(lab_day25_26)
lab_day25_26_data=pca_nonzero(lab_day25_26_channel)
lab_day25_26_pca=go_pca(lab_day25_26_data)
summary(lab_day25_26_pca)

lab_day25_26_scores<-as.data.frame(lab_day25_26_pca$x)
lab_day25_26_scores$treatment=lab_day25_26$treatment
lab_day25_26_scores$genotype=lab_day25_26$genotype
lab_day25_26_scores$date_time=lab_day25_26$date_time
lab_day25_26_scores$day=lab_day25_26$day
lab_day25_26_scores$barcode=lab_day25_26$barcode
lab_day25_26_scores$sv_area=lab_day25_26$sv_area
lab_day25_26_scores$height_above_bound=lab_day25_26$height_above_bound

cor.test(lab_day25_26_scores$treatment, lab_day25_26_scores$PC1, method="spearman")

cor.test(lab_day25_26_scores$treatment, lab_day25_26_scores$PC2, method="spearman")

lab_25_26_shape<-data.frame(lab=I(as.matrix(lab_day25_26_channel)),treatment=lab_day25_26$treatment,genotype=lab_day25_26$genotype,date_time=lab_day25_26$date_time, day=lab_day25_26$day, sv_area=lab_day25_26$sv_area)
lab_a10_25_26_treatment<-pcr(treatment~lab,data=lab_25_26_shape)
summary(lab_a10_25_26_treatment)


#Plot 17-18 DAP and 25-26 DAP LAB data for A10

#The interpretation of LAB results is consistent with RGB data. Color 25-26 DAP can be used to distinguish watering treatments but is not an earlier indication of water limitation than biomass 17-18 DAP
  
plot4<-ggplot(lab_day25_26_scores,aes(x=PC1,y=PC2, color=factor(treatment)))+
  geom_point(size=4)+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="LAB: A10 Day 25 to Day 26", y= "PC2 (16.15%)", x="PC1(56.02%)")

plot5 <- ggplot(lab_day25_26_scores,aes(x=factor(treatment),y=PC2, color=factor(treatment)))+
  geom_boxplot(size=1)+
  geom_jitter()+
  theme_bw()+
  theme(legend.position="top")+
  labs(title="LAB: A10 Day 25 to Day 26", y= "PC2", x="Treatment")

############ Graph all the  Scatter Plots ##############

library(gridExtra)
grid.arrange(plot1, plot2,ncol=2)
grid.arrange(plot4,plot5,ncol=2)

ggsave(plot1, file="lab_earlylate_plot1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot2, file="lab_earlylate_plot2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot4, file="lab_earlylate_plot3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot5, file="lab_earlylate_plot4.pdf", width=5, height=5, units="in", useDingbats=FALSE)


#Format data for eigen vectors and plot eigen vector
  
day17_18_table = as.data.frame(lab_day17_18_pca$rotation)
day17_18_table$explanatory_variables = rownames(day17_18_table)
day17_18_table$number<-NA
countrow=nrow(day17_18_table)
number<- seq(from = 1, to = countrow, by = 1)
day17_18_table$number<-as.data.frame(number)

day25_26_table = as.data.frame(lab_day25_26_pca$rotation)
day25_26_table$explanatory_variables = rownames(day25_26_table)
day25_26_table$number<-NA
countrow1=nrow(day25_26_table)
number1<- seq(from = 1, to = countrow1, by = 1)
day25_26_table$number<-as.data.frame(number1)

eigen1=day17_18_table
eigen2=day25_26_table

eigen1_sub=subset(eigen1, select=c(number,explanatory_variables,PC1,PC2))
eigen1_sub$color<-NA
eigen1_sub$color[grep("lightness", eigen1_sub$explanatory_variables)] <-"lightness"
eigen1_sub$color[grep("green.magenta", eigen1_sub$explanatory_variables)] <- "green.magenta"
eigen1_sub$color[grep("blue.yellow", eigen1_sub$explanatory_variables)] <- "blue.yellow"

label1_bin<-c(as.list(as.character(eigen1_sub$explanatory_variables)))
count_label1=nrow(eigen1_sub$number)
number1_bins<-c(as.list(seq(from=1, to= count_label1, 1)))
label1_skip<-label1_bin[seq(1, length(label1_bin), 20)]
number1_skip<- number1_bins[seq(1, length(number1_bins), 20)]

eigen2_sub=subset(eigen2, select=c(number,explanatory_variables,PC1,PC2))
eigen2_sub$color<-NA
eigen2_sub$color[grep("lightness", eigen2_sub$explanatory_variables)] <-"lightness"
eigen2_sub$color[grep("green.magenta", eigen2_sub$explanatory_variables)] <- "green.magenta"
eigen2_sub$color[grep("blue.yellow", eigen2_sub$explanatory_variables)] <- "blue.yellow"

label2_bin<-c(as.list(as.character(eigen2_sub$explanatory_variables)))
count_label2=nrow(eigen2_sub$number)
number2_bins<-c(as.list(seq(from=1, to= count_label2, 1)))
label2_skip<-label2_bin[seq(1, length(label2_bin), 20)]
number2_skip<- number2_bins[seq(1, length(number2_bins), 20)]

plot6<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("red","blue","green"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot7<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), eigen2_sub$PC1, color=factor(color)))+
  scale_colour_manual(values=c("red","blue","green"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

plot8<-ggplot(eigen1_sub, aes(x=seq(from=1, to= count_label1, 1), y=eigen1_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("red","blue","green"))+
  geom_line()+
  geom_hline(aes(yintercept=0))+
  scale_x_discrete(breaks=number1_skip, labels=label1_skip) +
  theme_bw()+
  theme(text = element_text(size=8),axis.text.x=element_text(angle=90))

plot9<-ggplot(eigen2_sub, aes(x=seq(from=1, to= count_label2, 1), y=eigen2_sub$PC2, color=factor(color)))+
  scale_colour_manual(values=c("red","blue","green"))+  
  geom_line()+
  geom_hline(aes(yintercept=0))+
  theme_bw()+
  scale_x_discrete(breaks=number2_skip, labels=label2_skip)+
  theme(text = element_text(size=8), axis.text.x=element_text(angle=90))

ggsave(plot6, file="lab_earlylate_eigen1.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot7, file="lab_earlylate_eigen2.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot8, file="lab_earlylate_eigen3.pdf", width=5, height=5, units="in", useDingbats=FALSE)
ggsave(plot9, file="lab_earlylate_eigen4.pdf", width=5, height=5, units="in", useDingbats=FALSE)


#PC1 and PC2 correlation between RGB and LAB

cor.test(day17_18_scores$PC1, lab_day17_18_scores$PC1, method="spearman")
cor.test(day17_18_scores$PC2, lab_day17_18_scores$PC2, method="spearman")

cor.test(day25_26_scores$PC1, lab_day25_26_scores$PC1, method="spearman")
cor.test(day25_26_scores$PC2, lab_day25_26_scores$PC2, method="spearman")




