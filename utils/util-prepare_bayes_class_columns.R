#! Rscript
# Command-line script to convert seqential class rgb data to columns of classes
# Input:
#   fn = relative path to file with class rgb values in a single column
#
# File contents should look like this. No numbers in class names:
# Plant
# 0,255,0
# Background
# 255,255,255
# Necrosis
# 255,0,0
#
# Example: Rscript --vanilla util-prepare_bayes_class_columns.R "data/naive_bayes_training/bayes_rgb.tsv"

# Get command line arguments
args = commandArgs(trailingOnly = T)

fn = args[1]

#read each line of file
raw = readLines(fn)
# find lines with letters
hdr = grep("[[:alpha:]]",raw)
# add an additional entry for the last line in the file so we can keep our logic onsistent below
hdr_end = c(hdr,length(raw)+1)

# read chunks of file per class into named list
rgb=list()
for(i in seq_along(hdr)){
  j=i+1
  rgb[[i]] = raw[(hdr_end[i]+1):(hdr_end[j]-1)]
}
names(rgb) <- raw[hdr]

# find the max number of entries in a class and append empty string ('') to each list so lengths are the same
maxrows = max(sapply(rgb,length))
for(i in seq_along(rgb)){
  addnrows = maxrows-length(rgb[[i]])
  rgb[[i]] = c(rgb[[i]],rep('',addnrows))
}

# save dataframe of list as tab delimited file with columns
write.table(as.data.frame(rgb), file.path(dirname(fn),'bayes_rgb_trainingclasses.tsv'), row.names=F, sep='\t', quote = F)
