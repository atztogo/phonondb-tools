#!/usr/bin/env python

import numpy as np
import sys

import argparse

parser = argparse.ArgumentParser(description="Show unit cell volume")
parser.add_argument("-n", "--no_break",
                    help="No line break",
                    action="store_false")
parser.add_argument("-m", "--max_num_atoms",
                    help="Max number of atoms to show",
                    type=int,
                    default=10)
parser.add_argument('filenames', nargs='*')
args = parser.parse_args()

f = open(args.filenames[0])

def distribution_num_atoms():
    num_atoms = np.zeros(1000, dtype=int)
    
    for line in f:
        vals = line.split()
        num_atom = int(vals[1])
        num_atoms[num_atom] += 1
    
    sum = 0
    for i, j in enumerate(num_atoms):
        sum += j
        print i, j, sum

def ratio_basis_vector_lengths(max_num_atom):
    for line in f:
        vals = line.split()
        abc = [float(x) for x in vals[4:7]]
        angles = [float(x) for x in vals[7:10]]
        spgnum = int(vals[3])
        max_ratio = max(abc) / min(abc)
        if int(vals[1]) <= max_num_atom and max_ratio < 2.1 and spgnum > 15:
            print vals[0], vals[1], max_ratio

ratio_basis_vector_lengths(args.max_num_atoms)
