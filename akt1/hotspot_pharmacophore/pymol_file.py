
try:
    import tkinter as tk      
except ImportError:
    import Tkinter as tk
from os.path import join
import tempfile

import zipfile
import math
from pymol import cmd, finish_launching, plugins
from pymol.cgo import *

finish_launching()

dirpath = tempfile.mkdtemp()
zip_dir = "out.zip"
wd = os.getcwd()
with zipfile.ZipFile(zip_dir) as hs_zip:
    hs_zip.extractall(dirpath)

os.chdir(dirpath)
cmd.load("hotspot/apolar.grd", "apolar_hotspot")
cmd.isosurface(name="surface_apolar_hotspot", map="apolar_hotspot", level="5")

cmd.color("yellow", "surface_apolar_hotspot")
cmd.set("transparency", 0.2, "surface_apolar_hotspot")
cmd.load("hotspot/donor.grd", "donor_hotspot")
cmd.isosurface(name="surface_donor_hotspot", map="donor_hotspot", level="5")

cmd.color("blue", "surface_donor_hotspot")
cmd.set("transparency", 0.2, "surface_donor_hotspot")
cmd.load("hotspot/acceptor.grd", "acceptor_hotspot")
cmd.isosurface(name="surface_acceptor_hotspot", map="acceptor_hotspot", level="5")

cmd.color("red", "surface_acceptor_hotspot")
cmd.set("transparency", 0.2, "surface_acceptor_hotspot")
cmd.group("hotspot", members="apolar_hotspot")
cmd.group("hotspot", members="surface_apolar_hotspot")
cmd.group("hotspot", members="donor_hotspot")
cmd.group("hotspot", members="surface_donor_hotspot")
cmd.group("hotspot", members="acceptor_hotspot")
cmd.group("hotspot", members="surface_acceptor_hotspot")
cmd.load("hotspot/buriedness.grd", "buriedness_hotspot")
cmd.isosurface(name="surface_buriedness_hotspot", map="buriedness_hotspot", level="3")

cmd.color("gray", "surface_buriedness_hotspot")
cmd.set("transparency", 0.2, "surface_buriedness_hotspot")
cmd.group("hotspot", members="buriedness_hotspot")
cmd.group("hotspot", members="surface_buriedness_hotspot")
cmd.pseudoatom(object="PS_apolar_hotspot_0", pos=(6.0, 3.0, 17.0), color=(1, 1, 1), label=15.2)

cmd.group("label_apolar_hotspot", members="PS_apolar_hotspot_0")
cmd.group("label_apolar_hotspot", members="PS_apolar_hotspot_0")
cmd.pseudoatom(object="PS_donor_hotspot_0", pos=(11.5, 8.5, 22.5), color=(1, 1, 1), label=6.0)

cmd.pseudoatom(object="PS_donor_hotspot_1", pos=(11.0, -1.0, 23.0), color=(1, 1, 1), label=15.0)

cmd.pseudoatom(object="PS_donor_hotspot_2", pos=(10.5, 5.5, 19.0), color=(1, 1, 1), label=14.2)

cmd.pseudoatom(object="PS_donor_hotspot_3", pos=(10.0, -4.5, 21.0), color=(1, 1, 1), label=8.7)

cmd.pseudoatom(object="PS_donor_hotspot_4", pos=(8.5, 3.0, 21.0), color=(1, 1, 1), label=15.0)

cmd.pseudoatom(object="PS_donor_hotspot_5", pos=(8.5, -5.5, 24.0), color=(1, 1, 1), label=9.0)

cmd.pseudoatom(object="PS_donor_hotspot_6", pos=(7.5, 1.0, 18.5), color=(1, 1, 1), label=15.9)

cmd.pseudoatom(object="PS_donor_hotspot_7", pos=(1.5, 2.5, 16.5), color=(1, 1, 1), label=14.0)

cmd.group("label_donor_hotspot", members="PS_donor_hotspot_0")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_0")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_1")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_1")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_2")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_2")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_3")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_3")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_4")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_4")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_5")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_5")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_6")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_6")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_7")
cmd.group("label_donor_hotspot", members="PS_donor_hotspot_7")
cmd.pseudoatom(object="PS_acceptor_hotspot_0", pos=(16.5, -3.5, 20.0), color=(1, 1, 1), label=10.1)

