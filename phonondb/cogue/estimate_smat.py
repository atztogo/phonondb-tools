#!/usr/bin/env python

import sys
import numpy as np
from cogue.interface.vasp_io import read_poscar
from cogue.crystal.cell import symbols2formula
from cogue.crystal.supercell import estimate_supercell_matrix

cell = read_poscar(sys.argv[1])
supercell_matrix = estimate_supercell_matrix(cell, 120)
