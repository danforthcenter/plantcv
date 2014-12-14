# Script to analyze NIR data
# Written by Max Feldman 12.8.14
# mfeldman@danforthcenter.org

# Load libraries
library(ggplot2)
library(lattice)
library(scales)

###
# Read in all files
###

# Set the working directory to the folder your data is in
setwd("/Users/mfeldman/Desktop/current_phenotyping/burnin2")

# Read in NIR shape files with different zooms
z3500_nir_shape<-read.table("nir_shapes_z3500.txt", sep="\t",header=TRUE)
z2500_nir_shape<-read.table("nir_shapes_z2500.txt", sep="\t",header=TRUE)
z500_nir_shape<-read.table("nir_shapes_z500.txt", sep="\t",header=TRUE)

# Put all zooms into a common dataframe, remove individual files
nir_shape<-rbind(z3500_nir_shape, z2500_nir_shape, z500_nir_shape)
rm(z3500_nir_shape, z2500_nir_shape, z500_nir_shape)

# Read in NIR signal files with different zooms
z3500_nir_signal<-read.csv("nir_signal_z3500.csv", header=TRUE)
z2500_nir_signal<-read.csv("nir_signal_z2500.csv", header=TRUE)
z500_nir_signal<-read.csv("nir_signal_z500.csv", header=TRUE)

# Put all zooms into a common dataframe, remove individual files
nir_signal<-rbind(z3500_nir_signal, z2500_nir_signal, z500_nir_signal)
rm(z3500_nir_signal, z2500_nir_signal, z500_nir_signal)

# Planting date
planting_date = as.POSIXct("2013-11-26")

# Treatment column for NIR shape attributes
nir_shape$treatment <- NA
nir_shape$treatment[grep("AA", nir_shape$plant_id)] <- 100
nir_shape$treatment[grep("AB", nir_shape$plant_id)] <- 0
nir_shape$treatment[grep("AC", nir_shape$plant_id)] <- 16
nir_shape$treatment[grep("AD", nir_shape$plant_id)] <- 33
nir_shape$treatment[grep("AE", nir_shape$plant_id)] <- 66

# Treatment column for NIR signal attributes
nir_signal$treatment <- NA
nir_signal$treatment[grep("AA", nir_signal$plant_id)] <- 100
nir_signal$treatment[grep("AB", nir_signal$plant_id)] <- 0
nir_signal$treatment[grep("AC", nir_signal$plant_id)] <- 16
nir_signal$treatment[grep("AD", nir_signal$plant_id)] <- 33
nir_signal$treatment[grep("AE", nir_signal$plant_id)] <- 66

# Plant genotype column for NIR shape attributes
nir_shape$genotype <- NA
nir_shape$genotype[grep("p1", nir_shape$plant_id)] <- 'A10'
nir_shape$genotype[grep("p2", nir_shape$plant_id)] <- 'B100'
nir_shape$genotype[grep("r1", nir_shape$plant_id)] <- 'R20'
nir_shape$genotype[grep("r2", nir_shape$plant_id)] <- 'R70'
nir_shape$genotype[grep("r3", nir_shape$plant_id)] <- 'R98'
nir_shape$genotype[grep("r4", nir_shape$plant_id)] <- 'R102'
nir_shape$genotype[grep("r5", nir_shape$plant_id)] <- 'R128'
nir_shape$genotype[grep("r6", nir_shape$plant_id)] <- 'R133'
nir_shape$genotype[grep("r7", nir_shape$plant_id)] <- 'R161'
nir_shape$genotype[grep("r8", nir_shape$plant_id)] <- 'R187'

# Plant genotype column for NIR signal attributes
nir_signal$genotype <- NA
nir_signal$genotype[grep("p1", nir_signal$plant_id)] <- 'A10'
nir_signal$genotype[grep("p2", nir_signal$plant_id)] <- 'B100'
nir_signal$genotype[grep("r1", nir_signal$plant_id)] <- 'R20'
nir_signal$genotype[grep("r2", nir_signal$plant_id)] <- 'R70'
nir_signal$genotype[grep("r3", nir_signal$plant_id)] <- 'R98'
nir_signal$genotype[grep("r4", nir_signal$plant_id)] <- 'R102'
nir_signal$genotype[grep("r5", nir_signal$plant_id)] <- 'R128'
nir_signal$genotype[grep("r6", nir_signal$plant_id)] <- 'R133'
nir_signal$genotype[grep("r7", nir_signal$plant_id)] <- 'R161'
nir_signal$genotype[grep("r8", nir_signal$plant_id)] <- 'R187'

