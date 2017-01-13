#!/usr/bin/env python

import sys
import numpy as np
from cogue.interface.vasp_io import read_poscar
from cogue.crystal.supercell import estimate_supercell_matrix

# count=1; for i in `cat id-nums.dat|awk '{print $2}'`;do python estimate_smat.py BPOSCAR-$i $count $i; count=$((count+1)); done |tee smat.dat

cell = read_poscar(sys.argv[1])
supercell_matrix = estimate_supercell_matrix(cell, 150)
diagval = tuple(np.diagonal(supercell_matrix))
count = int(sys.argv[2])
mid = int(sys.argv[3])
print("%4d%7d%3d%3d%3d" % ((count, mid) + diagval))
