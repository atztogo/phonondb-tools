#!/usr/bin/env python

import sys
import glob
import os.path
from datetime import date
from cogue import symmetry as get_symmetry
from cogue.interface.vasp_io import read_poscar_yaml
from cogue.crystal.utility import get_Z

tmpl_index = """Materials id {midstart} - {midend}
====================================================

.. toctree::
   :maxdepth: 2

"""

tmpl_mp = """Materials id {mid} / {pretty_formula} / {contents}
===================================================================

- Date page updated: {date}
- Space group type: {spg}
- Number of formula units (Z): {num_units}
- Phonon raw data: :download:`{filename} <./{filename}>`
- Link to Materials Project: `https://www.materialsproject.org/materials/mp-{mid}/ <https://www.materialsproject.org/materials/mp-{mid}/>`_

"""

citation_mp = """Citation
-----------

.. _the Materials Project: https://www.materialsproject.org/
.. _the Materials Project citation: https://materialsproject.org/citing

The initial crystal structure used to perform phonon calculation is obtained from `the Materials Project`_. More detail about the crystal structure and citation is found at :ref:`crystal_structure_and_citation`.

"""

data_license = """License
--------------

The contents of this web page are licensed under a `Creative Commons 4 Attribution.0
International License <http://creativecommons.org/licenses/by/4.0/>`_.

.. image :: https://i.creativecommons.org/l/by/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by/4.0/
   :alt: license

"""

d = int(sys.argv[1])
files = glob.glob("mp-*-POSCAR.yaml")
numbers = [int(filename.split('.')[0].replace("mp-", "").replace("-POSCAR", "")) for filename in files]
numbers.sort()

# index.rst
with open("index.rst", 'w') as w:
    w.write(tmpl_index.format(midstart="%d000" % d, midend="%d999" % d))
    for num in numbers:
        print num
        w.write("   mp-{num}\n".format(num=num))
        
# mp-{num}.rst
for num in numbers:
    pretty_formula = ""
    with open("/home/togo/autocalc/MP-data/data/mp-%d.dat" % num) as f:
        for line in f:
            if 'pretty_formula' in line:
                pretty_formula = line.split(':')[1].strip()
                break

    cell = read_poscar_yaml("mp-%d-POSCAR.yaml" % num)[0]
    symmetry = get_symmetry(cell)

    dos_filename = "mp-%d-dos.png" % num
    tprops_filename = "mp-%d-tprops.png" % num
    gruneisen_filename = "mp-%d-gruneisen.png" % num
    qha_filename = "mp-%d-qha.png" % num

    with open("mp-%d.rst" % num, 'w') as w:
        today = date.today()
        contents = ""
        if os.path.exists(dos_filename):
            contents += "d"
        else:
            contents += "."
        if os.path.exists(tprops_filename):
            contents += "t"
        else:
            contents += "."
        if os.path.exists(gruneisen_filename):
            contents += "g"
        else:
            contents += "."
        if os.path.exists(qha_filename):
            contents += "q"
        else:
            contents += "."

        w.write(tmpl_mp.format(mid=num,
                               pretty_formula=pretty_formula,
                               contents=contents,
                               spg="%s (%d) / %s" % (symmetry['international'],
                                                     symmetry['number'],
                                                     symmetry['hall']),
                               num_units="%d" % get_Z(cell.get_numbers()),
                               filename="mp-%d.tar.lzma" % num,
                               date="%d-%d-%d" % (today.year,
                                                  today.month,
                                                  today.day)))
    
        if os.path.exists(dos_filename):
            w.write("Phonon DOS\n")
            w.write("-----------\n\n")
            w.write(".. image:: mp-{mid}-dos.png\n\n".format(mid=num))

        if os.path.exists(tprops_filename):
            w.write("Thermal properties at constant volume\n")
            w.write("--------------------------------------\n\n")
            w.write(".. image:: mp-{mid}-tprops.png\n\n".format(mid=num))

        if os.path.exists(gruneisen_filename):
            w.write("Mode Gruneisen parameter\n")
            w.write("-------------------------\n\n")
            w.write(".. image:: mp-{mid}-gruneisen.png\n\n".format(mid=num))

        if os.path.exists(qha_filename):
            w.write("Properties at 0GPa under quasi-harmonic approximation\n")
            w.write("-----------------------------------------------------\n\n")
            w.write(".. image:: mp-{mid}-qha.png\n\n".format(mid=num))
            
        with open("mp-%d-POSCAR.yaml" % num) as f_poscar:
            w.write("POSCAR.yaml\n")
            w.write("----------------\n\n")
            w.write("POSCAR.yaml shows the crystal structure after the relaxation used for this phonon calculation.\n\n")

            w.write("::\n\n")
            for line in f_poscar:
                w.write("   %s" % line)
            w.write("\n\n")

        w.write(citation_mp)

        w.write(data_license)
