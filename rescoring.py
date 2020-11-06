import argparse
import os
from collections import OrderedDict

import numpy as np
import pandas as pd
from ccdc.io import EntryReader, EntryWriter, MoleculeReader, MoleculeWriter

from hotspots.grid_extension import Grid
from hotspots.hs_io import HotspotReader


def augmentation(hr, entries):
    # create a grid which can contain all docking poses
    coords = set()
    for i, entry in enumerate(entries):
        for atm in entry.molecule.heavy_atoms:
            coords.add(atm.coordinates)
        if i > 100:
            break

    small_blank = Grid.initalise_grid(coords=coords,
                                      padding=12)
    # dilate the grids
    # for p, g in hr.super_grids.items():
    #     hr.super_grids[p] = g.dilate_by_atom()

    # inflate
    prot_g = Grid.initalise_grid([a.coordinates for a in hr.protein.heavy_atoms], padding=1)

    for p, g in hr.super_grids.items():
        hr.super_grids[p] = prot_g.common_boundaries(g)

    # shrink hotspot maps to save time
    sub_grids = {p: Grid.shrink(small=small_blank, big=g)
                 for p, g in hr.super_grids.items()}

    # create single grid
    mask_dic, sg = Grid.get_single_grid(sub_grids)

    hr.super_grids = mask_dic

    # set background to 1
    hr.set_background()
    hr.normalize_to_max()
    return hr


def score(hr, entry):
    scores_by_type = hr.score_atoms_as_spheres(entry.molecule)
    entry.attributes = scores_by_type
    return np.mean([scores_by_type[p] for p in hr.super_grids.keys()])


def deduplicate(ordered_dic):
    seen = []
    removes = []
    for key, value in ordered_dic.items():
        # molecule number
        f = key.identifier.split("|")[1]
        cnt = key.identifier.split("|")[3]
        tag = f"{f}_{cnt}"
        if tag not in seen:
            seen.append(tag)
        else:
            removes.append(key)

    for remove in removes:
        ordered_dic.pop(remove)

    return ordered_dic


def activity_tag(identifier):
    if "ZINC" in identifier:
        return 0
    else:
        return 1


class Runner(argparse.ArgumentParser):
    def __init__(self):
        super(self.__class__, self).__init__(description=__doc__)

        self.add_argument(
            'docked_mols',
            help='path to docking solutions to be rescored'
        )
        self.add_argument(
            'hotspot_path',
            help='path to hotspot for rescoring'
        )
        self.add_argument(
            '-i', '--hotspot_identifier', default='hotspot',
            help='hotspot identifier'
        )

        self.args = self.parse_args()

    def run(self):
        #  inputs
        with HotspotReader(self.args.hotspot_path) as reader:
            hr = [h for h in reader.read() if h.identifier == self.args.hotspot_identifier][0]

        with MoleculeReader(self.args.docked_mols) as reader:
            out = os.path.join(os.path.dirname(self.args.docked_mols), "results_no_dummy.mol2")
            with MoleculeWriter(out) as writer:
                for mol in reader:
                    for atm in mol.atoms:
                        if atm.atomic_symbol == "Unknown":
                            mol.remove_atom(atm)
                    writer.write(mol)

        self.args.docked_mols = out
        entires = EntryReader(self.args.docked_mols)

        #  outputs
        out_dir = os.path.join(os.path.dirname(self.args.docked_mols))
        print(out_dir)
        #  process
        hr = augmentation(hr, entires)

        # 1) rescore
        rescored = {e: score(hr, e) for e in entires}
        ordered_rescored = OrderedDict(sorted(rescored.items(), key=lambda item: item[1], reverse=True))

        # 2) deduplicate: retain highest ranked pose only
        out_dic = deduplicate(ordered_rescored)
        # 3) output to dataframe ready for ccdc.descriptors API
        df = pd.DataFrame({"identifier": [e.identifier for e in out_dic.keys()],
                           "score": list(out_dic.values()),
                           "activity": [activity_tag(e.identifier) for e in out_dic.keys()]
                           })

        df.to_csv(os.path.join(out_dir, "rescored.csv"))

        with EntryWriter(os.path.join(out_dir, "rescored.sdf")) as w:
            for e in out_dic.keys():
                w.write(e)


if __name__ == "__main__":
    runner = Runner()
    runner.run()
