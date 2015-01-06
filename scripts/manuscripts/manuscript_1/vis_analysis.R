# Script for analysis of VIS image analysis and water data
library(ggplot2)
library(lubridate)
library(qvalue)
library(MASS)
library(plyr)

dir = '~/Google\ Drive/Phenotyping/Manuscripts/data/R'
setwd(dir)

########################################################################################
# VIS zoom correction
########################################################################################
# Read data for a reference object imaged at different zoom levels
z.data = read.table(file="zoom_calibration_data.txt", sep="\t", header=TRUE)

# Calculate px per cm
z.data$px_cm = z.data$length_px / z.data$length_cm

############################################
# Zoom correction for area
############################################
# Fit a variety of regression models to relative object area by zoom level
# Test whether an exponential or 2nd order polynomial model fits best (lowest AIC)

# Non-linear regression (exponential)
area.coef = coef(nls(log(rel_area) ~ log(a * exp(b * zoom)), z.data, start = c(a = 1, b = 0.01)))
area.coef = data.frame(a=area.coef[1], b=area.coef[2])
area.nls = nls(rel_area ~ a * exp(b * zoom), data = z.data, start=c(a=area.coef$a, b=area.coef$b))
summary(area.nls)

# Non-linear regression (polynomial)
area.pol = lm(rel_area ~ zoom + I(zoom^2), z.data)
summary(area.pol)

# AIC
AIC(area.nls, area.pol)

# Plot exponential model
pdf(file="model_area_zoom_nls.pdf",width=6,height=6,useDingbats = FALSE)
ggplot(z.data, aes(x=zoom, y=rel_area)) +
  geom_point(size=4) +
  scale_x_continuous(lim=c(0,4000), "Camera zoom setting") +
  scale_y_continuous(lim=c(0,16), "Reference object relative pixel area") +
  stat_smooth(data=z.data, aes(x=zoom, y=rel_area), method="nls", se=FALSE, formula=y ~ a * exp(b * x), start=c(a=area.coef$a, b=area.coef$b)) +
  theme_bw() +
  theme(axis.title.x=element_text(face="bold"),
        axis.title.y=element_text(face="bold"))
dev.off()

############################################
# Zoom correction for length
############################################
# Fit a variety of regression models to px/cm by zoom level
# Test whether an exponential or 2nd order polynomial model fits best (lowest AIC)

# Non-linear regression (exponential)
len.coef = coef(nls(log(px_cm) ~ log(a * exp(b * zoom)), z.data[z.data$camera == 'VIS SV',], start = c(a = 1, b = 0.01)))
len.coef = data.frame(a=len.coef[1], b=len.coef[2])
len.nls = nls(px_cm ~ a * exp(b * zoom), data = z.data[z.data$camera == 'VIS SV',], start=c(a=len.coef$a, b=len.coef$b))
summary(len.nls)

# Length zoom correction using a 2 order polynomial (px/cm given a zoom setting)
len.poly = lm(px_cm ~ zoom + I(zoom^2), data=z.data[z.data$camera == 'VIS SV',])
summary(len.poly)

# AIC
AIC(len.nls, len.poly)

# Plot
pdf(file="model_pxcm_zoom_lmpoly.pdf",width=6,height=6,useDingbats = FALSE)
ggplot(z.data[z.data$camera == 'VIS SV',], aes(x=zoom, y=px_cm)) +
  geom_point(size=4) +
  scale_x_continuous(lim=c(0,4000), "Camera zoom setting") +
  scale_y_continuous(lim=c(0,50), "Reference object length scale (px/cm)") +
  stat_smooth(data=z.data[z.data$camera == 'VIS SV',], aes(x=zoom, y=px_cm), method="lm", formula=y ~ x + I(x^2)) +
  theme_bw() +
  theme(axis.title.x=element_text(face="bold"),
        axis.title.y=element_text(face="bold"))
dev.off()

########################################################################################
# Height modeling
########################################################################################
ht.data = read.table(file="height_model_data.txt",sep="\t",header=TRUE)

## Convert pixel traits to cm with zoom correction
# px/cm calibration
px_cm = (0.00000217 * (ht.data$zoom ** 2)) + (0.002077 * ht.data$zoom) + 14.27

ht.data$height_above_bound_cm = ht.data$height_above_bound / px_cm

# Height model
height.model = lm(manual_height~height_above_bound_cm, ht.data)
summary(height.model)

