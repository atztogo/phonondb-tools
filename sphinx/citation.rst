References and citations
========================

.. _crystal_structure_and_citation:

About crystal structure and citation
-------------------------------------

.. _the Materials Project: https://www.materialsproject.org/
.. _the Materials Project citation: https://materialsproject.org/citing
.. _the Materials API: https://www.materialsproject.org/open
.. _spglib: http://spglib.sourceforge.net/
.. _pymatgen: http://pymatgen.org/

Phonon calculations shown in this section were performed using the
crystal structures obtained as follows:

1. Initial crystal structures were obtained from `the Materials Project`_.
2. Each crystal structure was symmetrized and standardized using
   `spglib`_ with the tolerance distance of 0.1 angstrom before
   starting phonon calculation.

For the reason of (1), if you use the data in this section, we ask you `the Materials Project
citation`_ as follows::

   A. Jain*, S.P. Ong*, G. Hautier, W. Chen, W.D. Richards, S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder, K.A. Persson (*=equal contributions)
   The Materials Project: A materials genome approach to accelerating materials innovation
   APL Materials, 2013, 1(1), 011002. doi:10.1063/1.4812323

The cyrstal structures in (1) can be computational results of `the
Materials Project`_ performed using crystal structure information from
other data sources. In each crystal page of `the Materials Project`_,
you may find the original ICSD numbers of the crystal structures and
respective citations.

We employed `pymatgen`_ to communicate with `the Materials Project`_
via `the Materials API`_. The
`pymatgen citation <http://pymatgen.org/#how-to-cite-pymatgen>`_ is shown below::

   Shyue Ping Ong, William Davidson Richards, Anubhav Jain, Geoffroy Hautier, Michael Kocher, Shreyas Cholia, Dan Gunter, Vincent Chevrier, Kristin A. Persson, Gerbrand Ceder.
   Python Materials Genomics (pymatgen) : A Robust, Open-Source Python Library for Materials Analysis.
   Computational Materials Science, 2013, 68, 314-319. doi:10.1016/j.commatsci.2012.10.028

The citation for `the Materials API`_ (`the Materials Project citation`_) is as follows::


   S. P. Ong, S. Cholia, A. Jain, M. Brafman, D. Gunter, G. Ceder, and K. A. Persson
   The Materials Application Programming Interface (API): A simple, flexible and efficient API for materials data based on REpresentational State Transfer (REST) principles.
   Computational Materials Science, 2015, 97, 209–215. doi:10.1016/j.commatsci.2014.10.037

We greatly appreciate `the Materials Project`_ and `pymatgen`_.
