import numpy as np
import seekpath

class Band:
    def __init__(self,
                 phonon,
                 num_qpoints=101):
        self._phonon = phonon # Phonopy object
        self._num_qpoints = num_qpoints
        self._band = []
        self._labels = None
        self._connected = None

    def run(self):
        unitcell = self._phonon.unitcell
        cell = (unitcell.get_cell(),
                unitcell.get_scaled_positions(),
                unitcell.get_atomic_numbers())
        band_path = seekpath.get_path(cell)

        self._set_band(band_path)
        self._set_labels(band_path)
        return self._run_band()

    def get_band(self):
        return self._phonon.get_band_structure()

    def plot_band(self, plt, delta_d=0.02):
        fig, ax = plt.subplots()

        _, distances, frequencies, _ = self._phonon.get_band_structure()
        d_shift = 0
        d_point = []
        special_points = []
        unconnected_points = [0]
        for d, f, c in zip(distances, frequencies, self._connected):
            special_points.append(d[0] + d_shift)
            if not c:
                d_shift += delta_d
                special_points.append(d[0] + d_shift)
                unconnected_points.append(special_points[-2])
                unconnected_points.append(special_points[-1])
            plt.plot(d + d_shift, f, 'r-', linewidth=1)

        special_points.append(distances[-1][-1] + d_shift)
        unconnected_points.append(special_points[-1])

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.ylabel('Frequency (THz)')
        plt.xlabel('Wave vector')
        plt.xlim(0, special_points[-1])
        plt.xticks(special_points, self._labels)

        ax.xaxis.set_ticks_position('both')
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_tick_params(which='both', direction='in')
        ax.yaxis.set_tick_params(which='both', direction='in')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        for d in unconnected_points:
            plt.axvline(x=d, linestyle='-', linewidth=1.5, color='k')
        
        x_pairs = np.reshape(unconnected_points, (-1, 2))
        x_pairs /= unconnected_points[-1]
        ymin, ymax = ax.get_ylim()
        for pair in x_pairs:
            plt.axhline(y=0, xmin=pair[0], xmax=pair[1],
                        linestyle=':', linewidth=0.5, color='b')
            plt.axhline(y=ymin, xmin=pair[0], xmax=pair[1],
                        linestyle='-', linewidth=1.5, color='k')
            plt.axhline(y=ymax, xmin=pair[0], xmax=pair[1],
                        linestyle='-', linewidth=1.5,  color='k')

        fig.tight_layout()

    def write_band_yaml(self):
        self._phonon.write_yaml_band_structure()
        
    def save_band(self, plt):
        plt.savefig("band.png")

    def _set_band(self, band_path):
        point_coords = band_path['point_coords']
        for path in band_path['path']:
            self._append_band(point_coords[path[0]], point_coords[path[1]])
        
    def _set_labels(self, band_path):
        labels = []
        prev_path = None
        connected = []
        point_coords = band_path['point_coords']

        for path in band_path['path']:
            if prev_path and prev_path[1] != path[0]:
                labels.append(prev_path[1])
                connected.append(False)
            else:
                connected.append(True)
            labels.append(path[0])
            prev_path = path
        labels.append(prev_path[1])

        for i, l in enumerate(labels):
            if 'GAMMA' in l:
                labels[i] = "$" + l.replace("GAMMA", "\Gamma") + "$"
            elif 'SIGMA' in l:
                labels[i] = "$" + l.replace("SIGMA", "\Sigma") + "$"
            elif 'DELTA' in l:
                labels[i] = "$" + l.replace("DELTA", "\Delta") + "$"
            else:
                labels[i] = "$\mathrm{%s}$" % l

        self._labels = labels
        self._connected = connected

    def _append_band(self, q_start, q_end):
        band = []
        nq = self._num_qpoints
        for i in range(nq):
            band.append(np.array(q_start) +
                        (np.array(q_end) - np.array(q_start)) / (nq - 1)  * i)
        self._band.append(band)

    def _run_band(self):
        return self._phonon.set_band_structure(self._band)

if __name__ == '__main__':
    import os
    import sys
    import yaml
    from phonopy import Phonopy
    from phonopy.interface.phonopy_yaml import get_unitcell_from_phonopy_yaml
    from phonopy.file_IO import parse_FORCE_SETS, parse_BORN
    from cogue.crystal.utility import (get_angles, get_lattice_parameters,
                                       frac2val)
    import matplotlib

    if len(sys.argv) > 1:
        cell = get_unitcell_from_phonopy_yaml(sys.argv[1])
    else:
        cell = get_unitcell_from_phonopy_yaml("POSCAR-unitcell.yaml")
    phonon_info = yaml.load(open("phonon.yaml"))
    cell = get_unitcell_from_phonopy_yaml("POSCAR-unitcell.yaml")

    phonon = None
    if os.path.isfile("phonopy.conf"):
        with open("phonopy.conf") as f:
            for line in f:
                if 'PRIMITIVE_AXIS' in line:
                    prim_vals = [frac2val(x) for x in line.split()[2:]]

                    if len(prim_vals) == 9:
                        primitive_matrix = np.reshape(prim_vals, (3, 3))
                        phonon = Phonopy(cell,
                                         phonon_info['supercell_matrix'],
                                         primitive_matrix=primitive_matrix)
                    else:
                        print("PRIMITIVE_AXIS is something wrong.")
                        sys.exit(1)
    
                    break

    if phonon is None:
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

    band = Band(phonon, num_qpoints=101)
    if band.run():
        band.write_band_yaml()

        _, distances, frequencies, _ = band.get_band()
        d_end = distances[-1][-1]
        f_max = np.max(frequencies)
        primitive = phonon.get_primitive()
        num_atom = primitive.get_number_of_atoms()
        length = num_atom ** (1.0 / 3) * 4.5

        figsize_x = d_end * length
        margin = 0.7
        scale = 0.15
        delta_d = d_end / (figsize_x - margin) * scale

        matplotlib.use('Agg')
        matplotlib.rcParams.update({'figure.figsize': (figsize_x, 3.1),
                                    'font.family': 'serif'})
        import matplotlib.pyplot as plt

        band.plot_band(plt, delta_d=(delta_d))
        band.save_band(plt)

