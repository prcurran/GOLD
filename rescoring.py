import argparse
import os
from collections import OrderedDict

import numpy as np
import pandas as pd
from ccdc.io import MoleculeReader
from hotspots.grid_extension import Grid
from hotspots.hs_io import HotspotReader


def augmentation(hr, mols):
    # create a grid which can contain all docking poses
    coords = set()
    for i, mol in enumerate(mols):
        for atm in mol.heavy_atoms:
            coords.add(atm.coordinates)
        if i > 100:
            break

    small_blank = Grid.initalise_grid(coords=coords,
                                      padding=12)
    # dilate the grids
    for p, g in hr.super_grids.items():
        hr.super_grids[p] = g.dilate_by_atom()

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


def score(hr, mol):
    scores_by_type = hr.score_atoms_as_spheres(mol)
    return np.mean([scores_by_type[p] for p in hr.super_grids.keys()])


def deduplicate(ordered_dic):
    seen = []
    removes = []
    for key, value in ordered_dic.items():
        tag = key.split("|")[0]
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

        mols = MoleculeReader(self.args.docked_mols)
        print(len(mols))
        #  outputs
        out_path = os.path.join(os.path.dirname(self.args.docked_mols), "rescored.csv")

        #  process
        hr = augmentation(hr, mols)

        # 1) rescore
        rescored = {mol.identifier: score(hr, mol) for mol in mols}
        ordered_rescored = OrderedDict(sorted(rescored.items(), key=lambda item: item[1], reverse=True))

        # 2) deduplicate: retain highest ranked pose only
        out_dic = deduplicate(ordered_rescored)

        # 3) output to dataframe ready for ccdc.descriptors API
        df = pd.DataFrame({"identifier": list(out_dic.keys()),
                           "score": list(out_dic.values()),
                           "activity": [activity_tag(ident) for ident in out_dic.keys()]
                           })

        print(df)
        df.to_csv(out_path)


if __name__ == "__main__":
    runner = Runner()
    runner.run()
