#!/usr/bin/env python

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

tmpl_mp = """Materials id {mid} / {pretty_formula} / {contents}
===================================================================

- Date page updated: {date}
- Space group type: {spg}
- Number of formula units (Z): {num_units}
- Link to Materials Project: `https://www.materialsproject.org/materials/mp-{mid}/ <https://www.materialsproject.org/materials/mp-{mid}/>`_

"""

citation_mp = """Citation
-----------

.. _the Materials Project: https://www.materialsproject.org/
.. _the Materials Project citation: https://materialsproject.org/citing
.. _SeeK-path: http://materialscloud.org/tools/seekpath

.. 

The initial crystal structure used to perform phonon calculation is
obtained from `the Materials Project`_. The phonon band structure
paths are determined using `SeeK-path`_. More details about how to
obtain the crystal structure, how to determine the band structure
paths, and those citations are found at
:ref:`crystal_structure_and_citation`.

"""

data_license = """License
--------------

The contents of this web page are licensed under a `Creative Commons
4.0 Attribution International License
<http://creativecommons.org/licenses/by/4.0/>`_.

.. image :: https://i.creativecommons.org/l/by/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by/4.0/
   :alt: license

"""


def get_mp_numbers(mp_filename):
    """
    The file should contains the lines like below

    mp-10009
    mp-1000
    mp-10070
    mp-10074
    mp-10080
    mp-10096
    mp-10103
    ...
    """

    with open(mp_filename) as f:
        numbers = [int(line.replace("mp-", "")) for line in f]
    numbers.sort()
    return numbers

def make_index_rst_for_each1000(d, numbers):
    """
    This creates the top page, index_rst.
    """

    d_numbers = []
    for num in numbers:
        if num in range(d * 1000, (d + 1) * 1000):
            d_numbers.append(num)

    if d_numbers:
        with open("index.rst", 'w') as w:
            w.write(tmpl_index.format(midstart="%d000" % d, midend="%d999" % d))
            for num in d_numbers:
                w.write("   mp-{num}\n".format(num=num))

def make_each_data_rst(num, mp_dat_directory, data_directory):
    pretty_formula = ""
    with open("{dir}/mp-{num}.dat".format(dir=mp_dat_directory, num=num)) as f:
        for line in f:
            if 'pretty_formula' in line:
                pretty_formula = line.split(':')[1].strip()
                break

    poscar_yaml_filename = "{dir}/POSCAR-unitcell.yaml".format(dir=data_directory)
    cell, _ = read_poscar_yaml(poscar_yaml_filename)
    symmetry = get_symmetry(cell)

    # dos_filename = "mp-%d-dos.png" % num
    # tprops_filename = "mp-%d-tprops.png" % num
    # gruneisen_filename = "mp-%d-gruneisen.png" % num
    # qha_filename = "mp-%d-qha.png" % num

    band_filename = "{dir}/band.png".format(dir=data_directory)
    dos_filename = "{dir}/dos.png".format(dir=data_directory)
    tprops_filename = "{dir}/tprops.png".format(dir=data_directory)
    gruneisen_filename = "{dir}/gruneisen.png".format(dir=data_directory)
    qha_filename = "{dir}/qha.png".format(dir=data_directory)

    with open("mp-%d.rst" % num, 'w') as w:
        today = date.today()
        contents = ""
        if os.path.exists(band_filename):
            contents += "b"
        else:
            contents += "."
        if os.path.exists(dos_filename):
            contents += "d"
        else:
            contents += "."
        if os.path.exists(tprops_filename):
            contents += "t"
        else:
            contents += "."
        # if os.path.exists(gruneisen_filename):
        #     contents += "g"
        # else:
        #     contents += "."
        # if os.path.exists(qha_filename):
        #     contents += "q"
        # else:
        #     contents += "."

        w.write(tmpl_mp.format(mid=num,
                               pretty_formula=pretty_formula,
                               contents=contents,
                               spg="%s (%d) / %s" % (symmetry['international'],
                                                     symmetry['number'],
                                                     symmetry['hall']),
                               num_units="%d" % get_Z(cell.get_numbers()),
                               #filename="mp-%d.tar.lzma" % num,
                               date="%d-%d-%d" % (today.year,
                                                  today.month,
                                                  today.day)))
    
        if os.path.exists(band_filename):
            w.write("Phonon band structure\n")
            w.write("----------------------\n\n")
            w.write(".. image:: mp-{mid}-band.png\n\n".format(mid=num))

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
            
        with open(poscar_yaml_filename) as f_poscar:
            w.write("POSCAR.yaml\n")
            w.write("----------------\n\n")
            w.write("POSCAR.yaml shows the crystal structure after the "
                    "relaxation used for this phonon calculation.\n\n")

            w.write("::\n\n")
            for line in f_poscar:
                w.write("   %s" % line)
            w.write("\n\n")

        w.write(citation_mp)

        w.write(data_license)

def main(d):
    mp_filename = "/home/togo/autocalc/calc20160429/data_arrange/phonon-data/mp-list.dat"
    numbers = get_mp_numbers(mp_filename)

    make_index_rst_for_each1000(d, numbers)

    for num in numbers:
        if num in range(d * 1000, (d + 1) * 1000):
            mp_dat_directory = "/home/togo/autocalc/MP-data-20160409/mp-data"
            data_directory = "/home/togo/autocalc/calc20160429/data_arrange/phonon-data/mp-{num}".format(num=num)
            make_each_data_rst(num, mp_dat_directory, data_directory)

if __name__ == "__main__":
    import sys
    d = int(sys.argv[1])
    main(d)
