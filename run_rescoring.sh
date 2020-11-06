#!/bin/bash
conda activate hotspots

#'akt1'
for target in 'ampc' 'cp3a4' 'cxcr4' 'gcr' 'hivrt' 'hivpr' 'kif11'
do
  for run in 'vanilla_scale_10'
  do
#  python rescoring.py "/home/pcurran/github_packages/GOLD/${target}/gold_results/test/docked_ligand.mol2" \
#                      "/home/pcurran/github_packages/GOLD/${target}/hotspot_pharmacophore/out.zip"
    nohup python rescoring.py "/local/pcurran/diverse/${target}/gold_results/${run}/docked_ligand.mol2" \
                        "/local/pcurran/diverse/${target}/hotspot_pharmacophore/out.zip" \
                        > "logs/${target}_rescore.out" 2> "logs/${target}_rescore.err" &

  done
done
