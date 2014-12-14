# Partitioning of variance script
# Written by Max Feldman 12.8.14
# mfeldman@danforthcenter.org


###
# Partition variance for NIR signal
###

library(lme4)
load(save.image(file="NIR_image_analysis_burnin2.Rdata"))

# put all in same dataframe
nir.pca.all.ag<-rbind(nir.pca.z3500.ag, nir.pca.z2500.ag, nir.pca.z500.ag)

days<-sort(unique(nir_signal$dap_i))
days_to_test<-c(15, 19, 25, 31)

n<-nir.pca.all.ag[,c(1:4,6:8)]
colnames(n)<-c("genotype", "treatment", "day","plant_id", "nirPC1", "nir.PC2", "nir.PC3")

variance_table<-c()
for (i in 1:length(days_to_test)) {
  d<-days_to_test[i]  
  H2<-c()
  r2<-c()
  e2<-c()
  gxe2<-c()
  
  for(j in 5:ncol(n)) {
    npa<-n[(n$day == d | n$day == d + 1) ,c(1:2,j)]
    cc.n<-npa[complete.cases(npa),]
    model<-lmer(cc.n[,3]~1+(1|genotype)+(1|treatment)+(1|genotype:treatment), data=cc.n)
    re<-as.numeric(VarCorr(model))
    res<-attr(VarCorr(model), "sc")^2
  
    gxe.var<-re[1]
    g.var<-re[2]
    e.var<-re[3]
    tot.var<-sum(re, res)
  
    h<-g.var/tot.var
    e<-e.var/tot.var
    r<-res/tot.var
    gxe<-gxe.var/tot.var
  
    H2<-c(H2,h)
    e2<-c(e2,e)
    r2<-c(r2,r)
    gxe2<-c(gxe2, gxe)
  }

variance<-rbind(H2, e2, gxe2, r2)
variance<-cbind(variance, rep(d, nrow(variance)))
colnames(variance)<-c('nir.PC1', 'nir.PC2', 'nir.PC3', 'day')
rownames(variance)<-c('Genotype', 'Treatment', 'G x Treatment', 'Residual')

variance_table<-rbind(variance_table, variance)

}

nir.var.table<-cbind(round(variance_table[,1:3]*100, 1), variance_table[,4])
colnames(nir.var.table)[4]<-c("day")
write.table(nir.var.table, file='nir.pc.var.table_12.8.14.csv', append=F, quote=F, sep=",", row.names=T, col.names=NA)

###
# Do the same for VIS shape data
###


# Planting date
planting_date = as.POSIXct("2013-11-26")

# Read VIS data
vis.data<-read.csv("vis.traits.csv")

# Treatment column
vis.data$treatment <- NA
vis.data$treatment[grep("AA", vis.data$plant_id)] <- 100
vis.data$treatment[grep("AB", vis.data$plant_id)] <- 0
vis.data$treatment[grep("AC", vis.data$plant_id)] <- 16
vis.data$treatment[grep("AD", vis.data$plant_id)] <- 33
vis.data$treatment[grep("AE", vis.data$plant_id)] <- 66

# Plant genotype column
vis.data$genotype <- NA
vis.data$genotype[grep("p1", vis.data$plant_id)] <- 'A10'
vis.data$genotype[grep("p2", vis.data$plant_id)] <- 'B100'
vis.data$genotype[grep("r1", vis.data$plant_id)] <- 'R20'
vis.data$genotype[grep("r2", vis.data$plant_id)] <- 'R70'
vis.data$genotype[grep("r3", vis.data$plant_id)] <- 'R98'
vis.data$genotype[grep("r4", vis.data$plant_id)] <- 'R102'
vis.data$genotype[grep("r5", vis.data$plant_id)] <- 'R128'
vis.data$genotype[grep("r6", vis.data$plant_id)] <- 'R133'
vis.data$genotype[grep("r7", vis.data$plant_id)] <- 'R161'
vis.data$genotype[grep("r8", vis.data$plant_id)] <- 'R187'

# Group
vis.data$group = paste(vis.data$genotype,'-',vis.data$treatment,sep='')