# Add date column based upon POSIX time for NIR shape
nir_shape$date <- as.POSIXct(nir_shape$datetime, origin = "1970-01-01")
nir_shape$dap <- as.numeric(nir_shape$date - planting_date)
nir_shape$dap_i <- as.integer(nir_shape$dap)
nir_shape$snapshot <- paste(nir_shape$plant_id, nir_shape$dap_i, sep=".")

# Add date column based upon POSIX time for NIR signal
nir_signal$date <- as.POSIXct(nir_signal$datetime, origin = "1970-01-01")
nir_signal$dap <- as.numeric(nir_signal$date - planting_date)
nir_signal$dap_i <- as.integer(nir_signal$dap)
nir_signal$snapshot <- paste(nir_signal$plant_id, nir_signal$dap_i, sep=".")

###
# Identify outliers
###

# Load in shapes from VIS pipeline
vis_shape<-read.csv("burnin2_data_2014-08-07.csv")

# Treatment column for VIS shape attributes
vis_shape$treatment <- NA
vis_shape$treatment[grep("AA", vis_shape$plant_id)] <- 100
vis_shape$treatment[grep("AB", vis_shape$plant_id)] <- 0
vis_shape$treatment[grep("AC", vis_shape$plant_id)] <- 16
vis_shape$treatment[grep("AD", vis_shape$plant_id)] <- 33
vis_shape$treatment[grep("AE", vis_shape$plant_id)] <- 66

# Plant genotype column for NIR shape attributes
vis_shape$genotype <- NA
vis_shape$genotype[grep("p1", vis_shape$plant_id)] <- 'A10'
vis_shape$genotype[grep("p2", vis_shape$plant_id)] <- 'B100'
vis_shape$genotype[grep("r1", vis_shape$plant_id)] <- 'R20'
vis_shape$genotype[grep("r2", vis_shape$plant_id)] <- 'R70'
vis_shape$genotype[grep("r3", vis_shape$plant_id)] <- 'R98'
vis_shape$genotype[grep("r4", vis_shape$plant_id)] <- 'R102'
vis_shape$genotype[grep("r5", vis_shape$plant_id)] <- 'R128'
vis_shape$genotype[grep("r6", vis_shape$plant_id)] <- 'R133'
vis_shape$genotype[grep("r7", vis_shape$plant_id)] <- 'R161'
vis_shape$genotype[grep("r8", vis_shape$plant_id)] <- 'R187'

# Add date column based upon POSIX time for NIR signal
vis_shape$date <- as.POSIXct(vis_shape$datetime, origin = "1970-01-01")
vis_shape$dap <- as.numeric(vis_shape$date - planting_date)
vis_shape$dap_i <- as.integer(vis_shape$dap)
vis_shape$snapshot <- paste(vis_shape$plant_id, vis_shape$dap_i, sep=".")

# For this experiment, images of pots with no plant are prefixed with '000' 
# Identify images with no plant
nir_shape_empties<-nir_shape[grep("^000", nir_shape$plant_id), ]
z3500_empty<-nir_shape_empties[nir_shape_empties$zoom == 3500,]
z2500_empty<-nir_shape_empties[nir_shape_empties$zoom == 2500,]
z500_empty<-nir_shape_empties[nir_shape_empties$zoom == 500,]

# Examine the distribution of plant_area and  extent_y of empty images
par(mfrow=c(2,1))

# Look at distribution of blank pot values at z3500
hist(z3500_empty$extent_y, col="blue", main="Hist of extent_y on empty images at z3500")
hist(z3500_empty$area_raw, col="green", main="Hist of area_raw on empty images at z3500")

# Get max values for these two attriburtes at zoom x3500 
z3500_extent_y_max_empty<-max(z3500_empty$extent_y)
z3500_area_raw_max_empty<-max(z3500_empty$area_raw)

# Didn't find any z2500 values that match '^000' prefix
z2500_extent_y_max_empty<-c(27)
z2500_area_raw_max_empty<-c(105)

