#!/usr/bin/env python

import sys
import yaml
from datetime import date
from cogue import symmetry as get_symmetry
from cogue.interface.vasp_io import read_poscar
from cogue.crystal.utility import klength2mesh
from cogue.crystal.converter import atoms2cell
from phonopy import Phonopy
from phonopy.interface.vasp import read_vasp
from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
import matplotlib
matplotlib.use('Agg')            
# matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams.update({'figure.figsize': (5, 3)})
import matplotlib.pyplot as plt

phonon_info = yaml.load(open("phonon.yaml"))
cell = read_vasp("POSCAR-unitcell")
phonon = Phonopy(cell,
                 phonon_info['supercell_matrix'],
                 is_auto_displacements=False)
force_sets = parse_FORCE_SETS()
phonon.set_displacement_dataset(force_sets)
phonon.produce_force_constants()

# born = [[[1.08703, 0, 0],
#          [0, 1.08703, 0],
#          [0, 0, 1.08703]],
#         [[-1.08672, 0, 0],
#          [0, -1.08672, 0],
#          [0, 0, -1.08672]]]
# epsilon = [[2.43533967, 0, 0],
#            [0, 2.43533967, 0],
#            [0, 0, 2.43533967]]
# factors = 14.400
# phonon.set_nac_params({'born': born,
#                        'factor': factors,
#                        'dielectric': epsilon})

cogue_cell = atoms2cell(cell)
mesh = klength2mesh(100, cogue_cell.get_lattice())

phonon.set_mesh(mesh)
# phonon.set_thermal_properties(t_step=10, t_max=2000, t_min=0)
phonon.set_total_DOS(tetrahedron_method=True)
freqs, dos = phonon.get_total_DOS()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(freqs, dos, 'r-')
xlim = ax.get_xlim()
ylim = ax.get_ylim()
aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
ax.set_aspect(aspect * 0.5)

plt.xlabel("Frequency (THz)")
plt.ylabel("Phonon DOS (States/THz$\cdot$unitcell)")
plt.savefig("dos.png")
