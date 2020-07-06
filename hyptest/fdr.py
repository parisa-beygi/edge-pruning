from multipy.fdr import lsu
# from multipy.data import neuhaus
import numpy as np
from numpy import genfromtxt
from pdb import set_trace
import time


def get_significant_pvals(pvals, q):
  try:
    significant_pvals = lsu(pvals, q)
  except TypeError:
    print ('TYPEERROR occured in sig')
    significant_pvals = np.array([pvals < q])

  finally:
    # print (list(zip(['{:.4f}'.format(p) for p in pvals], significant_pvals)))
    return significant_pvals

def get_significant_pvals_fromfile(path, q):

  print ('Started multiple hypotheses testing --->')

  pvals = genfromtxt(path, delimiter=',')

  return get_significant_pvals(pvals, q)