# Look at distribution of blank pot values at z500
hist(z500_empty$extent_y, col="blue", main="Hist of extent_y on empty images at z500")
hist(z500_empty$area_raw, col="green", main="Hist of area_raw on empty images at z500")

# Get max values for these two attriburtes at zoom x500 
z500_extent_y_max_empty<-max(z500_empty$extent_y)
z500_area_raw_max_empty<-max(z500_empty$area_raw)
par(mfrow=c(1,1))

# Identify entries which are likely to be empty due to their extent_y and area_raw (use z3500 values for z2500)
low_values_3500<-nir_shape[((nir_shape$extent_y <= z3500_extent_y_max_empty) & (nir_shape$zoom == 3500)) | ((nir_shape$area_raw <= z3500_area_raw_max_empty) & (nir_shape$zoom == 3500)), ]
low_values_2500<-nir_shape[((nir_shape$extent_y <= z2500_extent_y_max_empty) & (nir_shape$zoom == 2500)) | ((nir_shape$area_raw <= z2500_area_raw_max_empty) & (nir_shape$zoom == 2500)), ]
low_values_500<-nir_shape[((nir_shape$extent_y <= z500_extent_y_max_empty) & (nir_shape$zoom == 500)) | ((nir_shape$area_raw <= z500_area_raw_max_empty) & (nir_shape$zoom == 500)), ]

# Get a list of empty images, these are uniquely descriminated by the column 'image_path'
low_values<-c(as.character(low_values_3500$image_path), as.character(low_values_2500$image_path), as.character(low_values_500$image_path))

# Remove these entries from both nir_signal and nir_shape datasets
nir_signal<-nir_signal[!nir_signal$image_path %in% low_values,]
nir_shape<-nir_shape[!nir_shape$image_path %in% low_values,]

save.image(file="NIR_data_before_QCQA.Rdata")

###
# Peform QC/QA analysis
###

# Use Rscript named "NIR_image_QCQA.R"

load("NIR_data_after_QCQA.Rdata")

###
# Start by looking at raw histograms over time
###

# Basically get the mean of the NIR signal by date and a single treatment
# This is an average of all RILs on each date + treatment by iterating through vector of unique dates

### If QC/QA wasn't run, you'll need to do this steps...
days<-sort(unique(nir_signal$dap_i))
genotypes<-sort(unique(nir_signal$genotype))
treatments<-sort(unique(nir_signal$treatment))
signal_snapshots<-paste(nir_signal$plant_id, nir_signal$dap_i, sep=".")

nir_signal<-nir_signal[,c(268, 267, 271, 270, 272, 269, 1:266)]
nir_signal<-nir_signal[,-c(15:16)]

#### If QC/QA was run, you can skip the part above...

signal_ave_100<-c()
for(i in 1:length(days)) {
  temp<-colMeans(nir_signal[nir_signal$dap_i == days[i] & nir_signal$treatment == 100, 15:270])
  assign(paste('signalave', days[i], sep='.'), temp)
  signal_ave_100<-rbind(signal_ave_100, get(paste('signalave', days[i], sep='.')))
  rownames(signal_ave_100)[i]<-c(paste('Day', days[i], sep='_'))
}

# Prepare a cool looking color scheme
hmcols<-colorRampPalette(c("black","white"))(100)
# You only want to plot histogram bin label every 50 bins or so. Leave remaining labels blank
collab<-c(0,rep('',49),50,rep('',49),100,rep('',49),150,rep('',49),200,rep('',49),250,rep('',5))
# Use a bar chart scheme on the side to show which zooms are which
hmrcols<-c(rep('red', 4), rep('orange', 6), rep('yellow', 12))
pdf(file="Pixel_content_of_NIR_as_heatmap_throughout.pdf", height=6, width=6, useDingbats=F)
heatmap(signal_ave_100, Rowv= NA, Colv=NA, labCol=collab, col=hmcols, RowSideColors=hmrcols, cexRow=1, cexCol=1)
dev.off()

# Same as above but with treatment == 33
signal_ave_33<-c()
for(i in 1:length(days)) {
  temp<-colMeans(nir_signal[nir_signal$dap_i == days[i] & nir_signal$treatment == 33, 15:270])
  assign(paste('signalave', days[i], sep='.'), temp)
  signal_ave_33<-rbind(signal_ave_33, get(paste('signalave', days[i], sep='.')))
  rownames(signal_ave_33)[i]<-c(paste('Day', days[i], sep='_'))
}

