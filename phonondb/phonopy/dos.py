import numpy as np
from cogue.crystal.utility import klength2mesh

class DOS:
    def __init__(self,
                 phonon,
                 distance=100):
        self._phonon = phonon # Phonopy object
        self._lattice = np.array(phonon.get_unitcell().get_cell().T,
                                 dtype='double')
        self._distance = distance

        self._mesh = None
        self._freqs = None
        self._dos = None

    def run(self):
        self._set_mesh()
        if self._run_mesh_sampling():
            self._run_dos()
            return True
        return False

    def get_lattice(self):
        return self._lattice

    def get_mesh(self):
        return self._mesh

    def get_dos(self):
        return self._freqs, self._dos

    def write_dos(self):
        self._phonon.write_total_DOS()

    def plot_dos(self, plt):
        fig = plt.figure()
        # fig.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
        plt.tick_params(axis='both', which='major', labelsize=10.5)
        ax = fig.add_subplot(111)
        plt.plot(self._freqs, self._dos, 'r-')

        f_min, f_max = self._get_f_range()
        plt.xlim(xmin=f_min, xmax=f_max)
        plt.ylim(ymin=0)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_tick_params(which='both', direction='in')
        ax.yaxis.set_tick_params(which='both', direction='in')

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        # aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
        # ax.set_aspect(aspect * 0.55)
        plt.xlabel("Frequency (THz)")
        plt.ylabel("Phonon DOS\n(States/THz$\cdot$unitcell)")
        fig.tight_layout()
        
    def save_dos(self, plt):
        plt.savefig("dos.png")

    def _get_f_range(self):
        i_min = 0
        i_max = 1000

        for i, (f, d) in enumerate(zip(self._freqs, self._dos)):
            if d > 1e-5:
                i_min = i
                break

        for i, (f, d) in enumerate(zip(self._freqs[::-1], self._dos[::-1])):
            if d > 1e-5:
                i_max = len(self._freqs) - 1 - i
                break

        f_min = self._freqs[i_min]
        if f_min > 0:
            f_min = 0

        f_max = self._freqs[i_max]
        f_max += (f_max - f_min) * 0.05
            
        return f_min, f_max

    def _set_mesh(self):
        self._mesh = klength2mesh(self._distance, self._lattice)
    
    def _run_mesh_sampling(self):
        return self._phonon.set_mesh(self._mesh)
    
    def _run_dos(self, tetrahedron_method=True):
        if self._phonon.set_total_DOS(tetrahedron_method=tetrahedron_method):
            self._freqs, self._dos = self._phonon.get_total_DOS()

if __name__ == '__main__':
    import os
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.interface.phonopy_yaml import get_unitcell_from_phonopy_yaml
    from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    if len(sys.argv) > 1:
        cell = get_unitcell_from_phonopy_yaml(sys.argv[1])
    else:
        cell = get_unitcell_from_phonopy_yaml("POSCAR-unitcell.yaml")
    phonon_info = yaml.load(open("phonon.yaml"))
    cell = get_unitcell_from_phonopy_yaml("POSCAR-unitcell.yaml")
    phonon = Phonopy(cell, phonon_info['supercell_matrix'])
    force_sets = parse_FORCE_SETS()
    phonon.set_displacement_dataset(force_sets)
    phonon.produce_force_constants()
    if os.path.isfile("BORN"):
        with open("BORN") as f:
            primitive = phonon.get_primitive()
            nac_params = parse_BORN(primitive, filename="BORN")
            nac_params['factor'] = 14.399652
            phonon.set_nac_params(nac_params)

    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (5, 2.8),
                                'font.family': 'serif'})
    import matplotlib.pyplot as plt

    distance = 100
    dos = DOS(phonon, distance=distance)
    if dos.run():
        dos.write_dos()

        dos.plot_dos(plt)
        lattice = dos.get_lattice()
        print("a, b, c = %f %f %f" % tuple(get_lattice_parameters(lattice)))
        print("alpha, beta, gamma = %f %f %f" % tuple(get_angles(lattice)))
        print("mesh (x=%f) = %s" % (distance, dos.get_mesh()))
        dos.save_dos(plt)
    else:
        print("DOS calculation failed.")
