import sys
import os
from hotspots import hs_io
from hotspots.pharmacophore_extension import HotspotPharmacophoreModel
from gold_conf_template import template
from ccdc.io import MoleculeWriter, MoleculeReader
from ccdc.utilities import PushDir
import shutil


def check_dir(d):
    if not os.path.exists(d):
        os.mkdir(d)
    return d


def run():
    # must be abspath
    parent = sys.argv[1]
    score = sys.argv[2]
    autoscale = sys.argv[3]
    run_id = sys.argv[4]
    crossminer_file = os.path.join(parent, sys.argv[5])

    # data
    conf_name = "hs_gold.conf"
    out_path = check_dir(os.path.join(parent, "gold_results"))
    out_path = check_dir(os.path.join(out_path, run_id))
    junk = check_dir(os.path.join(out_path, "all"))
    hotspot = os.path.join(parent, "hotspot_pharmacophore", "out.zip")
    crystal_ligand = os.path.join(parent, "crystal_ligand.mol2")
    actives = os.path.join(parent, "actives_final.mol2")
    decoys = os.path.join(parent, "decoys_final.mol2")
    prot_file = os.path.join(out_path, "protein.mol2")

    # output protein
    with hs_io.HotspotReader(hotspot) as reader:
        hr = [h for h in reader.read() if h.identifier == "bestvol"][0]

    with MoleculeWriter(prot_file) as w:
        w.write(hr.protein)

    hspm = HotspotPharmacophoreModel.from_file(crossminer_file)
    constraint_str = hspm.to_gold_conf(score=score)

    # create template
    gold_conf_str = template(autoscale, crystal_ligand, actives, decoys, junk, prot_file, constraint_str)
    print(gold_conf_str)
    with open(os.path.join(out_path, conf_name), "w") as w:
        w.write(gold_conf_str)

    #  linux only
    gold_exe = os.path.join(os.environ["GOLD_DIR"], "bin/gold_auto")

    # run docking
    with PushDir(out_path):
        cmd = f"{gold_exe} {conf_name}"
        os.system(cmd)

    # process results
    docked = MoleculeReader(os.path.join(junk, "docked_ligands.mol2"))
    with MoleculeWriter(os.path.join(out_path, "docked_ligands.mol2")) as w:
        for d in docked:
            for atm in d.atoms:
                if atm.atomic_symbol == "Unknown":
                    d.remove_atom(atm)
            w.write(d)

    shutil.copyfile(os.path.join(junk, "bestranking.lst"), os.path.join(out_path, "bestranking.lst"))

    shutil.rmtree(junk)


if __name__ == "__main__":
    run()