hmcols<-colorRampPalette(c("black","white"))(100)
hmrcols<-c(rep('red', 4), rep('orange', 6), rep('yellow', 12))
heatmap(signal_ave_33, Rowv= NA, Colv=NA, labCol="", col=hmcols, RowSideColors=hmrcols)

# Now, take the difference between well-waterted and 33$ drought. Do you see any pattern when you plot the histogram?
signal_ave_diff<-signal_ave_100-signal_ave_33

# Ramp between blue to white to red.
hmcols<-colorRampPalette(c("red","white","blue"))(100)

# Use plot on side to show which zooms are which
hmrcols<-c(rep('black', 4), rep('dark gray', 6), rep('light gray', 12))
collab<-c(0,rep('',49),50,rep('',49),100,rep('',49),150,rep('',49),200,rep('',49),250,rep('',5))

pdf(file="Difference_in_pixel_content_as_heatmap_throughout.pdf", height=6, width=6, useDingbats=F)
heatmap(signal_ave_diff, Rowv= NA, Colv=NA, labCol=collab, col=hmcols, RowSideColors=hmrcols, cexCol=1)
dev.off()

# Lets summarize the NIR histogram using PCA
# There looks like the difference is primarily in the third zoom level

###
# Calculate PCAs only on individual zoom levels
###

pr.nir.z500<-prcomp(as.matrix(nir_signal[(nir_signal$zoom == 500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),15:270]))

# Make a new data frame which contains entire signal and first 3 PCS for each entry
nir.pca.z500<-cbind(nir_signal[(nir_signal$zoom == 500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),], pr.nir.z500$x[,1:3])
colnames(nir.pca.z500)[271:273]<-c("nir.PC1", "nir.PC2", "nir.PC3")

# Same for zoom = 2500 and 3500
pr.nir.z2500<-prcomp(as.matrix(nir_signal[(nir_signal$zoom == 2500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),15:270]))
nir.pca.z2500<-cbind(nir_signal[(nir_signal$zoom == 2500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),], pr.nir.z2500$x[,1:3])
colnames(nir.pca.z2500)[271:273]<-c("nir.PC1", "nir.PC2", "nir.PC3")

pr.nir.z3500<-prcomp(as.matrix(nir_signal[(nir_signal$zoom == 3500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),15:270]))
nir.pca.z3500<-cbind(nir_signal[(nir_signal$zoom == 3500) & (nir_signal$treatment == 33 | nir_signal$treatment == 100),], pr.nir.z3500$x[,1:3])
colnames(nir.pca.z3500)[271:273]<-c("nir.PC1", "nir.PC2", "nir.PC3")

###
# Examine PCs
###

# Can you seperate genotypes (A10 and B100) and treatments (33, 66, 100) basedon PC1 and PC2
# Get zoom = 500 and parents only

nir.pca.z500_parents<-nir.pca.z500[nir.pca.z500$genotype == "A10" | nir.pca.z500$genotype == "B100",]

# Assign treatments same color scheme as ggplot
treat <- c('100', '33')
t.col<-c('green', 'blue')
myCol_z500 <- rep("black", nrow(nir.pca.z500_parents))
for(i in 1:length(treat)){
  myCol_z500[nir.pca.z500_parents$treatment == treat[i]] <- t.col[i]
}

# Assign genotypes different plotting characters
geno <- unique(nir.pca.z500_parents$genotype)
g.chr<-c(19,17)
myChr_z500 <- rep("3", nrow(nir.pca.z500_parents))
for(i in 1:length(geno)){
  myChr_z500[nir.pca.z500_parents$genotype == geno[i]] <- g.chr[i]
}

# Plot values PC1 on x-axis, PC2 on y-axis
plot(nir.pca.z500_parents$nir.PC2~nir.pca.z500_parents$nir.PC1, pch = as.numeric(myChr_z500), cex=0.5, xlab='PC1 (33.5% of total variance)', ylab='PC2 (7.6% of total variance)', col = myCol_z500)
# Looks like both treatments and genotype seperate at zoom = 500

