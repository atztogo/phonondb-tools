import numpy as np
from cogue.crystal.utility import klength2mesh

class ModeGruneisen:
    def __init__(self,
                 phonopy_gruneisen,
                 distance=100):
        self._phonopy_gruneisen = phonopy_gruneisen
        self._phonon = self._phonopy_gruneisen.get_phonon()
        self._lattice = np.array(self._phonon.get_unitcell().get_cell().T,
                                 dtype='double')
        self._mesh = None
        self._gruneisen = None

    def run(self):
        self._set_mesh(distance=distance)
        if self._run_mesh_sampling():
            self._run_gruneisen()
            return True
        else:
            return False

    def get_lattice(self):
        return self._lattice

    def get_mesh(self):
        return self._mesh

    def get_mesh_gruneisen(self):
        return self._gruneisen_mesh

    def plot(self, 
             plt,
             cutoff_frequency=0.1):
        fig = plt.figure()
        fig.subplots_adjust(left=0.20, right=0.93, bottom=0.13, top=0.95)
        plt.tick_params(axis='both', which='major', labelsize=10.5)
        ax = fig.add_subplot(111)
        for f, g in zip(self._frequencies.T, self._gammas.T):
            condition = np.abs(f) > cutoff_frequency
            plt.plot(np.extract(condition, f), np.extract(condition, g), 
                     'o', color=(0, 0, 0), markersize=1.0)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
        ax.set_aspect(aspect * 1.0)
        plt.xlabel("Frequency (THz)")
        plt.ylabel("Mode Gruneisen parameter")
        
    def save_figure(self, plt):
        plt.savefig("gruneisen.png")

    def _set_mesh(self, distance=100):
        self._mesh = klength2mesh(distance, self._lattice)
    
    def _run_mesh_sampling(self):
        return self._phonopy_gruneisen.set_mesh(self._mesh)
    
    def _run_gruneisen(self):
        self._gruneisen_mesh = self._phonopy_gruneisen.get_mesh()
        self._gammas = self._gruneisen_mesh.get_gruneisen()
        self._frequencies = self._gruneisen_mesh.get_frequencies()

if __name__ == '__main__':
    import sys
    import yaml
    from phonopy import Phonopy, PhonopyGruneisen
    from phonopy.gruneisen.mesh import Mesh as GruneisenMesh
    from phonopy.interface.phonopy_yaml import phonopyYaml
    from phonopy.file_IO import parse_FORCE_SETS
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (4, 4),
                                'font.family': 'serif'})
    import matplotlib.pyplot as plt

    phonons = []
    for dirname in ('gruneisen-01', 'gruneisen-02', 'gruneisen-00'):
        if len(sys.argv) > 1:
            cell = phonopyYaml("%s/" % dirname + sys.argv[1]).get_atoms()
        else:
            cell = phonopyYaml("%s/POSCAR-unitcell.yaml" % dirname).get_atoms()
        phonon_info = yaml.load(open("%s/phonon.yaml" % dirname))
        phonon = Phonopy(cell,
                         phonon_info['supercell_matrix'],
                         is_auto_displacements=False)
        force_sets = parse_FORCE_SETS(filename="%s/FORCE_SETS" % dirname)
        phonon.set_displacement_dataset(force_sets)
        phonon.produce_force_constants()
        phonons.append(phonon)

    phonopy_gruneisen = PhonopyGruneisen(phonons[0], phonons[1], phonons[2])
    distance = 200
    gruneisen = ModeGruneisen(phonopy_gruneisen,
                              distance=distance)
    if gruneisen.run():
        gruneisen.plot(plt)
        lattice = gruneisen.get_lattice()
        print "a, b, c =", get_lattice_parameters(lattice)
        print "alpha, beta, gamma =", get_angles(lattice)
        print "mesh (x=%f) =" % distance, gruneisen.get_mesh()
        gruneisen.save_figure(plt)
        # plt.show()
    else:
        print "Mode Gruneisen parameter calculation failed."