# Date-time from Unix time
vis.data$date = as.POSIXct(vis.data$datetime, origin = "1970-01-01")

# Days after planting
vis.data$dap = as.numeric(vis.data$date - planting_date)

vis.data$dap_integer<-as.integer(vis.data$dap)

all_days<-sort(unique(vis.data$dap_integer))
days_to_test<-c(15, 19, 25, 31)


vis.data<-vis.data[,c(21,20,27,3:17,25:26)]
vis.data<-vis.data[vis.data$wue != Inf,]

variance_table<-c()

for (i in 1:length(days_to_test)) {
  d<-days_to_test[i]  
  H2<-c()
  r2<-c()
  e2<-c()
  gxe2<-c()
  
  for(j in 4:20) {
    vis<-vis.data[(vis.data$dap_integer == d | vis.data$dap_integer == d+1) & ( vis.data$treatment == 33 | vis.data$treatment == 100 )  ,c(1:2,j)]
    cc.vis<-vis[complete.cases(vis),]
    #cc.vis<-cc.vis[-c(cc.vis[,3] == 'Inf'),]
    model<-lmer(cc.vis[,3]~1+(1|genotype)+(1|treatment)+(1|genotype:treatment), data=cc.vis)
    re<-as.numeric(VarCorr(model))
    res<-attr(VarCorr(model), "sc")^2
    
    gxe.var<-re[1]
    g.var<-re[2]
    e.var<-re[3]
    tot.var<-sum(re, res)
    
    h<-g.var/tot.var
    e<-e.var/tot.var
    r<-res/tot.var
    gxe<-gxe.var/tot.var
    
    H2<-c(H2,h)
    e2<-c(e2,e)
    r2<-c(r2,r)
    gxe2<-c(gxe2, gxe)
  }
  
  variance<-rbind(H2, e2, gxe2, r2)
  variance<-cbind(variance, rep(d, nrow(variance)))
  colnames(variance)<-c(colnames(vis.data)[4:20], 'DAP')
  rownames(variance)<-c('Genotype', 'Treatment', 'G x Treatment', 'Residual')
  
  variance_table<-rbind(variance_table, variance)
  
}

vis.shape.var.table<-cbind(round(variance_table[,1:17]*100,1),variance_table[,18])
colnames(vis.shape.var.table)[18]<-c("day")

write.table(vis.shape.var.table, file='vis.shape.var.table.12.8.14.csv', append=F, quote=F, sep=",", row.names=T, col.names=NA)

###
# Do same thing for FLU signal
###

setwd("/Users/mfeldman/Desktop/current_phenotyping/burnin2/flu_heritability")

day_15<-read.table(file="flu15_16_loadings.txt",sep="\t",header=TRUE)
day_19<-read.table(file="flu19_20_loadings.txt",sep="\t",header=TRUE)
day_25<-read.table(file="flu25_26_loadings.txt",sep="\t",header=TRUE)
day_31<-read.table(file="flu31_32_loadings.txt",sep="\t",header=TRUE)

day_15<-day_15[,c(2,3,7:9)]
day_15$dap<-rep(15, nrow(day_15))
day_19<-day_19[,c(2,3,7:9)]
day_19$dap<-rep(19, nrow(day_19))
day_25<-day_25[,c(2,3,7:9)]
day_25$dap<-rep(25, nrow(day_25))
day_31<-day_31[,c(2,3,7:9)]
day_31$dap<-rep(31, nrow(day_31))

flu_signal<-rbind(day_15, day_19, day_25, day_31)

all_days<-sort(unique(flu_signal$dap))
days_to_test<-all_days