# Plot the loadings of the PC1 for each zoom (need to multiply z500 by -1 to make comparable to other zooms)
pdf(file="PC1_loadings_across_zooms.pdf", height=6, width=6, useDingbats=F)
plot(pr.nir.z500$rotation[,1]*-1, col="dark blue", pch=19, cex=0.3, ylab="PC1 loading", xlab="NIR signal bin", ylim=c(-0.19, 0.19))
points(pr.nir.z2500$rotation[,1], col="blue", pch=19, cex=0.3)
points(pr.nir.z3500$rotation[,1], col="light blue", pch=19, cex=0.3)
abline(h=0, lty=3, col="red")
dev.off()

# Lets examine the difference in PC1 if well-watered is subtracted from drought.

# Think about PC1 loadings in terms of the difference between treatment bin proportion (100 vs 33)
mean_100_z500<-colMeans(nir.pca.z500[nir.pca.z500$treatment == 100,15:270])
mean_100_z2500<-colMeans(nir.pca.z2500[nir.pca.z2500$treatment == 100,15:270])
mean_100_z3500<-colMeans(nir.pca.z3500[nir.pca.z3500$treatment == 100,15:270])

mean_33_z500<-colMeans(nir.pca.z500[nir.pca.z500$treatment == 33,15:270])
mean_33_z2500<-colMeans(nir.pca.z2500[nir.pca.z2500$treatment == 33,15:270])
mean_33_z3500<-colMeans(nir.pca.z3500[nir.pca.z3500$treatment == 33,15:270])

diff_100_33_z500<-mean_100_z500-mean_33_z500
diff_100_33_z2500<-mean_100_z2500-mean_33_z2500
diff_100_33_z3500<-mean_100_z3500-mean_33_z3500

# Plot the differences at each zoom level
pdf(file="Difference_in_pixel_content.pdf", height=6, width=6, useDingbats=F)
plot(diff_100_33_z500, pch=19, col=c("dark green"), cex=0.3, ylab=c("Differnece in pixel content"), xlab=c("NIR signal bin"))
points(diff_100_33_z2500, pch=19, col=c("green"), cex=0.3)
points(diff_100_33_z3500, pch=19, col=c("yellow"), cex=0.3)
abline(h=0, lty=3, col="red")
dev.off()

# Replace the dates with POSIX timestamp dates
nir.pca.z500$POSIX<-as.POSIXct(nir.pca.z500$datetime, origin="1970-01-01")
nir.pca.z2500$POSIX<-as.POSIXct(nir.pca.z2500$datetime, origin="1970-01-01")
nir.pca.z3500$POSIX<-as.POSIXct(nir.pca.z3500$datetime, origin="1970-01-01")

# Do same thing with parents
nir.pca.z500_parents$POSIX<-as.POSIXct(nir.pca.z500_parents$datetime, origin="1970-01-01")

# Plot the first PC component modeled by timepoint (seconds) but labels are plotted as by day at zoom 500
pdf(file="PC1_parents_z500.pdf", height=6, width=6, useDingbats=F)
p<-ggplot(nir.pca.z500_parents, aes(POSIX, nir.PC1 * -1, group=treatment, color=factor(treatment))) + geom_point(size=1) + geom_smooth(method="loess") + facet_wrap(~genotype) 
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1)) + scale_y_continuous(name='NIR.PC1')  + scale_fill_discrete(name="Water treatment", breaks=c("33", "100"), labels=c("33%", "100%"))                                                                                                       
dev.off()

# Plot the first PC component modeled by timepoint (seconds) but labels are plotted as by day (all genotypes) at zoom 500
p<-ggplot(nir.pca.z500, aes(POSIX, nir.PC1, group=treatment, color=factor(treatment))) + stat_smooth() + facet_wrap(~genotype) 
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))                                                                                                                 

# Plot the first PC component modeled by timepoint (seconds) but labels are plotted as by day (all genotypes) at zoom 2500
p<-ggplot(nir.pca.z2500, aes(POSIX, nir.PC1, group=treatment, color=factor(treatment))) + stat_smooth() + facet_wrap(~genotype) 
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))    

