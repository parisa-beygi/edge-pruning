import numpy as np
import csv

def save_biadjacency(adj_matrix, filename, delim='\t', binary=False):
    """Save the biadjacendy matrix of the BiCM null model.

    The matrix can either be saved as a binary NumPy ``.npy`` file or as a
    human-readable ``.csv`` file.

    .. note::

        * The relative path has to be provided in the filename, e.g.
          *../data/pvalue_matrix.csv*.

        * If ``binary==True``, NumPy
          automatically appends the format ending ``.npy`` to the file.

    :param filename: name of the output file
    :type filename: str
    :param delim: delimiter between values in file
    :type delim: str
    :param binary: if ``True``, save as binary ``.npy``, otherwise as a
        ``.csv`` file
    :type binary: bool
    """
    save_array(adj_matrix, filename, delim, binary)


def save_array(mat, filename, delim='\t', binary=False, formatt = '%.18e'):
    """Save the array ``mat`` in the file ``filename``.

    The array can either be saved as a binary NumPy ``.npy`` file or as a
    human-readable ``.npy`` file.

    .. note::

        * The relative path has to be provided in the filename, e.g.
          *../data/pvalue_matrix.csv*.

        * If ``binary==True``, NumPy
          automatically appends the format ending ``.npy`` to the file.

    :param mat: array
    :type mat: numpy.array
    :param filename: name of the output file
    :type filename: str
    :param delim: delimiter between values in file
    :type delim: str
    :param binary: if ``True``, save as binary ``.npy``, otherwise as a
        ``.csv`` file
    :type binary: bool
    """
    if binary:
        np.save(filename, mat)
    else:
        np.savetxt(filename, mat, delimiter=delim, fmt=formatt)
 
  
def load(filename):
  return np.genfromtxt(filename, delimiter='\t')