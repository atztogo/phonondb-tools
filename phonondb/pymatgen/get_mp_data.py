#!/usr/bin/env python

from pymatgen import MPRester
import numpy as np
import sys

mid = int(sys.argv[1])

m = MPRester()
resutls = m.query(criteria={"task_id": "mp-%d" % mid},
                  properties=["band_gap",
                              "created_at",
                              "e_above_hull",
                              "elasticity",
                              "exp_lattice",
                              "final_structure",
                              "icsd_id",
                              "icsd_ids",
                              "initial_structure",
                              "is_hubbard",
                              "nsites",
                              "spacegroup",
                              "pretty_formula",
                              "magnetic_type"])

for data in resutls:
    for key in data:
        if 'initial_structure' == key or 'final_structure' == key or 'exp_lattice' == key:
            print key, ":",
            try:
                data_str = data[key].as_dict()
                print data_str
            except:
                print "None"
        else:
            print key, ":", data[key]