# Plot by treatment at zoom 2500
p<-ggplot(nir.pca.z2500, aes(POSIX, nir.PC1, group=genotype, color=factor(genotype))) + stat_smooth()  + facet_wrap(~treatment)
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Plot by treatment at zoom 500
p<-ggplot(nir.pca.z500, aes(POSIX, nir.PC1, group=genotype, color=factor(genotype))) + stat_smooth()  + facet_wrap(~treatment)
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Plot by treatment at zoom 500
p_z500<-nir.pca.z500[nir.pca.z500$genotype == "A10" | nir.pca.z500$genotype == "B100",]
p_z2500<-nir.pca.z2500[nir.pca.z2500$genotype == "A10" | nir.pca.z2500$genotype == "B100",]

# Just parental genotypes by treatment at zoom 2500
p<-ggplot(p_z2500, aes(POSIX, nir.PC1, group=genotype, color=factor(genotype))) + stat_smooth()  + facet_wrap(~treatment)
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Just parental genotypes by treatment at zoom 500
p<-ggplot(p_z500, aes(POSIX, nir.PC1, group=genotype, color=factor(genotype))) + stat_smooth()  + facet_wrap(~treatment)
p + scale_x_datetime(breaks = date_breaks("1 day")) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1))

###
# Perform significance testing
###

# Aggregate first
nir.pca.z3500.ag<-aggregate(nir.pca.z3500[,c(4,271:273)], by=list(nir.pca.z3500$genotype, nir.pca.z3500$treatment, nir.pca.z3500$dap_i, nir.pca.z3500$plant_id), mean)
nir.pca.z2500.ag<-aggregate(nir.pca.z2500[,c(4,271:273)], by=list(nir.pca.z2500$genotype, nir.pca.z2500$treatment, nir.pca.z2500$dap_i, nir.pca.z2500$plant_id), mean)
nir.pca.z500.ag<-aggregate(nir.pca.z500[,c(4,271:273)], by=list(nir.pca.z500$genotype, nir.pca.z500$treatment, nir.pca.z500$dap_i, nir.pca.z500$plant_id), mean)

colnames(nir.pca.z3500.ag)[1:4]<-c("genotype", "treatment", "dap_i", "plant_id")
colnames(nir.pca.z2500.ag)[1:4]<-c("genotype", "treatment", "dap_i", "plant_id")
colnames(nir.pca.z500.ag)[1:4]<-c("genotype", "treatment", "dap_i", "plant_id")

# Get unique list of days
days_z3500<-sort(unique(nir.pca.z3500$mmdd))
# Get a list of genotypes
genotype<-sort(unique(nir.pca.z3500$id))

# Perform significance test on z3500 images
final_report_z3500<-c()
for(i in 1:(length(days_z3500)-1)) {
  temp<-nir.pca.z3500.ag[(nir.pca.z3500.ag$dap_i == days_z3500[i] | nir.pca.z3500.ag$dap_i == days_z3500[i+1]),]
  tt.all<-t.test(temp[temp$treatment == 100, 'nir.PC1'], temp[temp$treatment == 33, 'nir.PC1'])
  p_val<-tt.all$p.value
  g<-c("all")
  d<-days_z3500[i]
  ind_100<-temp[temp$treatment == 100,]
  ind_33<-temp[temp$treatment == 33,]
  ind_100<-nrow(ind_100)
  ind_33<-nrow(ind_33)
  report<-c(g,d,ind_100,ind_33,p_val)
  final_report_z3500<-rbind(final_report_z3500,report)
  for(j in 1:length(genotype)) {
    temp_100<-temp[temp$treatment == 100 & temp$genotype == genotype[j], 'nir.PC1']
    temp_33<-temp[temp$treatment == 33 & temp$genotype == genotype[j], 'nir.PC1']
    tt<-t.test(temp_100[1:8], temp_33[1:8])
    p_val<-tt$p.value
    g<-genotype[j]
    d<-days_z3500[i]
    ind_100<-temp[temp$id == genotype[j] & temp$treatment == 100,]
    ind_33<-temp[temp$id == genotype[j] & temp$treatment == 33,]
    ind_100<-nrow(ind_100)
    ind_33<-nrow(ind_33)
    report<-c(g,d,ind_100,ind_33,p_val)
    final_report_z3500<-rbind(final_report_z3500,report)
  }
}

