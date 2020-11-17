#!/bin/bash
conda activate hotspots
export GOLD_DIR="/local/pcurran/CCDC/Discovery_2020/GOLD"

# 'akt1''cp3a4' 'cxcr4' 'gcr' 'hivpr' 'hivrt' 'kif11'
for target in 'ampc'
do
#   "ligand_pharmacophores"
  for map in "hotspot_pharmacophore"
  do
    for num in {3..3}
    do
#      parent score autoscale run_id crossminer_file
      python pharmacophore_docking.py "/local/pcurran/diverse/${target}" \
         10 0.1 "${map}_num_${num}_scale_10_score_10" "${map}/${num}.cm"

#      nohup python pharmacophore_docking.py "/local/pcurran/diverse/${target}" \
#       10 0.1 "${map}_num_${num}_scale_10_score_10" "${map}/${num}.cm"\
#        > "logs/${target}_${map}.out" 2>"logs/${target}_${map}.err" &

    done
  done
done