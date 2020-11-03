#!/bin/bash
conda activate hotspots

# 'ampc' 'cp3a4' 'cxcr4' 'gcr' 'hivrt' 'kif11'
for target in 'akt1'
do
  python rescoring.py "/local/pcurran/diverse/${target}/gold_results/vanilla/docked_ligand.mol2" \
                      "/local/pcurran/diverse/${target}/hotspot_pharmacophore/out.zip"
#  nohup python rescoring.py "/local/pcurran/diverse/${target}/gold_results/vanilla/docked_ligand.mol2" \
#                      "/local/pcurran/diverse/${target}/hotspot_pharmacophore/out.zip" \
#                      > "logs/${target}_rescore.out" 2> "logs/${target}_rescore.err" &

done
