#!/bin/bash
conda activate hotspots
export GOLD_DIR="/local/pcurran/CCDC/Discovery_2020/GOLD"

#'ampc' 'cp3a4' 'cxcr4' 'gcr' 'hivpr' 'hivrt' 'kif11'
for target in 'akt1'
do
  python pharmacophore_docking.py "/home/pcurran/github_packages/GOLD/${target}" 10 1 "test" "hotspot_pharmacophore/3.cm"

done