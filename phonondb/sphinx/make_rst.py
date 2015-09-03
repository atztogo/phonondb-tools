#!/usr/bin/env python

import sys
import glob
import os.path
from datetime import date
from cogue import symmetry as get_symmetry
from cogue.interface.vasp_io import read_poscar_yaml

tmpl_index = """Materials id {midstart} - {midend}
====================================================

.. toctree::
   :maxdepth: 2

"""

tmpl_mp = """Materials id {mid} / {pretty_formula}
===================================================================

- Date page updated: {date}
- Space group type: {spg}
- Raw data: :download:`{filename} <./{filename}>`
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

The contents of this web page are licensed under a `Creative Commons Attribution 4.0
International License <http://creativecommons.org/licenses/by/4.0/>`_.

.. image :: https://i.creativecommons.org/l/by/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by/4.0/
   :alt: license

"""

d = int(sys.argv[1])
files = glob.glob("mp-*.tar.lzma")
numbers = [int(filename.split('.')[0].replace("mp-", "")) for filename in files]
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

    symmetry = get_symmetry(read_poscar_yaml("mp-%d-POSCAR.yaml" % num)[0])

    with open("mp-%d.rst" % num, 'w') as w:
        today = date.today()
        w.write(tmpl_mp.format(mid=num,
                               pretty_formula=pretty_formula,
                               spg="%s (%d) / %s" % (symmetry['international'],
                                                     symmetry['number'],
                                                     symmetry['hall']),
                               filename="mp-%d.tar.lzma" % num,
                               date="%d-%d-%d" % (today.year,
                                                  today.month,
                                                  today.day)))
    
        dos_filename = "mp-%d-dos.png" % num
        if os.path.exists(dos_filename):
            w.write("Phonon DOS\n")
            w.write("-----------\n\n")
            w.write(".. image:: mp-{mid}-dos.png\n\n".format(mid=num))

        tprops_filename = "mp-%d-tprops.png" % num
        if os.path.exists(tprops_filename):
            w.write("Thermal properties at constant volume\n")
            w.write("--------------------------------------\n\n")
            w.write(".. image:: mp-{mid}-tprops.png\n\n".format(mid=num))

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
