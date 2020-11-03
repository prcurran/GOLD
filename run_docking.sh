#!/bin/bash
conda activate hotspots

for target in 'akt1' 'ampc' 'cp3a4' 'cxcr4' 'gcr' 'hivpr' 'hivrt' 'kif11'
do
  nohup python docking.py "/local/pcurran/diverse/${target}" > "${target}_dock.out" 2> "${target}_dock.err" &
done
