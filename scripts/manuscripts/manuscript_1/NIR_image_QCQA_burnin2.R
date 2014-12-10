# Script to perform QC/QA on NIR data
# Written by Max Feldman 12.8.14
# mfeldman@danforthcenter.org

###
# Proceed with QC/QA based on shape attributes
###

# Load libraries
library(emdist)
library(rgl)
library(analogue)
library(VennDiagram)

# Load data
setwd("/Users/mfeldman/Desktop/current_phenotyping/burnin2")
load("NIR_data_before_QCQA.Rdata")

# First, remove entries which the plant is called 'out of bounds' in the VIS image
# When using VIS-NIR comparison to identify NIR outliers plants which are out of bounds in VIS are often times the highest ranking outliers even though the NIR image is good

# Identify a subset of images which are called as out of frame in VIS images (need to remove to do shape based QC/QA)
out_of_bounds<-vis_shape[vis_shape$in_bounds=='FALSE',]
vis_shape_in_bounds<-vis_shape[!vis_shape$image_path %in% out_of_bounds$image_path,]

# merge vis and nir shape data.frame into the same data.frame by common attributes 
# colnames from VIS will be appended with an .x (ex/ area_raw.x)
# colnames from NIR will be appended with an .y (ex/ area_raw.y)

merge_shape<-merge(vis_shape_in_bounds, nir_shape, by=c('genotype','treatment','dap_i','frame','plant_id','snapshot'))
# subset attributes to keep only the ones for comparison, and rename 'area' and 'area_raw' columns
# columns 1:6 are by=c('genotype','treatment','dap_i','frame','plant_id','snapshot') and 15:24 are VIS shape attributes 40:50 are NIR shape attributes (column 41 is not common)
merge_shape<-merge_shape[,c(1:6,15:24,40,42:50)]
colnames(merge_shape)[c(7,17)]<-c('area_raw.x', 'area_raw.y')

###
# Compare the correlation between VIS and NIR images using daily models
###

days<-sort(unique(merge_shape$dap_i))
genotypes<-sort(unique(merge_shape$genotype))
treatments<-sort(unique(merge_shape$treatment))

# Calculate models using this loop 
shape_models<-c()
for(j in 1:length(days)) {
  d <- days[j]
  shape_day<-merge_shape[merge_shape$dap_i == d,]
  day_fit<-shape_day
  for (k in 7:16) {
    shape_trait<-c()
    l <- k + 10
    # model NIR value given VIS
    shape_lm<-lm(shape_day[,l]~shape_day[,k])
    # get expected phenotype value
    shape_day$fitted<-fitted(shape_lm)
    # get residual
    shape_day$residual<-residuals(shape_lm)
    # get standardized residual
    shape_day$standardresid<-rstandard(shape_lm)
    # remove .x or .y from phenotype name for storage
    shape_name<-strsplit(colnames(shape_day)[k], split="[.]")
    shape_name<-shape_name[[1]][1]
    # add the last three columns ('fitted', 'residual', 'standardresidual') to shape trait
    shape_trait<-shape_day[,c(27:29)]
    # rename the columns to include trait name
    colnames(shape_trait)<-paste(shape_name, colnames(shape_trait), sep=".")
    # add values to data frame representing day
    day_fit<-cbind(day_fit, shape_trait)
  }
  shape_models<-rbind(shape_models, day_fit)
}

# STDEV cut-off increase or decrease value
stdev_cutoff <- 2