variance_table<-c()
for (i in 1:length(days_to_test)) {
  d<-days_to_test[i]  
  H2<-c()
  r2<-c()
  e2<-c()
  gxe2<-c()
  
  for(j in 3:5) {
    flu<-flu_signal[flu_signal$dap == d & flu_signal$treatment >30 ,c(1,2,j)]
    cc.flu<-flu[complete.cases(flu),]
    model<-lmer(cc.flu[,3]~1+(1|genotype)+(1|treatment)+(1|genotype:treatment), data=cc.flu)
    re<-as.numeric(VarCorr(model))
    res<-attr(VarCorr(model), "sc")^2
    
    gxe.var<-re[1]
    g.var<-re[2]
    e.var<-re[3]
    tot.var<-sum(re, res)
    
    h<-g.var/tot.var
    e<-e.var/tot.var
    r<-res/tot.var
    gxe<-gxe.var/tot.var
    
    H2<-c(H2,h)
    e2<-c(e2,e)
    r2<-c(r2,r)
    gxe2<-c(gxe2, gxe)
  }
  
  variance<-rbind(H2, e2, gxe2, r2)
  variance<-cbind(variance, rep(d, nrow(variance)))
  colnames(variance)<-c(colnames(flu_signal)[3:5], 'DAP')
  rownames(variance)<-c('Genotype', 'Treatment', 'G x Treatment', 'Residual')
  
  variance_table<-rbind(variance_table, variance)
  
}


flu.signal.var.table<-cbind(round(variance_table[,1:3]*100,1),variance_table[,4])
colnames(flu.signal.var.table)[c(1,2,3,4)]<-c("FLU.PC1", "FLU.PC2", "FLU.PC3", "day")


write.table(flu.signal.var.table, file='flu.signal.var.table.csv', append=F, quote=F, sep=",", row.names=T, col.names=NA)

###
# Do same thing for VIS color
###

setwd("/Users/mfeldman/Desktop/current_phenotyping/burnin2/color_heritability")

day_15<-read.table(file="allday15_16_scores.txt",sep="\t",header=TRUE)
day_19<-read.table(file="allday19_20_scores.txt",sep="\t",header=TRUE)
day_25<-read.table(file="allday25_26_scores.txt",sep="\t",header=TRUE)
day_31<-read.table(file="allday31_32_scores.txt",sep="\t",header=TRUE)

day_15<-day_15[,c(2,3,6:8)]
day_15$dap<-rep(15, nrow(day_15))
day_19<-day_19[,c(2,3,6:8)]
day_19$dap<-rep(19, nrow(day_19))
day_25<-day_25[,c(2,3,6:8)]
day_25$dap<-rep(25, nrow(day_25))
day_31<-day_31[,c(2,3,6:8)]
day_31$dap<-rep(31, nrow(day_31))

vis_color<-rbind(day_15, day_19, day_25, day_31)

all_days<-sort(unique(vis_color$dap))
days_to_test<-all_days

variance_table<-c()
for (i in 1:length(days_to_test)) {
  d<-days_to_test[i]  
  H2<-c()
  r2<-c()
  e2<-c()
  gxe2<-c()
  
  for(j in 3:5) {
    vis<-vis_color[vis_color$dap == d & vis_color$treatment >30 ,c(1,2,j)]
    cc.vis<-vis[complete.cases(vis),]
    model<-lmer(cc.vis[,3]~1+(1|genotype)+(1|treatment)+(1|genotype:treatment), data=cc.vis)
    re<-as.numeric(VarCorr(model))
    res<-attr(VarCorr(model), "sc")^2
    
    gxe.var<-re[1]
    g.var<-re[2]
    e.var<-re[3]
    tot.var<-sum(re, res)
    
    h<-g.var/tot.var
    e<-e.var/tot.var
    r<-res/tot.var
    gxe<-gxe.var/tot.var
    
    H2<-c(H2,h)
    e2<-c(e2,e)
    r2<-c(r2,r)
    gxe2<-c(gxe2, gxe)
  }
  
  variance<-rbind(H2, e2, gxe2, r2)
  variance<-cbind(variance, rep(d, nrow(variance)))
  colnames(variance)<-c(colnames(vis_color)[3:5], 'DAP')
  rownames(variance)<-c('Genotype', 'Treatment', 'G x Treatment', 'Residual')
  
  variance_table<-rbind(variance_table, variance)
  
}


vis.color.var.table<-cbind(round(variance_table[,1:3]*100,1),variance_table[,4])
colnames(vis.color.var.table)[1:4]<-c("RGB.PC1", "RGB.PC2", "RGB.PC3","day")

write.table(vis.color.var.table, file='vis.color.var.table.csv', append=F, quote=F, sep=",", row.names=T, col.names=NA)



