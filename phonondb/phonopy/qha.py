import numpy as np
from phonopy import PhonopyQHA

class QHA:
    def __init__(self,
                 volumes,
                 electronic_energies,
                 temperatures,
                 free_energy,
                 cv,
                 entropy,
                 eos='vinet',
                 t_max=1000.0,
                 Z=1,
                 verbose=True):
        self._qha = PhonopyQHA(volumes,
                               electronic_energies,
                               eos=eos,
                               temperatures=temperatures,
                               free_energy=fe_phonon,
                               cv=cv,
                               entropy=entropy,
                               t_max=t_max,
                               verbose=True)
        self._Z = Z


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

    def plot(self, plt, thin_number=10):
        fig = plt.figure()
        fig.subplots_adjust(left=0.09, right=0.97, bottom=0.09, top=0.95)
        
        plt1 = fig.add_subplot(2, 3, 1)
        plt1.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_volume_temperature(plt=plt)

        plt2 = fig.add_subplot(2, 3, 2)
        plt2.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_thermal_expansion(plt=plt)

        plt3 = fig.add_subplot(2, 3, 3)
        plt3.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_bulk_modulus_temperature(plt=plt,
                                                ylabel="Bulk modulus (GPa)")

        plt4 = fig.add_subplot(2, 3, 4)
        plt4.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_heat_capacity_P_polyfit(plt=plt, Z=self._Z)

        plt5 = fig.add_subplot(2, 3, 5)
        plt5.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_gibbs_temperature(plt=plt,
                                         ylabel='Gibbs free energy (eV)')

        plt6 = fig.add_subplot(2, 3, 6)
        plt6.tick_params(axis='both', which='major', labelsize=10.5)
        self._qha.plot_helmholtz_volume(thin_number=thin_number,
                                        plt=plt,
                                        ylabel='Free energy (eV)')
        
    def save_figure(self, plt):
        plt.savefig("qha.png")

if __name__ == '__main__':
    import sys
    import yaml
    from phonopy.file_IO import (read_thermal_properties_yaml, read_v_e,
                                 read_cp, read_ve)
    from phonopy.interface.phonopy_yaml import phonopyYaml
    from thermal_prop import get_Z
    import matplotlib
    matplotlib.use('Agg')            
    matplotlib.rcParams.update({'figure.figsize': (10, 7),
                                'font.family': 'serif'})
    import matplotlib.pyplot as plt

    # plt.rcParams['backend'] = 'PDF'
    # plt.rcParams['pdf.fonttype'] = 42
    # plt.rcParams['font.family'] = 'serif'
    # plt.rcParams['axes.labelsize'] = 18
    # plt.rcParams['figure.subplot.left'] = 0.15
    # plt.rcParams['figure.subplot.bottom'] = 0.15
    # plt.rcParams['figure.figsize'] = 8, 6

    cell = phonopyYaml("gruneisen-01/POSCAR-unitcell.yaml").get_atoms()
    volumes, electronic_energies = read_v_e("e-v.dat")
    (temperatures,
     cv,
     entropy,
     fe_phonon,
     imag_ratios) = read_thermal_properties_yaml(sys.argv[1:])

    indices_used = np.nonzero(np.array(imag_ratios) < 0.001)[0]

    qha = QHA(volumes[indices_used],
              electronic_energies[indices_used],
              temperatures,
              fe_phonon[:, indices_used],
              cv[:, indices_used],
              entropy[:, indices_used],
              eos='vinet', # or 'birch_murnaghan'
              t_max=1000,
              Z=get_Z(cell.get_atomic_numbers()),
              verbose=True)

    qha.plot(plt, thin_number=20)
    plt.subplots_adjust(wspace=0.42, hspace=0.31)

    plt.savefig("qha.png")
