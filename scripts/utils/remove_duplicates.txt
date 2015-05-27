#!/bin/bash

awk '{print $1}' vis_sv_z500_boundary_data.tab | sort -n | uniq -c | awk '{if($1>1){print $2}}'

awk '{print $1}' vis_sv_z500_vis_shapes.tab | sort -n | uniq -c | awk '{if($1>1){print $2}}' > shapes_z500_sv_duplicate_ids.txt

awk 'FNR==NR{id[$1];next} {if($1 in id == 0){print $0}}' boundary_data_z500_sv_duplicate_ids.txt vis_sv_z500_boundary_data.tab > no-dup_vis_sv_z500_boundary_data.tab