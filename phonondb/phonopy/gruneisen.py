import numpy as np
from cogue.crystal.utility import klength2mesh

class ModeGruneisen:
    def __init__(self,
                 phonon_orig,
                 phonon_plus,
                 phonon_minus,
                 distance=100):
        self._phonopy_gruneisen = phonopy_gruneisen
        self._phonon = phonon
        self._lattice = np.array(phonon.get_unitcell().get_cell().T,
                                 dtype='double')

        self._mesh = None
        self._gruneisen = None

    def run(self):
        self._set_mesh(distance=distance)
        if self._run_mesh_sampling():
            self._run_gruneisen()
            return True
        return False

    def get_lattice(self):
        return self._lattice

    def get_mesh(self):
        return self._mesh

    def get_mesh_gruneisen(self):
        return self._gruneisen

    def plot(self, plt, max_index=101):
        temps, fe, entropy, cv = self._thermal_properties
        fig = plt.figure()
        fig.subplots_adjust(left=0.20, right=0.92, bottom=0.18)
        plt.tick_params(axis='both', which='major', labelsize=10.5)
        ax = fig.add_subplot(111)
        plt.plot(temps[:max_index], fe[:max_index], 'r-')
        plt.plot(temps[:max_index], entropy[:max_index], 'b-')
        plt.plot(temps[:max_index], cv[:max_index], 'g-')
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
        # ax.set_aspect(aspect * 0.7)
        plt.legend(('Free energy [kJ/mol]', 'Entropy [J/K/mol]',
                    r'C$_\mathrm{V}$ [J/K/mol]'),
                   loc='best',
                   prop={'size':8.5},
                   frameon=False)
        plt.xlabel("Temperatures (K)")
        plt.ylabel("Thermal properties (*/unitcell)")
        
    def save_figure(self, plt):
        plt.savefig("gruneisen.png")

    def _set_mesh(self, distance=100):
        self._mesh = klength2mesh(distance, self._lattice)
    
    def _run_mesh_sampling(self):
        return self._phonopy_gruneisen.set_mesh(self._mesh)
    
    def _run_gruneisen(self):
        self._thermal_properties = self._phonon.get_thermal_properties()
    

if __name__ == '__main__':
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.gruneisen.mesh import Mesh as GruneisenMesh
    from phonopy.interface.phonopy_yaml import phonopyYaml
    from phonopy.file_IO import parse_FORCE_SETS
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (4.5, 3)})
    import matplotlib.pyplot as plt

    phonons = []
    for dirname in ('orig', 'plus', 'minus'):
        if len(sys.argv) > 1:
            cell = phonopyYaml("%s/" % dirname + sys.argv[1]).get_atoms()
        else:
            cell = phonopyYaml("%s/POSCAR-unitcell.yaml" % dirname).get_atoms()
        phonon_info = yaml.load(open("%s/%s.yaml" % (dirname, dirname)))
        phonon = Phonopy(cell,
                         phonon_info['supercell_matrix'],
                         is_auto_displacements=False)
        force_sets = parse_FORCE_SETS()
        phonon.set_displacement_dataset(force_sets)
        phonon.produce_force_constants()
        phonons.append(phonon)

    distance = 100
    gruneisen = ModeGruneisen(phonons[0], phonons[1], phonons[2], distance=distance)
    if gruneisen.run():
        gruneisen.plot(plt)
        lattice = gruneisen.get_lattice()
        print "a, b, c =", get_lattice_parameters(lattice)
        print "alpha, beta, gamma =", get_angles(lattice)
        print "mesh (x=%f) =" % distance, gruneisen.get_mesh()
        gruneisen.save_figure(plt)
    else:
        print "Mode Gruneisen parameter calculation failed."
