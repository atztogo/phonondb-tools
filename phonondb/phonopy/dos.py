import numpy as np
from cogue.crystal.utility import klength2mesh

class DOS:
    def __init__(self,
                 phonon,
                 distance=100):
        self._phonon = phonon # Phonopy object
        self._lattice = np.array(phonon.get_unitcell().get_cell().T,
                                 dtype='double')

        self._mesh = None
        self._freqs = None
        self._dos = None


    def run(self):
        self._set_mesh(distance=distance)
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

    def plot_dos(self, plt):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(self._freqs, self._dos, 'r-')
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
        ax.set_aspect(aspect * 0.5)
        plt.xlabel("Frequency (THz)")
        plt.ylabel("Phonon DOS (States/THz$\cdot$unitcell)")
        
    def save_dos(self, plt):
        plt.savefig("dos.png")

    def _set_mesh(self, distance=100):
        self._mesh = klength2mesh(distance, self._lattice)
    
    def _run_mesh_sampling(self):
        return self._phonon.set_mesh(self._mesh)
    
    def _run_dos(self, tetrahedron_method=True):
        if self._phonon.set_total_DOS(tetrahedron_method=tetrahedron_method):
            self._freqs, self._dos = self._phonon.get_total_DOS()
    

if __name__ == '__main__':
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.interface.phonopy_yaml import phonopyYaml
    from phonopy.file_IO import parse_FORCE_SETS
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (5, 3)})
    import matplotlib.pyplot as plt
    
    phonon_info = yaml.load(open("phonon.yaml"))
    cell = phonopyYaml("POSCAR-unitcell.yaml").get_atoms()
    phonon = Phonopy(cell,
                     phonon_info['supercell_matrix'],
                     is_auto_displacements=False)
    force_sets = parse_FORCE_SETS()
    phonon.set_displacement_dataset(force_sets)
    phonon.produce_force_constants()
    
    distance = 100
    dos = DOS(phonon, distance=distance)
    if dos.run():
        dos.plot_dos(plt)
        lattice = dos.get_lattice()
        print "a, b, c =", get_lattice_parameters(lattice)
        print "alpha, beta, gamma =", get_angles(lattice)
        print "mesh (x=%f) =" % distance, dos.get_mesh()
        dos.save_dos(plt)
    else:
        print "DOS calculation failed."
