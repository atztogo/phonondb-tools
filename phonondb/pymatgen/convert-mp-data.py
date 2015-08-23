#!/usr/bin/env python

import sys
import numpy as np
from ast import literal_eval
from cogue import cell as make_cell
from cogue import symmetry as make_symmetry
from cogue.crystal.symmetry import get_crystallographic_cell
from cogue.interface.vasp_io import write_poscar

def get_band_gap(strval, show=False):
    band_gap = float(strval)
    if show:
        print "[Band gap]"
        print float(strval)
    return band_gap

def get_icsd_id(strval, show=False):
    if strval == "None":
        icsd_id = None
    else:
        icsd_id = int(strval)
    if show:
        print "[ICSD ID]"
        print icsd_id
    return icsd_id

def get_icsd_ids(strval, show=False):
    icsd_ids = literal_eval(strval)    
    if show:
        print "[ICSD IDs]"
        print icsd_ids
    return icsd_ids

def get_e_above_hull(strval, show=False):
    e_above_hull = float(strval)
    if show:
        print "[Energy above hull]"
        print e_above_hull
    return e_above_hull

def get_pretty_formula(strval, show=False):
    if show:
        print "[Formula]"
        print strval
    return strval

def get_created_at(strval, show=False):
    if show:
        print "[Created data]"
        print strval
    return strval

def get_is_hubbard(strval, show=False):
    if strval == "False":
        is_hubbard = False
    else:
        is_hubbard = True
    if show:
        print "[Is Hubbard-U used?]"
        is_hubbard
    return is_hubbard

def get_nsites(strval, show=False):
    nsites = int(strval)
    if show:
        print "[Number of atomic sites]"
        print nsites
    return nsites

def get_elasticity(strval, show=False):
    elasticity = literal_eval(strval)    
    if show:
        print "[Elastic constants]"
        print elasticity
    return elasticity

def get_final_structure(strval, show=False):
    if show:
        print "[Final structure]"
    cell = _show_structure(strval, show=show)
    if show:
        print make_symmetry(cell, tolerance=1e-1)['international']
    return cell

def get_initial_structure(strval, show=False):
    if show:
        print "[Initial structure]"
    cell = _show_structure(strval, show=show)
    if show:
        print make_symmetry(cell, tolerance=1e-1)['international']
    return cell

def _show_structure(strval, show=False):
    val = literal_eval(strval)
    lattice = val['lattice']['matrix']
    for key in val['lattice'].keys():
        if show:
            print key, ":", val['lattice'][key]

    symbols = []
    points = []
    for site in val['sites']:
        s, p = _show_site(site, show=show)
        symbols.append(s)
        points.append(p)
    return make_cell(lattice=np.transpose(lattice),
                     points=np.transpose(points),
                     symbols=symbols)

def _show_site(site, show=False):
    symbol = site['label']
    point = site['abc']
    if show:
        print symbol, point,
        if site['properties']:
            print site['properties']['forces']
        else:
            print 
    return symbol, point

def get_spacegroup(strval, show=False):
    val = literal_eval(strval)
    if show:
        print "[Space group]"
        for key in val.keys():
            print key, ":",  val[key]
    return val

def get_magnetic_type(strval, show=False):
    if show:
        print "[Magnetic type]"
        print strval
    return strval

def get_exp_lattice(strval, show=False):
    print "[Exp. lattice]"
    val = literal_eval(strval)
    print np.array(val['matrix'])
    print "(a, b, c, alpha, beta, gamma) ="
    print "(%f, %f, %f, %f, %f, %f)" % (
        (val['a'], val['b'], val['c'], val['alpha'], val['beta'], val['gamma']))

functions_all = {'band_gap': get_band_gap,
                 'icsd_id': get_icsd_id,
                 'icsd_ids': get_icsd_ids,
                 'e_above_hull': get_e_above_hull,
                 'pretty_formula': get_pretty_formula,
                 'created_at': get_created_at,
                 'is_hubbard': get_is_hubbard,
                 'nsites': get_nsites,
                 'elasticity': get_elasticity,
                 'final_structure': get_final_structure,
                 'initial_structure': get_initial_structure,
                 'icsd_id': get_icsd_id,
                 'spacegroup': get_spacegroup,
                 'magnetic_type': get_magnetic_type,
                 'exp_lattice': get_exp_lattice}

functions = {'band_gap': get_band_gap,
             'e_above_hull': get_e_above_hull,
             'is_hubbard': get_is_hubbard,
             'final_structure': get_final_structure,
             'initial_structure': get_initial_structure,
             'magnetic_type': get_magnetic_type}

mid = sys.argv[2]
for line in open(sys.argv[1]):
    words = line.partition(':')
    key = words[0].strip()
    if key in functions:
        if key == 'final_structure':
            retval = functions[key](words[2].strip(), show=False)
            brv_cell = get_crystallographic_cell(retval, tolerance=1e-1)
            write_poscar(brv_cell, filename="BPOSCAR-%s" % mid)