cmd.pseudoatom(object="PS_acceptor_hotspot_1", pos=(14.5, 3.0, 18.5), color=(1, 1, 1), label=8.8)

cmd.pseudoatom(object="PS_acceptor_hotspot_2", pos=(14.0, -2.0, 24.0), color=(1, 1, 1), label=10.4)

cmd.pseudoatom(object="PS_acceptor_hotspot_3", pos=(13.5, 1.0, 22.5), color=(1, 1, 1), label=10.8)

cmd.pseudoatom(object="PS_acceptor_hotspot_4", pos=(11.5, 8.0, 19.5), color=(1, 1, 1), label=10.0)

cmd.pseudoatom(object="PS_acceptor_hotspot_5", pos=(10.5, -3.0, 24.0), color=(1, 1, 1), label=12.4)

cmd.pseudoatom(object="PS_acceptor_hotspot_6", pos=(10.0, -4.5, 18.5), color=(1, 1, 1), label=7.9)

cmd.pseudoatom(object="PS_acceptor_hotspot_7", pos=(7.5, -6.0, 21.0), color=(1, 1, 1), label=8.6)

cmd.pseudoatom(object="PS_acceptor_hotspot_8", pos=(7.0, -7.0, 23.5), color=(1, 1, 1), label=8.7)

cmd.pseudoatom(object="PS_acceptor_hotspot_9", pos=(3.5, 4.5, 16.0), color=(1, 1, 1), label=15.7)

cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_0")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_0")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_1")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_1")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_2")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_2")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_3")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_3")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_4")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_4")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_5")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_5")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_6")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_6")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_7")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_7")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_8")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_8")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_9")
cmd.group("label_acceptor_hotspot", members="PS_acceptor_hotspot_9")
cmd.group("labels_hotspot", members="label_apolar_hotspot")
cmd.group("labels_hotspot", members="label_donor_hotspot")
cmd.group("labels_hotspot", members="label_acceptor_hotspot")
cmd.load("hotspot/protein.pdb", "protein_hotspot")
cmd.show("cartoon", "protein_hotspot")
cmd.hide("line", "protein_hotspot")
cmd.show("sticks", "organic")
cmd.load("bestvol/apolar.grd", "apolar_bestvol")
cmd.isosurface(name="surface_apolar_bestvol", map="apolar_bestvol", level="5")

cmd.color("yellow", "surface_apolar_bestvol")
cmd.set("transparency", 0.2, "surface_apolar_bestvol")
cmd.load("bestvol/donor.grd", "donor_bestvol")
cmd.isosurface(name="surface_donor_bestvol", map="donor_bestvol", level="5")

cmd.color("blue", "surface_donor_bestvol")
cmd.set("transparency", 0.2, "surface_donor_bestvol")
cmd.load("bestvol/acceptor.grd", "acceptor_bestvol")
cmd.isosurface(name="surface_acceptor_bestvol", map="acceptor_bestvol", level="5")

cmd.color("red", "surface_acceptor_bestvol")
cmd.set("transparency", 0.2, "surface_acceptor_bestvol")
cmd.group("bestvol", members="apolar_bestvol")
cmd.group("bestvol", members="surface_apolar_bestvol")
cmd.group("bestvol", members="donor_bestvol")
cmd.group("bestvol", members="surface_donor_bestvol")
cmd.group("bestvol", members="acceptor_bestvol")
cmd.group("bestvol", members="surface_acceptor_bestvol")
cmd.group("bestvol", members="buriedness_bestvol")
cmd.group("bestvol", members="surface_buriedness_bestvol")
cmd.pseudoatom(object="PS_apolar_bestvol_0", pos=(6.5, 4.0, 16.5), color=(1, 1, 1), label=15.3)

cmd.pseudoatom(object="PS_apolar_bestvol_1", pos=(6.0, 2.0, 17.5), color=(1, 1, 1), label=15.3)

cmd.group("label_apolar_bestvol", members="PS_apolar_bestvol_0")
cmd.group("label_apolar_bestvol", members="PS_apolar_bestvol_0")
cmd.group("label_apolar_bestvol", members="PS_apolar_bestvol_1")
cmd.group("label_apolar_bestvol", members="PS_apolar_bestvol_1")
cmd.pseudoatom(object="PS_donor_bestvol_0", pos=(11.0, -1.0, 23.0), color=(1, 1, 1), label=14.9)

