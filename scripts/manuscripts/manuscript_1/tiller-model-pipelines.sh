#!/bin/bash

#For this script to work it must be executed while you are in the same folder as the tiller-model-pipeline.sh script
#Two inputs are necessary, the first is the path to the images that need to be processed, the second is the folder that you want the output in.

echo $1
echo $2
time="$(date +"%T")"
day="$(date +"%m-%d-%y")"
name="tiller-output-"$day"-"$time
echo $name
mkdir $2/$name
mkdir $2/$name/output-images
cd ../../../
cwd="$PWD"
echo $cwd
cd $2/$name

time $cwd/scripts/image_analysis/image_analysis.pl \
-d $1 \
-p $cwd/scripts/image_analysis/vis_sv/vis_sv_z700_L1.py \
-t vis_sv \
-z 700 \
-s tillertest.sqlite3 \
-i $2/$name/output-images \
-T 10 \
-c \
-f

time $cwd/scripts/image_analysis/image_analysis.pl \
-d $1 \
-p $cwd/scripts/image_analysis/vis_sv/vis_sv_z500_L1.py \
-t vis_sv \
-z 500 \
-s tillertest.sqlite3 \
-i $2/$name/output-images \
-T 10 \
-f

time $cwd/scripts/image_analysis/image_analysis.pl \
-d $1 \
-p $cwd/scripts/image_analysis/vis_sv/vis_sv_z2500_L1.py \
-t vis_sv \
-z 2500 \
-s tillertest.sqlite3 \
-i $2/$name/output-images \
-T 10 \
-f

time $cwd/scripts/image_analysis/image_analysis.pl \
-d $1 \
-p $cwd/scripts/image_analysis/vis_sv/vis_sv_z3500_L1.py \
-t vis_sv \
-z 3500 \
-s tillertest.sqlite3 \
-i $2/$name/output-images \
-T 10 \
-f