# Plot height model
pdf(file="height.heightAboveBoundsCM_zoomColored.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(ht.data, aes(x=height_above_bound_cm, y=manual_height)) +
  geom_point(aes(color=factor(zoom)),size=3) +
  geom_smooth(method="lm",formula=y~x) +
  scale_x_continuous(lim=c(0,120), "Estimated height (cm)") +
  scale_y_continuous(lim=c(0,100), "Manually measured height (cm)") +
  theme_bw() +
  theme(legend.position=c(0.2,0.8),
        axis.title.x=element_text(face="bold"),
        axis.title.y=element_text(face="bold"))
dev.off()

########################################################################################
# Biomass modeling
########################################################################################
# Read data
st.data = read.table(file='biomass_model_data.txt', sep="\t", header=TRUE, stringsAsFactors=FALSE)

# Create outlier indicator variable
st.data$outind = NA
st.data[st.data$out_of_frame == T,]$outind = 1
st.data[st.data$out_of_frame == F,]$outind = 0

# Genotype indicator variable
st.data$group = NA
st.data[st.data$genotype == 'A10',]$group = 0
st.data[st.data$genotype == 'B100',]$group = 1

############################################
# Fresh-weight biomass
############################################
# Full model
fw.full = lm(fresh_weight ~ sv_area * tv_area * height_above_bound, st.data)

# Step-wise model selection with AIC
fw.step = stepAIC(fw.full, direction="both")
summary(fw.step)

# AIC model
fw.aic = lm(fresh_weight ~ sv_area + tv_area + height_above_bound + sv_area*height_above_bound, st.data)
summary(fw.aic)

# The AIC model contains tv_area and height which does not have a significant coefficient, test dropping
fw.red = lm(fresh_weight ~ sv_area, st.data)
summary(fw.red)

# Goodness of fit
anova(fw.aic, fw.red)

# SV area model
sv.model = lm(fresh_weight ~ sv_area, st.data)
summary(sv.model)

# Plot SV model
pdf(file="fresh_weight.sv_area.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=fresh_weight)) +
  geom_smooth(method="lm", color="black", formula = y ~ x) +
  geom_point(size=4) +
  theme_bw()
dev.off()

# SV area model with out-of-bounds
sv.ind.model = lm(fresh_weight ~ sv_area + outind, st.data)
summary(sv.ind.model)

# Plot SV model with out-of-bouns groups
pdf(file="fresh_weight.sv_area.out_of_bounds.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=fresh_weight,group=out_of_bounds,color=out_of_bounds)) +
  geom_point(size=4) +
  stat_smooth(method="lm",se=FALSE) +
  theme(legend.position=c(0.2,0.8))
dev.off()

# SV area model with out-of-bounds
sv.gt.model = lm(fresh_weight ~ sv_area + genotype, st.data)
summary(sv.gt.model)

# Plot SV model with genotypes
pdf(file="fresh_weight.sv_area.genotype.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=fresh_weight,group=group,color=group)) +
  geom_point(size=4) +
  stat_smooth(method="lm",se=FALSE) +
  theme(legend.position=c(0.2,0.8))
dev.off()

############################################
# Dry-weight biomass
############################################
# SV area model
dry.sv.model = lm(dry_weight ~ sv_area, st.data)
summary(dry.sv.model)

# Plot SV model
pdf(file="dry_weight.sv_area.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=dry_weight)) +
  geom_smooth(method="lm", color="black", formula = y ~ x) +
  geom_point(size=4) +
  theme_bw()
dev.off()

# SV area model with out-of-bounds
dry.sv.ind.model = lm(dry_weight ~ sv_area + outind, st.data)
summary(dry.sv.ind.model)

# Plot SV model with out-of-bouns groups
pdf(file="dry_weight.sv_area.out_of_bounds.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=dry_weight,group=out_of_bounds,color=out_of_bounds)) +
  geom_point(size=4) +
  stat_smooth(method="lm",se=FALSE) +
  theme(legend.position=c(0.2,0.8))
dev.off()

# SV area model with out-of-bounds
dry.sv.gt.model = lm(dry_weight ~ sv_area + genotype, st.data)
summary(dry.sv.gt.model)

# Plot SV model with genotypes
pdf(file="dry_weight.sv_area.genotype.pdf",height=6,width=6,useDingbats=FALSE)
ggplot(st.data,aes(x=sv_area,y=dry_weight,group=group,color=group)) +
  geom_point(size=4) +
  stat_smooth(method="lm",se=FALSE) +
  theme(legend.position=c(0.2,0.8))
dev.off()

########################################################################################
# Analyze VIS data
########################################################################################
############################################
# Read data and format for analysis
############################################
# Planting date
planting_date = as.POSIXct("2013-11-26")

# Read VIS data
vis.data = read.table(file="vis_snapshots.txt",sep=",",header=TRUE)

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

# Remove sampled plants
vis.data = vis.data[!vis.data$plant_id %in% st.data$barcode,]

# Group
vis.data$group = paste(vis.data$genotype,'-',vis.data$treatment,sep='')

# Date-time from Unix time
vis.data$date = as.POSIXct(vis.data$datetime, origin = "1970-01-01")

# Days after planting
vis.data$dap = as.numeric(vis.data$date - planting_date)

# Predict biomass from linear model
vis.data$fw_biomass = predict.lm(object = sv.model, newdata=vis.data)
vis.data$dw_biomass = predict.lm(object = dry.sv.model, newdata=vis.data)

############################################
# Plant height
############################################
# Height plotting function
plot_height = function(vis.data, genotype) {
  # Plot command
  hplot = ggplot(vis.data[vis.data$genotype==genotype & (vis.data$treatment == 100 | vis.data$treatment == 33),], aes(x=dap, y=height_above_bound, color=factor(treatment))) +
            #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
            geom_point(size=3) +
            geom_smooth(method="loess",size=1) +
            scale_x_continuous(name="Days after planting") +
            scale_y_continuous(lim=c(0,120),breaks=c(0,20,40,60,80,100,120),name="Estimated height (cm)") +
            theme_bw() +
            theme(legend.position=c(0.2,0.8),
                  axis.title.x=element_text(face="bold"),
                  axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste(genotype, "_height_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(hplot)
  dev.off()
}

# Plot height of each genotype
for(genotype in levels(factor(vis.data$genotype))) {
  plot_height(vis.data, genotype)
}

# Statistical analysis
analyze_height = function(vis.data, genotype) {
  days = c()
  diff.low = c()
  diff.up = c()
  pvals = c()
  for(day in levels(factor(as.integer(vis.data$dap)))) {
    day = as.integer(day)
    #control = vis.data[as.integer(vis.data$dap) == day & vis.data$genotype == genotype & vis.data$treatment == 100,]$height_above_bound
    #drought = vis.data[as.integer(vis.data$dap) == day & vis.data$genotype == genotype & vis.data$treatment == 33,]$height_above_bound
    control = vis.data[(as.integer(vis.data$dap) == day | as.integer(vis.data$dap) == day + 1) & vis.data$genotype == genotype & vis.data$treatment == 100,]$height_above_bound
    drought = vis.data[(as.integer(vis.data$dap) == day | as.integer(vis.data$dap) == day + 1) & vis.data$genotype == genotype & vis.data$treatment == 33,]$height_above_bound
    test = t.test(x=control,y=drought)
    days = c(days,day)
    diff.low = c(diff.low,test$conf.int[1])
    diff.up = c(diff.up,test$conf.int[2])
    pvals = c(pvals,test$p.value)
  }
  #qvals = qvalue(pvals)
  #results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals,qvalue=qvals$qvalues)
  results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals)
  return(results)
}

# Test for treatment effect on two-day intervals
a10.height.results = analyze_height(vis.data, 'A10')
b100.height.results = analyze_height(vis.data, 'B100')

# Control for multiple testing by controlling the FDR
qvalues.height = qvalue(c(a10.height.results$pvalue, b100.height.results$pvalue))
a10.height.results$qvalue = qvalues.height$qvalues[1:nrow(a10.height.results)]
b100.height.results$qvalue = qvalues.height$qvalues[(nrow(a10.height.results)+1):(nrow(a10.height.results) + nrow(b100.height.results))]

# Assign genotypes for merged table
a10.height.results$genotype = 'A10'
b100.height.results$genotype = 'B100'

# Output the A10 and B100 tables to the same file
write.table(a10.height.results, file='height.stats.csv', sep = ',', row.names = FALSE, append = FALSE)
write.table(b100.height.results, file='height.stats.csv', sep = ',', row.names = FALSE, append = TRUE, col.names = FALSE)

# Height plotting function by treatment
plot_height_treatment = function(vis.data, treatment) {
  # Plot command
  hplot = ggplot(vis.data[vis.data$treatment == treatment,], aes(x=dap, y=height_above_bound, color=factor(genotype))) +
    #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(lim=c(0,120),breaks=c(0,20,40,60,80,100,120),name="Estimated height (cm)") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste("water",treatment, "all_genotypes_height_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(hplot)
  dev.off()
}

# Plot height of each genotype
for(treatment in levels(factor(vis.data$treatment))) {
  plot_height_treatment(vis.data, treatment)
}

############################################
# Response to drought - height
############################################
drought_response_height = function(vis.data, genotypes) {
  # Initialize drought response data frame with days
  drought_resp = data.frame(day=c(min(as.integer(vis.data$dap)):max(as.integer(vis.data$dap))))
  
  # Initialize genotypes
  for(g in genotypes) {
    control = paste(g,'control',sep='')
    drought = paste(g,'drought',sep='')
    
    # Calculate median biomass per treatment per day
    drought_resp[,paste(control)] = 0
    drought_resp[,paste(drought)] = 0
    for(d in min(as.integer(vis.data$dap)):max(as.integer(vis.data$dap))) {
      drought_resp[drought_resp$day == d, paste(control)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 100 & as.integer(vis.data$dap) == d,]$height_above_bound)
      drought_resp[drought_resp$day == d, paste(drought)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 33 & as.integer(vis.data$dap) == d,]$height_above_bound)
    }
  }
  drought_resp = drought_resp[-14,]
  
  # Calculate biomass loss to drought
  days = c()
  response = c()
  genotype=c()
  for(r in 1:nrow(drought_resp)) {
    days = c(days, rep(drought_resp[r,]$day,length(genotypes)))
    for(g in genotypes) {
      control = paste(g,'control',sep='')
      drought = paste(g,'drought',sep='')
      response = c(response, drought_resp[r,paste(drought)] - drought_resp[r,paste(control)])
      genotype = c(genotype, g)
    }
  }
  dr.df = data.frame(day=days,response=response,genotype=as.factor(genotype))
  
  # Plot results
  resp = ggplot(dr.df, aes(x=day,y=response,group=genotype,colour=genotype)) +
    geom_point(size=4) +
    geom_smooth(method="loess") +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(name="Height loss to drought (cm)") +
    theme_bw() +
    theme(legend.position=c(0.8,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  pdf(file=paste(paste(genotypes,collapse='_'),"_height_responseDrought_dap.pdf",sep=''),height=6,width=6,useDingbats=FALSE)
  print(resp)
  dev.off()
  return(dr.df)
}

# A10 vs B100 drought responses
drought.response.height.parents = drought_response_height(vis.data,c('A10','B100'))
drought.response.height.all = drought_response_height(vis.data,c('A10','B100','R20','R70','R98','R102','R128','R133','R161','R187'))

############################################
# Height variation per day
############################################
height_per_day = function(vis.data) {
  dap = c()
  genotype = c()
  int.low = c()
  int.up = c()
  est = c()
  
  # Loop through each day and genotype
  for(d in min(as.integer(vis.data$dap)):max(as.integer(vis.data$dap))) {
    if(d != 24) {
      for(g in levels(factor(vis.data$genotype))) {
        #m = median(vis.data[vis.data$genotype == g & vis.data$treatment == 100 & as.integer(vis.data$dap) == d,]$height_above_bound)
        h.data = vis.data[vis.data$genotype == g & vis.data$treatment == 100 & as.integer(vis.data$dap) == d,]$height_above_bound
        if(sd(h.data) != 0) {
          dap = c(dap,d)
          genotype = c(genotype,g)
          test = t.test(h.data)
          int.low = c(int.low,test$conf.int[1])
          int.up = c(int.up,test$conf.int[2])
          est = c(est,test$estimate)
        }
      }
    }
  }
  #drought_resp = drought_resp[-14,]
  results = data.frame(dap=as.numeric(dap),genotype=genotype,conf.int.low=int.low,conf.int.up=int.up,mean=est)  

  return(results)
}

# Height per day 95% CI
height.perday.results = height_per_day(vis.data)
write.csv(height.perday.results,file="height.perday.100water.csv")

############################################
# Biomass analysis
############################################
# Biomass plotting function
plot_biomass = function(vis.data, genotype, predicted=TRUE) {
  # Plot predicted biomass
  if (predicted==TRUE) {
    bplot = ggplot(vis.data[vis.data$genotype==genotype & (vis.data$treatment == 100 | vis.data$treatment == 33),], aes(x=dap, y=fw_biomass, color=factor(treatment))) +
                scale_y_continuous(lim=c(-1,41), name="Estimated biomass (g)")
  } else {
    bplot = ggplot(vis.data[vis.data$genotype==genotype & (vis.data$treatment == 100 | vis.data$treatment == 33),], aes(x=dap, y=sv_area, color=factor(treatment))) +
                scale_y_continuous(lim=c(0,1e6), name="Estimated biomass (px)")
  }
  # Plot command
  bplot = bplot + geom_point(size=3) +
                  geom_smooth(method="loess",size=1) +
                  scale_x_continuous(name="Days after planting") +
                  #scale_y_continuous(lim=c(0,1e6), name="Estimated biomass (px)") +
                  theme_bw() +
                  theme(legend.position=c(0.2,0.8),
                  axis.title.x=element_text(face="bold"),
                  axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste(genotype,"_biomass_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(bplot)
  dev.off()
}

# Plot biomass for each genotype
for(genotype in levels(factor(vis.data$genotype))) {
  plot_biomass(vis.data, genotype, predicted = TRUE)
}

# Statistical analysis
analyze_biomass = function(vis.data, genotype) {
  days = c()
  diff.low = c()
  diff.up = c()
  pvals = c()
  for(day in levels(factor(as.integer(vis.data$dap)))) {
    day = as.integer(day)
    #control = vis.data[as.integer(vis.data$dap) == day & vis.data$genotype == genotype & vis.data$treatment == 100,]$sv_area
    #drought = vis.data[as.integer(vis.data$dap) == day & vis.data$genotype == genotype & vis.data$treatment == 33,]$sv_area
    control = vis.data[(as.integer(vis.data$dap) == day | as.integer(vis.data$dap) == day + 1) & vis.data$genotype == genotype & vis.data$treatment == 100,]$fw_biomass
    drought = vis.data[(as.integer(vis.data$dap) == day | as.integer(vis.data$dap) == day + 1) & vis.data$genotype == genotype & vis.data$treatment == 33,]$fw_biomass
    # If the control group has a lot more replicates (e.g. A10 and B100), randomly sample to drought sample size
    if (genotype == 'A10' | genotype == 'B100') {
      control = sample(control, size = length(drought))
    }
    test = t.test(x=control,y=drought)
    days = c(days,day)
    diff.low = c(diff.low,test$conf.int[1])
    diff.up = c(diff.up,test$conf.int[2])
    pvals = c(pvals,test$p.value)
  }
  #qvals = qvalue(pvals, pi0.method="bootstrap")
  #results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals,qvalue=qvals$qvalues)
  results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals)
  return(results)
}

# Test for treatment effect on two-day intervals
a10.biomass.results = analyze_biomass(vis.data, 'A10')
b100.biomass.results = analyze_biomass(vis.data, 'B100')

# Control for multiple testing by controlling the FDR
qvalues.biomass = qvalue(c(a10.biomass.results$pvalue, b100.biomass.results$pvalue))
a10.biomass.results$qvalue = qvalues.biomass$qvalues[1:nrow(a10.biomass.results)]
b100.biomass.results$qvalue = qvalues.biomass$qvalues[(nrow(a10.biomass.results)+1):(nrow(a10.biomass.results) + nrow(b100.biomass.results))]

# Assign genotypes for merged table
a10.biomass.results$genotype = 'A10'
b100.biomass.results$genotype = 'B100'

# Output the A10 and B100 tables to the same file
write.table(a10.biomass.results, file='biomass.stats.csv', sep = ',', row.names = FALSE, append = FALSE)
write.table(b100.biomass.results, file='biomass.stats.csv', sep = ',', row.names = FALSE, append = TRUE, col.names = FALSE)

############################################
# Response to drought - biomass
############################################
drought_response = function(vis.data, genotypes) {
  # Initialize drought response data frame with days
  drought_resp = data.frame(day=c(min(as.integer(vis.data$dap)):max(as.integer(vis.data$dap))))
  
  # Initialize genotypes
  for(g in genotypes) {
    control = paste(g,'control',sep='')
    drought = paste(g,'drought',sep='')
    
    # Calculate median biomass per treatment per day
    drought_resp[,paste(control)] = 0
    drought_resp[,paste(drought)] = 0
    for(d in min(as.integer(vis.data$dap)):max(as.integer(vis.data$dap))) {
      #drought_resp[drought_resp$day == d, paste(control)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 100 & as.integer(vis.data$dap) == d,]$sv_area)
      #drought_resp[drought_resp$day == d, paste(drought)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 33 & as.integer(vis.data$dap) == d,]$sv_area)
      drought_resp[drought_resp$day == d, paste(control)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 100 & as.integer(vis.data$dap) == d,]$fw_biomass)
      drought_resp[drought_resp$day == d, paste(drought)] = median(vis.data[vis.data$genotype == g & vis.data$treatment == 33 & as.integer(vis.data$dap) == d,]$fw_biomass)
    }
  }
  drought_resp = drought_resp[-14,]
  
  # Calculate biomass loss to drought
  days = c()
  response = c()
  genotype=c()
  for(r in 1:nrow(drought_resp)) {
    days = c(days, rep(drought_resp[r,]$day,length(genotypes)))
    for(g in genotypes) {
      control = paste(g,'control',sep='')
      drought = paste(g,'drought',sep='')
      response = c(response, drought_resp[r,paste(drought)] - drought_resp[r,paste(control)])
      genotype = c(genotype, g)
    }
  }
  dr.df = data.frame(day=days,response=response,genotype=as.factor(genotype))
  
  # Plot results
  resp = ggplot(dr.df, aes(x=day,y=response,group=genotype,colour=genotype)) +
            geom_point(size=4) +
            geom_smooth(method="loess") +
            scale_x_continuous(name="Days after planting") +
            scale_y_continuous(name="Reduced accumulated biomass (g)") +
            theme_bw() +
            theme(legend.position=c(0.8,0.8),
                  axis.title.x=element_text(face="bold"),
                  axis.title.y=element_text(face="bold"))
  pdf(file=paste(paste(genotypes,collapse='_'),"_responseDrought_dap.pdf",sep=''),height=6,width=6,useDingbats=FALSE)
  print(resp)
  dev.off()
  return(dr.df)
}

# A10 vs B100 drought responses
drought.response.parents = drought_response(vis.data,c('A10','B100'))
drought.response.all = drought_response(vis.data,c('A10','B100','R20','R70','R98','R102','R128','R133','R161','R187'))

# Biomass plotting function by treatment
plot_biomass_treatment = function(vis.data, treatment) {
  # Plot command
  bplot = ggplot(vis.data[vis.data$treatment == treatment,], aes(x=dap, y=sv_area, color=factor(genotype))) +
    #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(name="Estimated biomass (px)") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste("water",treatment, "all_genotypes_biomass_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(bplot)
  dev.off()
}

# Plot biomass of each genotype
for(treatment in levels(factor(vis.data$treatment))) {
  plot_biomass_treatment(vis.data, treatment)
}

########################################################################################
# Water use efficiency
########################################################################################
############################################
# Read data and format for analysis
############################################
# Read water data
water.data = read.table(file="B2_watering_data_phenofront.csv",sep=",",header=TRUE)

# Remove the empty pot controls
water.data = water.data[grep('000A',water.data$plant.barcode, invert = TRUE),]

# Remove snapshots that were not valid waterings (water.amount = -1)
water.data = water.data[water.data$water.amount != -1,]

# Treatment column
water.data$treatment <- NA
water.data$treatment[grep("AA", water.data$plant.barcode)] <- 100
water.data$treatment[grep("AB", water.data$plant.barcode)] <- 0
water.data$treatment[grep("AC", water.data$plant.barcode)] <- 16
water.data$treatment[grep("AD", water.data$plant.barcode)] <- 33
water.data$treatment[grep("AE", water.data$plant.barcode)] <- 66

# Plant genotype column
water.data$genotype <- NA
water.data$genotype[grep("p1", water.data$plant.barcode)] <- 'A10'
water.data$genotype[grep("p2", water.data$plant.barcode)] <- 'B100'
water.data$genotype[grep("r1", water.data$plant.barcode)] <- 'R20'
water.data$genotype[grep("r2", water.data$plant.barcode)] <- 'R70'
water.data$genotype[grep("r3", water.data$plant.barcode)] <- 'R98'
water.data$genotype[grep("r4", water.data$plant.barcode)] <- 'R102'
water.data$genotype[grep("r5", water.data$plant.barcode)] <- 'R128'
water.data$genotype[grep("r6", water.data$plant.barcode)] <- 'R133'
water.data$genotype[grep("r7", water.data$plant.barcode)] <- 'R161'
water.data$genotype[grep("r8", water.data$plant.barcode)] <- 'R187'

# Group
water.data$group = paste(water.data$genotype,'-',water.data$treatment,sep='')

# Convert timestamp to a Date
water.data$timestamp = ymd_hms(water.data$timestamp)

# Days after planting
water.data$dap = as.numeric(water.data$timestamp - planting_date)

# Some plants were removed from the system but were not inactivated
bad.cars = unique(water.data$car.tag[water.data$water.amount >120 & water.data$dap > 14])
water.data = water.data[!water.data$car.tag %in% bad.cars,]

# Water figure (S.viridis water)
sv.water = water.data[(water.data$treatment == 100 | water.data$treatment == 33) & water.data$genotype == 'A10',]

# Classify water job as early or later in the day
sv.water$early.late <- NA  #restrict to the scheduled watering later in the run
sv.water$early.late[hour(sv.water$timestamp) < 7] <- 'early'
sv.water$early.late[hour(sv.water$timestamp) < 15 & hour(sv.water$timestamp) > 11 ] <- 'late'
sv.water = sv.water[!is.na(sv.water$early.late),]
sv.water$dap = day(sv.water$timestamp) + 4
sv.water = sv.water[sv.water$dap > 14,]

water.plot = ggplot(sv.water, aes(y = water.amount, x = dap, group = factor(interaction(early.late,treatment,dap)),fill = factor(interaction(early.late, treatment)),color = factor(interaction(early.late, treatment)))) +
  geom_boxplot(outlier.colour = NULL) +
  scale_x_continuous("Days after planting") +
  scale_y_continuous("Water volume (ml)") +
  theme_bw() +
  theme(legend.position = c(0.2,0.8),
        axis.title.x=element_text(face="bold"),
        axis.title.y=element_text(face="bold"))

pdf(file = "BI2_watering_A10_watercomp_boxplots_clean_dap.pdf", useDingbats=FALSE, width=2.0014, height=2.5708)
print(water.plot)
dev.off()

# WUE function
wue = function(water, biomass, genotype) {
  # WUE data vectors
  dap.list = c()
  plant.list = c()
  water.list = c()
  biomass.list = c()
  treatment.list = c()
  
  # Get unique barcodes for biomass
  barcodes = unique(biomass[biomass$genotype==genotype & (biomass$treatment == 100 | biomass$treatment == 33),]$plant_id)
  for(barcode in barcodes) {
    snapshots = biomass[biomass$plant_id==barcode,]
    snapshots = snapshots[with(snapshots, order(dap)),]
    for(row in 1:nrow(snapshots)) {
      total.water = sum(water[water$dap <= snapshots[row,]$dap & water$plant.barcode == barcode,]$water.amount)
      
      dap.list = c(dap.list, snapshots[row,]$dap)
      plant.list = c(plant.list, barcode)
      water.list = c(water.list, total.water)
      #biomass.list = c(biomass.list, snapshots[row,]$sv_area)
      biomass.list = c(biomass.list, snapshots[row,]$fw_biomass)
      treatment.list = c(treatment.list, snapshots[row,]$treatment)
    }
  }
  
  wue.data = data.frame(plant_id=plant.list,dap=dap.list,water=water.list,biomass=biomass.list,treatment=treatment.list)
  return(wue.data)
}

# Statistical analysis on two-day increments
analyze_wue = function(wue.data) {
  days = c()
  diff.low = c()
  diff.up = c()
  pvals = c()
  for(day in levels(factor(as.integer(wue.data$dap)))) {
    day = as.integer(day)
    #control = wue.data[as.integer(wue.data$dap) == day & wue.data$treatment == 100,]
    #drought = wue.data[as.integer(wue.data$dap) == day & wue.data$treatment == 33,]
    control = wue.data[(as.integer(wue.data$dap) == day | as.integer(wue.data$dap) == day + 1) & wue.data$treatment == 100,]
    drought = wue.data[(as.integer(wue.data$dap) == day | as.integer(wue.data$dap) == day + 1) & wue.data$treatment == 33,]
    control.wue = control$biomass / control$water
    drought.wue = drought$biomass / drought$water
    test = t.test(x=control.wue,y=drought.wue)
    days = c(days,day)
    diff.low = c(diff.low,test$conf.int[1])
    diff.up = c(diff.up,test$conf.int[2])
    pvals = c(pvals,test$p.value)
  }
  #qvals = qvalue(pvals)
  #results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals,qvalue=qvals$qvalues)
  results = data.frame(dap=as.numeric(days),conf.int.low=diff.low,conf.int.up=diff.up,pvalue=pvals)
  return(results)
}

# Analyze WUE for each genotype and aggregate results
wue.results = data.frame()
for(genotype in levels(factor(water.data$genotype))) {
  genotype.wue = wue(water.data, vis.data, genotype)
  genotype.wue = genotype.wue[genotype.wue$water != 0,]
  print(max(genotype.wue$biomass/genotype.wue$water))
  genotype.wue.results = analyze_wue(genotype.wue)
  genotype.wue.results$genotype = genotype
  wue.results = rbind(wue.results, genotype.wue.results)
  
  wue.plot = ggplot(genotype.wue, aes(x=dap, y=(biomass/water)*1000, color=factor(treatment))) +
                #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
                geom_point(size=3) +
                geom_smooth(method="loess",size=1) +
                scale_x_continuous(name="Days after planting") +
                scale_y_continuous(lim=c(-2.1,26), name="Water-use efficiency (mg/mL)") +
                theme_bw() +
                theme(legend.position=c(0.2,0.8),
                      axis.title.x=element_text(face="bold"),
                      axis.title.y=element_text(face="bold"))
  pdf(file=paste(genotype,"_cumulative_WUE.pdf",sep=''),height=6,width=6,useDingbats=FALSE)
  print(wue.plot)
  dev.off()
}
# Control for multiple testing by controlling the FDR
qvalues.wue = qvalue(wue.results$pvalue)
wue.results$qvalue = qvalues.wue$qvalues
write.table(wue.results, file='wue.stats.csv', sep=',', row.names=FALSE)

############################################
# Height-width ratio
############################################
# Calculate height-width ratio
vis.data$height_width_ratio = vis.data$height_above_bound / vis.data$extent_x

# Plot height-width ratio 
plot_heightwidth_ratio = function(vis.data, genotype) {
  # Plot command
  hwplot = ggplot(vis.data[vis.data$genotype==genotype & (vis.data$treatment == 100 | vis.data$treatment == 33) & vis.data$dap > 17,], aes(x=dap, y=height_width_ratio, color=factor(treatment))) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(lim=c(0, 3), name="Height-width ratio") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste(genotype, "_height-width_ratio_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(hwplot)
  dev.off()
}

# Plot height-width ratio of each genotype
for(genotype in levels(factor(vis.data$genotype))) {
  plot_heightwidth_ratio(vis.data, genotype)
}

# Plot spreadratio of each treatment for parents
# 100% FC
hw100.plot = ggplot(vis.data[(vis.data$genotype == 'A10' | vis.data$genotype == 'B100') & vis.data$treatment == 100 & vis.data$dap > 17,], aes(x=dap, y=height_width_ratio, color=factor(genotype), size=24)) +
  #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
  geom_point(size=3) +
  geom_smooth(method="loess",size=1) +
  scale_x_continuous(name="Days after planting") +
  scale_y_continuous(lim=c(0,2.5), name="Height-width ratio") +
  theme_bw() +
  theme(legend.position=c(0.2,0.8),
        axis.title.x=element_text(face="bold", size=24),
        axis.title.y=element_text(face="bold", size=24))

# Save file
pdf(file="A10.100_vs_B100.100_height-width_ratio_dap.pdf", height=6, width=6, useDingbats=FALSE)
print(hw100.plot)
dev.off()

# 33% FC
hw33.plot = ggplot(vis.data[(vis.data$genotype == 'A10' | vis.data$genotype == 'B100') & vis.data$treatment == 33 & vis.data$dap > 17,], aes(x=dap, y=height_width_ratio, color=factor(genotype), size=24)) +
  #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
  geom_point(size=3) +
  geom_smooth(method="loess",size=1) +
  scale_x_continuous(name="Days after planting") +
  scale_y_continuous(lim=c(0,2.5), name="Height-width ratio") +
  theme_bw() +
  theme(legend.position=c(0.2,0.8),
        axis.title.x=element_text(face="bold", size=24),
        axis.title.y=element_text(face="bold", size=24))

# Save file
pdf(file="A10.33_vs_B100.33_height-width_ratio_dap.pdf", height=6, width=6, useDingbats=FALSE)
print(hw33.plot)
dev.off()

############################################
# Tiller count
############################################
# 200 random images where Tracy counted tillers
tiller.counts = read.table(file="200tiller_counts.txt",sep="\t",header=TRUE)
tiller.counts$date = as.POSIXct(paste(paste(tiller.counts$year,tiller.counts$month,tiller.counts$day,sep='-'), paste(tiller.counts$hours, tiller.counts$minutes, tiller.counts$seconds, sep=':'), sep=' '))

# Merge with VIS table
tiller.counts = merge(x=tiller.counts, y=vis.data, by = 'date')

# Model tiller count
tiller.model.full = lm(ave_tillers~fw_biomass+height_above_bound+solidity+extent_x+height_width_ratio, data=tiller.counts)

# Variance inflation
vif(tiller.model.full)

# Drop height
tiller.model1 = lm(ave_tillers~fw_biomass+solidity+extent_x+height_width_ratio, data=tiller.counts)
vif(tiller.model1)

# Drop extent x
tiller.model2 = lm(ave_tillers~fw_biomass+solidity+height_width_ratio, data=tiller.counts)
vif(tiller.model2)
summary(tiller.model2)

# Drop solidity
tiller.model3 = lm(ave_tillers~fw_biomass+height_width_ratio, data=tiller.counts)

# Partial regression
pdf(file="tiller_count_avPlot.pdf", height=3, width=6, useDingbats=FALSE)
avPlots(model = tiller.model3, pch=16)
dev.off()

# Predict tiller count for another set
tiller660 = read.table(file="660tiller_counts.txt",sep="\t",header=TRUE)
tiller660 = merge(x=tiller660, y=vis.data, by='datetime')
tiller660$predicted_tiller_count = predict.lm(object = tiller.model3, newdata=tiller660)

# Plot manual versus predicted tiller counts
pdf(file="model_tiller_count_220set.pdf", height=6, width=6, useDingbats=FALSE)
ggplot(data=tiller660, aes(x=tiller_count, y=predicted_tiller_count)) +
  geom_point(size=4) +
  geom_abline(intercept=0, slope=1) +
  #geom_abline(intercept=3, slope=1) +
  #geom_abline(intercept=-3, slope=1) +
  scale_x_continuous(lim=c(0,14), "Manual tiller count") +
  scale_y_continuous(lim=c(0,14), "Predicted tiller count") +
  theme_bw() +
  theme(axis.title.x=element_text(face="bold"),
        axis.title.y=element_text(face="bold"))
dev.off()

# Median prediction interval
predict.var = tiller660.predict[,3]-tiller660.predict[,1]
predict.var = c(predict.var, tiller660.predict[,1] - tiller660.predict[,2])
median(predict.var)

# Median difference from actual
median(abs(tiller660$tiller_count - tiller660$predicted_tiller_count))

# Predict for whole data set
vis.data$tiller_count = predict.lm(object = tiller.model3, newdata = vis.data)

# Tiller plotting function
plot_tillers = function(vis.data, genotype) {
  # Plot command
  tplot = ggplot(vis.data[vis.data$genotype==genotype & (vis.data$treatment == 100 | vis.data$treatment == 33),], aes(x=dap, y=tiller_count, color=factor(treatment))) +
    #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(lim=c(0,12), name="Estimated tiller count") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste(genotype, "_tillers_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(tplot)
  dev.off()
}

# Plot height of each genotype
for(genotype in levels(factor(vis.data$genotype))) {
  plot_tillers(vis.data, genotype)
}


# Tiller plotting function by treatment
plot_tiller_treatment = function(vis.data, treatment) {
  # Plot command
  tplot = ggplot(vis.data[vis.data$treatment == treatment,], aes(x=dap, y=tiller_count, color=factor(genotype))) +
    #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(lim=c(0,12),name="Estimated tiller count") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste("water",treatment, "all_genotypes_tillers_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(tplot)
  dev.off()
}

# Plot height of each genotype
for(treatment in levels(factor(vis.data$treatment))) {
  plot_tiller_treatment(vis.data, treatment)
}

plot_tiller_parents = function(vis.data, treatment) {
  # Plot command
  tplot = ggplot(vis.data[vis.data$treatment == treatment & (vis.data$genotype == 'A10' | vis.data$genotype == 'B100'),], aes(x=dap, y=tiller_count, color=factor(genotype))) +
    #geom_line(aes(color=factor(treatment),group=plant_id),size=1) +
    geom_point(size=3) +
    geom_smooth(method="loess",size=1) +
    scale_x_continuous(name="Days after planting") +
    scale_y_continuous(lim=c(0,12),name="Estimated tiller count") +
    theme_bw() +
    theme(legend.position=c(0.2,0.8),
          axis.title.x=element_text(face="bold"),
          axis.title.y=element_text(face="bold"))
  
  # Save file
  pdf(file=paste("water",treatment, "parents_tillers_dap.pdf", sep=''), height=6, width=6, useDingbats=FALSE)
  print(tplot)
  dev.off()
}

########################################################################################
# Trait table
########################################################################################
# Export all of the VIS traits (except color)
h.table = vis.data
#h.table$height_width_ratio = h.table$height_above_bound / h.table$extent_x
h.table$plant_id = as.character(h.table$plant_id)
h.table$wue = NA
for(r in 1:nrow(h.table)) {
  row = h.table[r,]
  total.water = sum(water.data[water.data$dap <= row$dap & water.data$plant.barcode == row$plant_id,]$water.amount)
  h.table[r,]$wue = row$sv_area / total.water
}
write.table(h.table,file="vis.traits.csv",quote=FALSE,sep=",",row.names=FALSE)

