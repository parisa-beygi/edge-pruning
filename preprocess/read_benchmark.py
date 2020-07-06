import numpy as np
import math

def get_network_adjmat(filename):
  f = open(filename, 'r') 
  lines = f.readlines()
  for l in lines:
    x = l.strip().split()
    if '#' in x:
      n = int(x[2].strip(','))
      adj_mat = np.zeros((n, n), dtype=int)
    else:
      i = int(x[0]) - 1
      j = int(x[1]) - 1
      # print (i,j)
      # print (x[2])
      w = float(x[2])
      adj_mat[i,j] = math.ceil(w)

  return adj_mat

def get_community_partition(filename):
  f = open(filename, 'r') 
  lines = f.readlines()
  partition = {}
  comm = 0
  for l in lines:
    for node in l.strip().split():
      partition[int(node) - 1] = comm
    comm += 1

  return partition


def get_community_array(filename):
  f = open(filename, 'r') 
  lines = f.readlines()
  arr = []
  comm = 0
  for l in lines:
    for node in l.strip().split():
      arr.append((int(node) - 1, comm))
    comm += 1

  return arr

def save_community(partition, filename):
  f = open(filename, 'w')
  comm_dict = {}

  for node in partition:
    c = partition[node]
    if c not in comm_dict:
      comm_dict[c] = []
    comm_dict[c].append("{}".format(node+1))

  for c in comm_dict:
    f.write(' '.join(comm_dict[c]))
    f.write('\n')

def get_num_of_communities(cnl_filename):
  f = open(cnl_filename, 'r') 
  lines = f.readlines()
  return len(lines)

# get_num_of_communities('../benchmarks/N512_k6_no_com/mut_0.1.cnl')
# l = get_community_array()
# print (l)