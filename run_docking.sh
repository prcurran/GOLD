#!/bin/bash
conda activate hotspots
export GOLD_DIR="/local/pcurran/CCDC/Discovery_2020/GOLD"

#'ampc' 'cp3a4' 'cxcr4' 'gcr' 'hivpr' 'hivrt' 'kif11'
for target in 'akt1'
do
  python docking.py "/home/pcurran/github_packages/GOLD/${target}" 10 1 "test"
#   nohup python docking.py "/local/pcurran/diverse/${target}" 0 100 "vanilla" \
#   > "${target}_dock.out" 2> "${target}_dock.err" &
#  nohup python docking.py "/local/pcurran/diverse/${target}" 0 10 "vanilla_scale_10" \
#  > "${target}_dock.out" 2> "${target}_dock.err" &
#  nohup python docking.py "/local/pcurran/diverse/${target}" 50 10 "hotspot_50_scale_10" \
#  > "${target}_dock.out" 2> "${target}_dock.err" &
done