cmd.pseudoatom(object="PS_donor_bestvol_1", pos=(10.5, 5.5, 19.0), color=(1, 1, 1), label=14.0)

cmd.pseudoatom(object="PS_donor_bestvol_2", pos=(8.5, 3.0, 21.0), color=(1, 1, 1), label=14.9)

cmd.pseudoatom(object="PS_donor_bestvol_3", pos=(7.5, 1.0, 18.5), color=(1, 1, 1), label=15.6)

cmd.pseudoatom(object="PS_donor_bestvol_4", pos=(1.5, 2.5, 16.5), color=(1, 1, 1), label=13.9)

cmd.group("label_donor_bestvol", members="PS_donor_bestvol_0")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_0")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_1")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_1")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_2")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_2")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_3")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_3")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_4")
cmd.group("label_donor_bestvol", members="PS_donor_bestvol_4")
cmd.pseudoatom(object="PS_acceptor_bestvol_0", pos=(10.5, -3.0, 24.0), color=(1, 1, 1), label=12.3)

cmd.pseudoatom(object="PS_acceptor_bestvol_1", pos=(3.5, 4.5, 16.0), color=(1, 1, 1), label=15.6)

cmd.group("label_acceptor_bestvol", members="PS_acceptor_bestvol_0")
cmd.group("label_acceptor_bestvol", members="PS_acceptor_bestvol_0")
cmd.group("label_acceptor_bestvol", members="PS_acceptor_bestvol_1")
cmd.group("label_acceptor_bestvol", members="PS_acceptor_bestvol_1")
cmd.group("labels_bestvol", members="label_apolar_bestvol")
cmd.group("labels_bestvol", members="label_donor_bestvol")
cmd.group("labels_bestvol", members="label_acceptor_bestvol")
cmd.load("bestvol/protein.pdb", "protein_bestvol")
cmd.show("cartoon", "protein_bestvol")
cmd.hide("line", "protein_bestvol")
cmd.show("sticks", "organic")


class IsoLevel(tk.Variable):
    def __init__(self, master, name, level):
        tk.Variable.__init__(self, master, value=level)
        self.name = name
        self.trace('w', self.callback)

    def callback(self, *args):
        cmd.isolevel(self.name, self.get())

    def increment(self, event=None, delta=0.1):
        self.set(round(float(self.get()) + delta, 2))

    def decrement(self, event=None):
        self.increment(None, -0.1)


surface_list = {'hotspot': {'fhm': ['surface_apolar_hotspot', 'surface_donor_hotspot', 'surface_acceptor_hotspot'], 'buriedness': ['surface_buriedness_hotspot']}, 'bestvol': {'fhm': ['surface_apolar_bestvol', 'surface_donor_bestvol', 'surface_acceptor_bestvol']}}
surface_max_list = {'hotspot': {'fhm': 15.9, 'buriedness': 8}, 'bestvol': {'fhm': 15.6}}

top = tk.Toplevel(plugins.get_tk_root())

master = tk.Frame(top, padx=10, pady=10)
master.pack(fill="both", expand=1)

for child in list(master.children.values()):
    child.destroy()


row_counter = 0
for identifier, component_dic in surface_list.items():
    # add calculation identifier
    tk.Label(master, text=identifier).grid(row=row_counter, column=0, sticky="w")
    row_counter += 1
    
    for component_id, surfaces in component_dic.items():
        # add collection label, e.g. superstar or hotspot etc.
        tk.Label(master, text=component_id).grid(row=row_counter, column=1, sticky='w')
        row_counter += 1
        
        for i, surface in enumerate(surfaces):
            # add grid type label
            probe = surface.split("_")[-2]
            tk.Label(master, text=probe).grid(row=row_counter, column=2, sticky="w")
            
            # slider code 
            v = IsoLevel(master, surface, 5)
            e = tk.Scale(master, orient=tk.HORIZONTAL, from_=0, to=surface_max_list[identifier][component_id],
                         resolution=0.1, showvalue=0, variable=v)
            e.grid(row=row_counter, column=3, sticky="ew")

            e = tk.Entry(master, textvariable=v, width=4)
            e.grid(row=row_counter, column=4, sticky="e")
            master.columnconfigure(3, weight=1)
            row_counter += 1



cmd.bg_color("white")
if wd:
    os.chdir(wd)