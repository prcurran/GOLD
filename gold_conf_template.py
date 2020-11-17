

def template(autoscale, crystal_ligand, actives, decoys, dump_dir, protein, constraints):
    return f"""
  GOLD CONFIGURATION FILE

  AUTOMATIC SETTINGS
autoscale = {autoscale}

  POPULATION
popsiz = auto
select_pressure = auto
n_islands = auto
maxops = auto
niche_siz = auto

  GENETIC OPERATORS
pt_crosswt = auto
allele_mutatewt = auto
migratewt = auto

  FLOOD FILL
radius = 6
origin = 0 0 0
do_cavity = 0
floodfill_atom_no = 0
cavity_file = {crystal_ligand}
floodfill_center = cavity_from_ligand

  DATA FILES
ligand_data_file {actives} 5
ligand_data_file {decoys} 5
param_file = DEFAULT
set_ligand_atom_types = 1
set_protein_atom_types = 0
directory = {dump_dir}
tordist_file = DEFAULT
make_subdirs = 0
save_lone_pairs = 1
fit_points_file = fit_pts.mol2
read_fitpts = 0

  FLAGS
internal_ligand_h_bonds = 0
flip_free_corners = 0
match_ring_templates = 0
flip_amide_bonds = 0
flip_planar_n = 1 flip_ring_NRR flip_ring_NHR
flip_pyramidal_n = 0
rotate_carboxylic_oh = flip
use_tordist = 1
postprocess_bonds = 1
rotatable_bond_override_file = DEFAULT
solvate_all = 1

  TERMINATION
early_termination = 1
n_top_solutions = 3
rms_tolerance = 1.5

  CONSTRAINTS
force_constraints = 0

  COVALENT BONDING
covalent = 0

  SAVE OPTIONS
save_score_in_file = 1 comments
save_protein_torsions = 1
concatenated_output = {dump_dir}/docked_ligands.mol2
output_file_format = MOL2

  FITNESS FUNCTION SETTINGS
initial_virtual_pt_match_max = 3
relative_ligand_energy = 1
gold_fitfunc_path = goldscore
score_param_file = DEFAULT

  PROTEIN DATA
protein_datafile = {protein}

  CONSTRAINTS
{constraints}
"""
