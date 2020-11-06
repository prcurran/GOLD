
"""
Example script for the Hotspot API manuscript

The docking example has been adapted from the CCDC API documentation:
    - https://downloads.ccdc.cam.ac.uk/documentation/API/cookbook_examples/docking_examples.html
"""

import gzip
import os
import shutil
from shutil import copyfile
import sys

from ccdc.docking import Docker
from ccdc.io import MoleculeReader, MoleculeWriter
from hotspots.hs_docking import DockerSettings
from hotspots.hs_io import HotspotReader


def dock(inputs):
    """
    submit a GOLD API docking calculation using docking constraints automatically generated from the Hotspot API

    :param ligand_path:
    :param out_path:
    :param hotspot:
    :param weight:
    :return:
    """

    def add_ligands(docker, ligand_path):
        docker.settings.add_ligand_file(os.path.join(ligand_path,
                                                     "actives_final.mol2"),
                                        ndocks=5)

        docker.settings.add_ligand_file(os.path.join(ligand_path,
                                                     "decoys_final.mol2"),
                                        ndocks=5)

    def add_protein(docker, hotspot, junk):

        pfile = os.path.join(junk, "protein.mol2")
        with MoleculeWriter(pfile) as w:
            w.write(hotspot.protein)
        print(pfile)
        docker.settings.add_protein_file(pfile)

    def define_binding_site(docker, ligand_path):

        crystal_ligand = MoleculeReader(os.path.join(ligand_path, "crystal_ligand.mol2"))[0]
        docker.settings.binding_site = docker.settings.BindingSiteFromLigand(protein=docker.settings.proteins[0],
                                                                             ligand=crystal_ligand)

    def add_hotspot_constraint(docker, hotspot, weight):

        if int(weight) != 0:
            constraints = docker.settings.HotspotHBondConstraint.create(protein=docker.settings.proteins[0],
                                                                        hr=hotspot,
                                                                        weight=int(weight),
                                                                        min_hbond_score=0.05,
                                                                        max_constraints=1)

            for constraint in constraints:
                docker.settings.add_constraint(constraint)

    def write(docker, out_path):

        results = Docker.Results(docker.settings)

        # write ligands
        with MoleculeWriter(os.path.join(out_path, "docked_ligand.mol2")) as w:
            for d in results.ligands:
                mol = d.molecule
                # for atm in mol.atoms:
                #     if atm.atomic_symbol == "Unknown":
                #         mol.remove_atom(atm)
                w.write(mol)

        # copy ranking file
        # in this example, this is the only file we use for analysis. However, other output files can be useful.
        copyfile(os.path.join(junk, "bestranking.lst"),
                 os.path.join(out_path, "bestranking.lst"))

    # GOLD docking routine
    ligand_path, out_path, hs_path, weight, search_efficiency = inputs
    docker = Docker()

    # GOLD settings
    docker.settings = DockerSettings()
    docker.settings.fitness_function = 'plp'
    docker.settings.autoscale = search_efficiency
    junk = check_dir(os.path.join(out_path, "all"))
    docker.settings.output_directory = junk

    # GOLD write lots of files we don't need in this example

    docker.settings.output_file = os.path.join(junk, "docked_ligands.mol2")

    # read the hotspot
    with HotspotReader(hs_path) as reader:
        # change if your hotspot is call something else
        hotspot = [h for h in reader.read() if h.identifier == "bestvol"][0]

    # for p, g in hotspot.super_grids.items():
    #     hotspot.super_grids[p] = g.dilate_by_atom()  # dilation to reduce noise

    add_ligands(docker, ligand_path)
    add_protein(docker, hotspot, junk)
    define_binding_site(docker, ligand_path)
    add_hotspot_constraint(docker, hotspot, weight)
    docker.dock(file_name=os.path.join(out_path, "hs_gold.conf"))
    write(docker, out_path)

    # Clean out unwanted files
    shutil.rmtree(junk)


def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def run():

    # must be abspath
    parent = sys.argv[1]
    weight = sys.argv[2]
    search_efficiency = sys.argv[3]
    run_id = sys.argv[4]

    ligand_path = parent
    out_path = check_dir(os.path.join(parent, "gold_results"))
    out_path = check_dir(os.path.join(out_path, run_id))

    hotspot = os.path.join(parent, "hotspot_pharmacophore", "out.zip")

    inputs = (ligand_path, out_path, hotspot, weight, search_efficiency)
    dock(inputs)


if __name__ == "__main__":
    run()