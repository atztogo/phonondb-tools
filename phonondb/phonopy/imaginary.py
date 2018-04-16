import numpy as np
from cogue.crystal.utility import klength2mesh

class Imaginary:
    def __init__(self,
                 phonon,
                 distance=200):
        self._phonon = phonon # Phonopy object
        self._lattice = np.array(phonon.get_unitcell().get_cell().T,
                                 dtype='double')

        self._mesh = None
        self._ratio = None

        self._set_mesh(distance=distance)
        self._run_mesh_sampling()
        self._search_imaginary_qpoint_ratio()

    def get_imaginary_qpoint_ratio(self):
        return self._ratio

    def get_lattice(self):
        return self._lattice

    def get_mesh(self):
        return self._mesh

    def _set_mesh(self, distance=200):
        self._mesh = klength2mesh(distance, self._lattice)

    def _run_mesh_sampling(self):
        self._phonon.set_mesh(self._mesh)

    def _search_imaginary_qpoint_ratio(self):
        _, weights, freqs, _ = self._phonon.get_mesh()
        self._ratio = (float(np.extract(freqs[:, 0] < 0, weights).sum()) /
                       np.prod(self._mesh))

if __name__ == '__main__':
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.interface.phonopy_yaml import phonopyYaml
    from phonopy.file_IO import parse_FORCE_SETS
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    if len(sys.argv) > 1:
        cell = phonopyYaml(sys.argv[1]).get_atoms()
    else:
        cell = phonopyYaml("POSCAR-unitcell.yaml").get_atoms()
    phonon_info = yaml.load(open("phonon.yaml"))
    phonon = Phonopy(cell,
                     phonon_info['supercell_matrix'],
                     is_auto_displacements=False)
    force_sets = parse_FORCE_SETS()
    phonon.set_displacement_dataset(force_sets)
    phonon.produce_force_constants()

    distance = 200
    imaginary = Imaginary(phonon, distance=distance)

    lattice = imaginary.get_lattice()
    print "lattice_lengths: [ %f, %f, %f ]" % tuple(get_lattice_parameters(lattice))
    print "lattice_angles: [ %f, %f, %f ]" % tuple(get_angles(lattice))
    print "mesh_length: %f" % distance
    print "mesh: [ %d, %d, %d ]" % tuple(imaginary.get_mesh())
    print "ratio: %f" % imaginary.get_imaginary_qpoint_ratio()
