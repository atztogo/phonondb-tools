#!/usr/bin/env python

from pymatgen import MPRester
import numpy as np
import sys

def run(all_mids):
    m = MPRester()
    for i, mid in enumerate(all_mids):
        with open("mp-%d.dat" % mid, 'w') as w:
            print("mp-%d (%d/%d)" % (mid, i + 1, len(all_mids)))
            lines = get_mp_data_lines(mid, m)
            w.write("\n".join(lines))

def get_mp_data_lines(mid, m):
    resutls = m.query(criteria={"task_id": "mp-%d" % mid},
                      properties=["band_gap",
                                  "created_at",
                                  "e_above_hull",
                                  "elasticity",
                                  "elements",
                                  "energy",
                                  "energy_per_atom",
                                  "exp_lattice",
                                  "final_structure",
                                  "formation_energy_per_atom",
                                  "hubbards",
                                  "icsd_id",
                                  "icsd_ids",
                                  "incar",
                                  "kpoints",
                                  "initial_structure",
                                  "is_hubbard",
                                  "magnetic_type",
                                  "nelements",
                                  "nsites",
                                  "spacegroup",
                                  "pretty_formula",
                                  "total_magnetization",
                                  "unit_cell_formula",
                                  "volume"])

    lines = []
    for data in resutls:
        for key in data:
            if ('initial_structure' == key or
                'final_structure' == key or
                'exp_lattice' == key):
                try:
                    data_str = data[key].as_dict()
                except:
                    data_str = "None"
            else:
                data_str = data[key]
            lines.append("%s : %s" % (key, data_str))

    return lines


try: # One integer mp number
    mid = int(sys.argv[1])
    run([mid,])
except ValueError: # A file obtained by get_all_materialsIDs.py
    with open(sys.argv[1]) as f:
        mids = [int(x.split('-')[1]) for x in f]
        run(mids)
