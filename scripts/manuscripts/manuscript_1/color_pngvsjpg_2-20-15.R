
library(gridExtra)
library(ggplot2)
library(lubridate)
```

#Load data PNG and JPG data
  
dir<-"~/Desktop/r/"
setwd(dir)

# Planting date
planting_date = as.POSIXct("2013-11-26")

green1<-read.table("vis_signal_green_10-20-2014_19:23:58.txt", sep=',', header=TRUE)
blue1<-read.table("vis_signal_blue_10-20-2014_19:23:58.txt", sep=',', header=TRUE)
red1<-read.table("vis_signal_red_10-20-2014_19:23:58.txt",sep=',', header=TRUE)

green_jpg<-read.table("vis_signal_green_11-18-2014_12:59:18-jpg.txt", sep=',', header=TRUE)
blue_jpg<-read.table("vis_signal_blue_11-18-2014_12:59:18-jpg.txt", sep=',', header=TRUE)
red_jpg<-read.table("vis_signal_red_11-18-2014_12:59:18-jpg.txt",sep=',', header=TRUE)
```

#Add treatment and genotype columns for png and jpg data, subeset the data to include only 100%FC and 33%FC data
  
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
rgb2_png<-merge(gb1,r, by=c("date_time","frame","barcode", "treatment","genotype", "day"))

green1_jpg<-format_data(green_jpg)
blue1_jpg<-format_data(blue_jpg)
red1_jpg<-format_data(red_jpg)
g1<-as.data.frame(green1_jpg)
b1<-as.data.frame(blue1_jpg)
r1<-as.data.frame(red1_jpg)
gb1_jpg<-merge(g1,b1,by=c("date_time","frame","barcode", "treatment","genotype","day"))
rgb2_jpg<-merge(gb1_jpg,r1, by=c("date_time","frame","barcode", "treatment","genotype", "day"))

png<-rgb2_png[(rgb2_png$treatment==100 |rgb2_png$treatment==33),]
jpg<-rgb2_jpg[(rgb2_jpg$treatment==100 |rgb2_jpg$treatment==33),]


#Format the data for PCA
  
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

#PCA on color data for both JPG and PNG formats
  
png_channel=pca_format(png)
png_data=pca_nonzero(png_channel)
png_pca=go_pca(png_data)
summary(png_pca)

jpg_channel=pca_format(jpg)
jpg_data=pca_nonzero(jpg_channel)
jpg_pca=go_pca(jpg_data)
summary(jpg_pca)

png_scores<-as.data.frame(png_pca$x)
png_scores$datetime=png$date_time

jpg_scores<-as.data.frame(jpg_pca$x)
jpg_scores$datetime=jpg$date_time

rgb2_jpg_png<-merge(jpg_scores,png_scores, by=c("datetime"),suffixes = c(".jpg",".png"))

#Read in the other shape data from pngs and jpgs
  
# Read PNG data
png.data = read.table(file="vis_snapshots.txt",sep="\t",header=TRUE)

# Read JPEG data
jpg.data = read.table(file="vis_snapshots-jpg.txt",sep="\t",header=TRUE)

# Join tables
join.data = merge(png.data, jpg.data, by="datetime",suffixes = c(".png",".jpg"))
join.data = merge(join.data, rgb2_jpg_png, by="datetime")


#Correlation tests and plotting of shape and color data from pngs and jpgs
  
# Biomass
biomass.r = cor.test(x = join.data$sv_area.png, y = join.data$sv_area.jpg)
biomass = ggplot(data=join.data,aes(x=sv_area.png,y=sv_area.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("VIS side-view area PNG") +
  scale_y_continuous("VIS side-view area JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=2e5,y=1e6,r=paste("r =", round(biomass.r$estimate,5))), aes(x, y, label=r),size=4)

# TV area
tv_area.r = cor.test(x = join.data$tv_area.png, y = join.data$tv_area.jpg)
tv_area = ggplot(data=join.data,aes(x=tv_area.png,y=tv_area.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("VIS top-view area PNG") +
  scale_y_continuous("VIS top-view area JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=2e5,y=1e6,r=paste("r =", round(tv_area.r$estimate,5))), aes(x, y, label=r),size=4)

# Height
height.r = cor.test(x = join.data$height_above_bound.png, y = join.data$height_above_bound.jpg)
height = ggplot(data=join.data,aes(x=height_above_bound.png,y=height_above_bound.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("Height PNG") +
  scale_y_continuous("Height JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=20,y=100,r=paste("r =", round(height.r$estimate,5))), aes(x, y, label=r),size=4)

# Solidity
solidity.r = cor.test(x = join.data$solidity.png, y = join.data$solidity.jpg)
solidity = ggplot(data=join.data,aes(x=solidity.png,y=solidity.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("Solidity PNG") +
  scale_y_continuous("Solidity JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=0.3,y=0.9,r=paste("r =", round(solidity.r$estimate,5))), aes(x, y, label=r),size=4)

#Color PC1
pc1.r=cor.test(join.data$PC1.png, join.data$PC1.jpg, method="pearson")
color.pc1 = ggplot(data=join.data,aes(x=join.data$PC1.png,y=join.data$PC1.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("Color PC1 PNG") +
  scale_y_continuous("Color PC2 JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=0,y=40,r=paste("r =", round(pc1.r$estimate,5))), aes(x, y, label=r),size=4)

#Color PC2
pc2.r=cor.test(join.data$PC2.png, join.data$PC2.jpg, method="pearson")
color.pc2 = ggplot(data=join.data,aes(x=join.data$PC2.png,y=join.data$PC2.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("Color PC2 PNG") +
  scale_y_continuous("Color PC2 JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw()+
  geom_text(data=data.frame(x=50,y=0,r=paste("r =", round(pc2.r$estimate,5))), aes(x, y, label=r),size=4)

#Color PC3
pc3.r=cor.test(join.data$PC3.png, join.data$PC3.jpg, method="pearson")
color.pc3 = ggplot(data=join.data,aes(x=join.data$PC3.png,y=join.data$PC3.jpg)) +
  geom_point(size=1) +
  scale_x_continuous("Color PC3 PNG") +
  scale_y_continuous("Color PC3 JPEG") +
  stat_smooth(method="lm", se=FALSE)+
  theme_bw() +
  geom_text(data=data.frame(x=15,y=20,r=paste("r =", round(pc3.r$estimate,5))), aes(x, y, label=r),size=4)

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

multiplot(biomass,tv_area,height,color.pc1,color.pc2,color.pc3,cols=2)
