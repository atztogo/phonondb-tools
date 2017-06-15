import numpy as np
from cogue.crystal.utility import klength2mesh, get_Z

class ThermalProperty:
    def __init__(self,
                 phonon,
                 distance=100):
        self._phonon = phonon # Phonopy object
        self._lattice = np.array(phonon.get_unitcell().get_cell().T,
                                 dtype='double')
        self._mesh = None
        self._thermal_properties = None

    def run(self):
        self._set_mesh(distance=distance)
        if self._run_mesh_sampling():
            self._run_thermal_properties()
            return True
        return False

    def get_lattice(self):
        return self._lattice

    def get_mesh(self):
        return self._mesh

    def get_thermal_properties(self):
        # (temps(K), fe(kJ/mol), entropy(J/K/mol), cv(J/K/mol))
        return self._thermal_properties

    def plot(self, plt, max_index=101):
        temps, fe, entropy, cv = self._thermal_properties
        Z = self._get_Z()
        fig, ax = plt.subplots()
        # fig.subplots_adjust(left=0.20, right=0.92, bottom=0.18)
        plt.tick_params(axis='both', which='major', labelsize=10.5)
        plt.plot(temps[:max_index], fe[:max_index] / Z, 'r-')
        plt.plot(temps[:max_index], entropy[:max_index] / Z, 'b-')
        plt.plot(temps[:max_index], cv[:max_index] / Z, 'g-')
        plt.axhline(y=0, linestyle=':', linewidth=0.5, color='k')

        plt.xlim(xmin=0, xmax=1000)
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        aspect = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
        # ax.set_aspect(aspect * 0.7)
        plt.legend(('Free energy (kJ/mol)]', 'Entropy (J/K/mol)',
                    r'$C_\mathrm{V}$ (J/K/mol)'),
                   loc='best',
                   prop={'size':8.5},
                   frameon=False)
        plt.xlabel("Temperatures (K)")
        plt.ylabel("Thermal properties")

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_tick_params(which='both', direction='in')
        ax.yaxis.set_tick_params(which='both', direction='in')

        fig.tight_layout()

    def save_figure(self, plt):
        plt.savefig("tprops.png")

    def _set_mesh(self, distance=100):
        self._mesh = klength2mesh(distance, self._lattice)
    
    def _run_mesh_sampling(self):
        return self._phonon.set_mesh(self._mesh)
    
    def _run_thermal_properties(self):
        self._phonon.set_thermal_properties(t_max=3000)
        self._thermal_properties = self._phonon.get_thermal_properties()

    def _get_Z(self):
        numbers = self._phonon.get_unitcell().get_atomic_numbers()
        return get_Z(numbers)
            
if __name__ == '__main__':
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.interface.phonopy_yaml import get_unitcell_from_phonopy_yaml
    from phonopy.file_IO import parse_FORCE_SETS
    from cogue.crystal.utility import get_angles, get_lattice_parameters
    import matplotlib

    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (4.5, 3),
                                'font.family': 'serif'})
    import matplotlib.pyplot as plt
    
    if len(sys.argv) > 1:
        cell = get_unitcell_from_phonopy_yaml(sys.argv[1])
    else:
        cell = get_unitcell_from_phonopy_yaml("POSCAR-unitcell.yaml")
    phonon_info = yaml.load(open("phonon.yaml"))
    phonon = Phonopy(cell, phonon_info['supercell_matrix'])
    force_sets = parse_FORCE_SETS()
    phonon.set_displacement_dataset(force_sets)
    phonon.produce_force_constants()
    
    distance = 100
    tprops = ThermalProperty(phonon, distance=distance)
    if tprops.run():
        tprops.plot(plt)
        lattice = tprops.get_lattice()
        print("a, b, c = %f %f %f" % tuple(get_lattice_parameters(lattice)))
        print("alpha, beta, gamma = %f %f %f" % tuple(get_angles(lattice)))
        print("mesh (x=%f) = %s" % (distance, tprops.get_mesh()))
        tprops.save_figure(plt)
    else:
        print("Thermal property calculation failed.")