outlier_shp.mdl_area.raw<-shape_models[abs(shape_models$area_raw.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_hull_area<-shape_models[abs(shape_models$hull_area.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_solidity<-shape_models[abs(shape_models$solidity.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_perimeter<-shape_models[abs(shape_models$perimeter.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_extent_x<-shape_models[abs(shape_models$extent_x.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_extent_y<-shape_models[abs(shape_models$extent_y.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_centroid_x<-shape_models[abs(shape_models$centroid_x.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_centroid_y<-shape_models[abs(shape_models$centroid_y.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_longest_axis<-shape_models[abs(shape_models$longest_axis.standardresid) > stdev_cutoff, ]
outlier_shp.mdl_hull_vertices<-shape_models[abs(shape_models$hull_vertices.standardresid) > stdev_cutoff, ]

outlier_shp.mdl_all<-rbind(outlier_shp.mdl_area.raw,outlier_shp.mdl_hull_area,outlier_shp.mdl_solidity,outlier_shp.mdl_perimeter,outlier_shp.mdl_extent_x,outlier_shp.mdl_extent_y,outlier_shp.mdl_centroid_x,outlier_shp.mdl_centroid_y,outlier_shp.mdl_longest_axis,outlier_shp.mdl_hull_vertices)
# unique_outlier_shp.mdl_all<-outlier_shp.mdl_all[!duplicated(outlier_shp.mdl_all$image_path.y),]

###
# Proceed with QC/QA based on NIR signal attributes
###


days<-sort(unique(nir_signal$dap_i))
genotypes<-sort(unique(nir_signal$genotype))
treatments<-sort(unique(nir_signal$treatment))
signal_snapshots<-paste(nir_signal$plant_id, nir_signal$dap_i, sep=".")

nir_signal<-nir_signal[,c(268, 267, 271, 270, 272, 269, 1:266)]
nir_signal<-nir_signal[,-c(15:16)]

nir_signal_mean_by_factor<-c()

for(i in 1:length(days)) {
  for(j in 1:length(genotypes)) {
    for(k in 1:length(treatments)) {
      factor_mean<-colMeans(nir_signal[nir_signal$dap_i == days[i] & nir_signal$genotype == genotypes[j] & nir_signal$treatment == treatments[k],15:270])
      factor_mean<-c(as.character(days[i]), as.character(genotypes[j]), as.character(treatments[k]), factor_mean)
      nir_signal_mean_by_factor<-rbind(nir_signal_mean_by_factor, factor_mean)
    }
  }
}

colnames(nir_signal_mean_by_factor)[1:3]<-c("dap_i", "genotype", "treatment")
rownames(nir_signal_mean_by_factor)<-paste(nir_signal_mean_by_factor[,1], nir_signal_mean_by_factor[,2],nir_signal_mean_by_factor[,3], sep=".")

nir_signal_qc_img<-c()
nir_signal_qc_snap<-c()
# Do the following analaysis for each nir image signal set
for (i in 1:length(signal_snapshots)) {
  #for (i in 1:10) {
  s.snap<-signal_snapshots[i]
  signal_day<-nir_signal[nir_signal$snapshot == s.snap,]
  d<-dim(signal_day)
  if (d[1]<4) {next}
  # Make sure the frame (0,90,180,270) are in a consistent order (signal_day[,12] is the column for signal_day$frame)
  signal_day<-signal_day[order(signal_day[,12]),]
  # Calculate the average signal in the image set
  signal_day_ave<-colMeans(signal_day[,15:270])
  # Get snapshot average date x genotype x treatment
  nir_signal_factor<-paste(signal_day$dap_i,signal_day$genotype, signal_day$treatment, sep=".")
  d.g.t.ave<-nir_signal_mean_by_factor[rownames(nir_signal_mean_by_factor) == nir_signal_factor,]
  signal_day_and_ave<-rbind(signal_day[,15:270], signal_day_ave)
  # Get snapshot average date x genotype x treatment
  nir_signal_factor<-paste(signal_day$mmdd,signal_day$id, signal_day$treatment, sep=".")
  d.g.t.ave<-nir_signal_mean_by_factor[rownames(nir_signal_mean_by_factor) == nir_signal_factor,]
  signal_day_and_ave<-rbind(signal_day_and_ave, as.numeric(d.g.t.ave[4:259]))
  # Calculate chi-square distance between reflective images (0-180, 90-270)
  chi.sq_dist.mat<-distance(signal_day_and_ave, method='chi.square')
  # Value of the 90-270 reflecive images is stored in chi.sq_dist.mat[2,1]  
  score_0_180<-chi.sq_dist.mat[1,3]
  score_90_270<-chi.sq_dist.mat[2,4]
  score_0_AVE<-chi.sq_dist.mat[1,5]
  score_90_AVE<-chi.sq_dist.mat[2,5]
  score_180_AVE<-chi.sq_dist.mat[3,5]
  score_270_AVE<-chi.sq_dist.mat[4,5]
  group_0_AVE<-chi.sq_dist.mat[1,6]
  group_90_AVE<-chi.sq_dist.mat[2,6]
  group_180_AVE<-chi.sq_dist.mat[3,6]
  group_270_AVE<-chi.sq_dist.mat[4,6]
  
  # Calcuate average chi-square distance of all snapshots
  distances<-c(chi.sq_dist.mat[2:4,1],chi.sq_dist.mat[3:4,2],chi.sq_dist.mat[4,3])
  chi.sq_AVE<-mean(distances)
  # Calculate earth movers distance (EMD) between reflective images (0-180, 90-270)
  emd_0_180<-emd2d(as.matrix(signal_day[1,15:270]), as.matrix(signal_day[3,15:270]), dist='euclidean')
  emd_90_270<-emd2d(as.matrix(signal_day[2,15:270]), as.matrix(signal_day[4,15:270]), dist='euclidean')
  emd_0_AVE<-emd2d(as.matrix(signal_day[1,15:270]), t(as.matrix(signal_day_ave)), dist='euclidean')
  emd_90_AVE<-emd2d(as.matrix(signal_day[2,15:270]), t(as.matrix(signal_day_ave)), dist='euclidean')
  emd_180_AVE<-emd2d(as.matrix(signal_day[3,15:270]), t(as.matrix(signal_day_ave)), dist='euclidean')
  emd_270_AVE<-emd2d(as.matrix(signal_day[4,15:270]), t(as.matrix(signal_day_ave)), dist='euclidean')
  emd_0_GROUP<-emd2d(as.matrix(signal_day[1,15:270]), as.matrix(signal_day_and_ave[6,]), dist='euclidean')
  emd_90_GROUP<-emd2d(as.matrix(signal_day[2,15:270]), as.matrix(signal_day_and_ave[6,]), dist='euclidean')
  emd_180_GROUP<-emd2d(as.matrix(signal_day[3,15:270]), as.matrix(signal_day_and_ave[6,]), dist='euclidean')
  emd_270_GROUP<-emd2d(as.matrix(signal_day[4,15:270]), as.matrix(signal_day_and_ave[6,]), dist='euclidean')
  
  
  # Write results to a data.frame
  img_qc_0_AVE<-cbind(signal_day[1,c(1,2,9,10,12,17,276)], score_0_AVE, group_0_AVE, emd_0_AVE, emd_0_GROUP)
  img_qc_90_AVE<-cbind(signal_day[2,c(1,2,9,10,12,17,276)], score_90_AVE, group_90_AVE, emd_90_AVE, emd_90_GROUP)
  img_qc_180_AVE<-cbind(signal_day[3,c(1,2,9,10,12,17,276)], score_180_AVE, group_180_AVE, emd_180_AVE, emd_180_GROUP)
  img_qc_270_AVE<-cbind(signal_day[4,c(1,2,9,10,12,17,276)], score_270_AVE, group_270_AVE, emd_270_AVE, emd_270_GROUP)
  colnames(img_qc_0_AVE)[c(8,9,10,11)]<-c('chi.sq.d_snap','chi.sq.d_group','emd_snap', 'emd_group')
  colnames(img_qc_90_AVE)[c(8,9,10,11)]<-c('chi.sq.d_snap','chi.sq.d_group','emd_snap', 'emd_group')
  colnames(img_qc_180_AVE)[c(8,9,10,11)]<-c('chi.sq.d_snap','chi.sq.d_group','emd_snap', 'emd_group')
  colnames(img_qc_270_AVE)[c(8,9,10,11)]<-c('chi.sq.d_snap','chi.sq.d_group','emd_snap', 'emd_group')
  img_qc<-rbind(img_qc_0_AVE, img_qc_90_AVE, img_qc_180_AVE, img_qc_270_AVE)
  
  # Write metrics from each image and snapshot to data.frame which summarizes images and ratios
  snap_qc_0<-cbind(signal_day[1,c(1,2,9,10,12,17,276)], score_0_180, emd_0_180, chi.sq_AVE)
  snap_qc_90<-cbind(signal_day[2,c(1,2,9,10,12,17,276)], score_90_270, emd_90_270, chi.sq_AVE)
  colnames(snap_qc_0)[c(8,9,10)]<-c('chi.sq.ratio.d','emd','chi.sq.ave.d')
  colnames(snap_qc_90)[c(8,9,10)]<-c('chi.sq.ratio.d','emd','chi.sq.ave.d')
  snap_qc<-rbind(snap_qc_0, snap_qc_90)
  
  # Write both images and snapshots to a large data.frame for further analysis (combine this snapshot/image set with the rest)
  nir_signal_qc_img<-rbind(nir_signal_qc_img, img_qc)
  nir_signal_qc_snap<-rbind(nir_signal_qc_snap, snap_qc)
}

# calculate the standard deviation within each metric based on image
sd_chi.sq_snap<-sd(nir_signal_qc_img[,8])
sd_chi.sq_group<-sd(nir_signal_qc_img[,9])
sd_emd_snap<-sd(nir_signal_qc_img[,10])
sd_emd_group<-sd(nir_signal_qc_img[,11])

# calculate the standard deviation within each metric based on snapshot
sd_chi.sq_mirror_snap<-sd(nir_signal_qc_snap[,8])
sd_emd_mirror_snap<-sd(nir_signal_qc_snap[,9])
sd_chi.sq_ave_snap<-sd(nir_signal_qc_snap[seq(1, nrow(nir_signal_qc_snap), 2),10])

# calculate cut-off (2 STDEV greater than the mean distance score)
cutoff_chi.sq_snap<-(mean(nir_signal_qc_img[,8])+(2*sd_chi.sq_snap))
cutoff_chi.sq_group<-(mean(nir_signal_qc_img[,9])+(2*sd_chi.sq_group))
cutoff_emd_snap<-(mean(nir_signal_qc_img[,10])+(2*sd_emd_snap))
cutoff_emd_group<-(mean(nir_signal_qc_img[,11])+(2*sd_emd_group))

cutoff_chi.sq_mirror_snap<-(mean(nir_signal_qc_snap[,8])+(2*sd_chi.sq_mirror_snap))
cutoff_emd_mirror_snap<-(mean(nir_signal_qc_snap[,9])+(2*sd_emd_mirror_snap))
cutoff_chi.sq_ave_snap<-(mean(nir_signal_qc_snap[seq(1, nrow(nir_signal_qc_snap), 2), 10])+(2*sd_chi.sq_ave_snap))

# flag outliers which exhibit a chi-squre distance or EMD score greater than 2 STDEV from the mean
outlier_chi.sq_snap<-nir_signal_qc_img[nir_signal_qc_img[,8] > (cutoff_chi.sq_snap),]
outlier_chi.sq_group<-nir_signal_qc_img[nir_signal_qc_img[,9] > (cutoff_chi.sq_group),]
outlier_emd_snap<-nir_signal_qc_img[nir_signal_qc_img[,10] > (cutoff_emd_snap),]
outlier_emd_group<-nir_signal_qc_img[nir_signal_qc_img[,11] > (cutoff_emd_group),]


outlier_chi.sq_snap<-nir_signal_qc_snap[nir_signal_qc_snap[,8] > (cutoff_chi.sq_mirror_snap),]
outlier_emd_snap<-nir_signal_qc_snap[nir_signal_qc_snap[,9] > (cutoff_emd_mirror_snap),]
outlier_chi.sq_ave_snap<-nir_signal_qc_snap[nir_signal_qc_snap[,9] > (cutoff_chi.sq_ave_snap),]

outlier_chi.sq_img<-unique(outlier_chi.sq_img)
outlier_emd_img<-unique(outlier_emd_img)
outlier_chi.sq_snap<-unique(outlier_chi.sq_snap)
outlier_emd_snap<-unique(outlier_emd_snap)
 
save.image(file="NIR_data_after_QCQA.Rdata")