# Do the same as above at zoom = 2500
days_z2500<-sort(unique(nir.pca.z2500.ag$dap_i))
genotype<-sort(unique(nir.pca.z2500.ag$genotype))

final_report_z2500<-c()
for(i in 1:(length(days_z2500)-1)) {
  temp<-nir.pca.z2500.ag[(nir.pca.z2500.ag$dap_i == days_z2500[i] | nir.pca.z2500.ag$dap_i == days_z2500[i+1]),]
  tt.all<-t.test(temp[temp$treatment == 100, 'nir.PC1'], temp[temp$treatment == 33, 'nir.PC1'])
  p_val<-tt.all$p.value
  g<-c("all")
  d<-days_z2500[i]
  ind_100<-temp[temp$treatment == 100,]
  ind_33<-temp[temp$treatment == 33,]
  ind_100<-nrow(ind_100)
  ind_33<-nrow(ind_33)
  report<-c(g,d,ind_100,ind_33,p_val)
  final_report_z2500<-rbind(final_report_z2500,report)
  for(j in 1:length(genotype)) {
    temp_100<-temp[temp$treatment == 100 & temp$genotype == genotype[j], 'nir.PC1']
    temp_33<-temp[temp$treatment == 33 & temp$genotype == genotype[j], 'nir.PC1']
    tt<-t.test(temp_100[1:8], temp_33[1:8])
    p_val<-tt$p.value
    g<-genotype[j]
    d<-days_z2500[i]
    ind_100<-temp[temp$id == genotype[j] & temp$treatment == 100,]
    ind_33<-temp[temp$id == genotype[j] & temp$treatment == 33,]
    ind_100<-nrow(ind_100)
    ind_33<-nrow(ind_33)
    report<-c(g,d,ind_100,ind_33,p_val)
    final_report_z2500<-rbind(final_report_z2500,report)
  }
}

# Do the same as above at zoom = 500
days_z500<-sort(unique(nir.pca.z500.ag$dap_i))
genotype<-sort(unique(nir.pca.z500.ag$genotype))
final_report_z500<-c()

for(i in 1:(length(days_z500)-1)) {
  temp<-nir.pca.z500.ag[(nir.pca.z500.ag$dap_i == days_z500[i] | nir.pca.z500.ag$dap_i == days_z500[i+1]),]
  tt.all<-t.test(temp[temp$treatment == 100, 'nir.PC1'], temp[temp$treatment == 33, 'nir.PC1'])
  p_val<-tt.all$p.value
  g<-c("all")
  d<-days_z500[i]
  ind_100<-temp[temp$treatment == 100,]
  ind_33<-temp[temp$treatment == 33,]
  ind_100<-nrow(ind_100)
  ind_33<-nrow(ind_33)
  report<-c(g,d,ind_100,ind_33,p_val)
  final_report_z500<-rbind(final_report_z500,report)
  for(j in 1:length(genotype)) {
    temp_100<-temp[temp$treatment == 100 & temp$genotype == genotype[j], 'nir.PC1']
    temp_33<-temp[temp$treatment == 33 & temp$genotype == genotype[j], 'nir.PC1']
    tt<-t.test(temp_100[1:8], temp_33[1:8])
    p_val<-tt$p.value
    g<-genotype[j]
    d<-days_z500[i]
    ind_100<-temp[temp$id == genotype[j] & temp$treatment == 100,]
    ind_33<-temp[temp$id == genotype[j] & temp$treatment == 33,]
    ind_100<-nrow(ind_100)
    ind_33<-nrow(ind_33)
    report<-c(g,d,ind_100,ind_33,p_val)
    final_report_z500<-rbind(final_report_z500,report)
  }
}

# Add all files together into a final report of all days
final_report<-rbind(final_report_z3500, final_report_z2500, final_report_z500)

# Give better colnames and make into a data frame from a matrix
colnames(final_report)<-c("id", 'dap','ind_100', 'ind_33', 'pval')
final_report<-as.data.frame(final_report)
final_report_days<-sort(unique(final_report$dap))
rownames(final_report)<-c(1:nrow(final_report))

final_report$rounded<-round(as.numeric(as.character(final_report$pval)), 5)

write.csv(final_report, file="NIR_significance_by_day_after_aggregation_first_8.csv", quote=F, row.names=F)

save.image(file="NIR_image_analysis_burnin2.Rdata")
