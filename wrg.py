import networkx as nx
import numpy as np
from utils import math_computations
from utils import sum_combinations 
import math
import time
from collections import Counter 
from pdb import set_trace
import multiprocessing
import os


class WRG(object):

  def __init__(self, graph):
    """Initialize the parameters of the WRG (Weighted Random Graph)."""
    self.graph = graph
    self.N = len(graph.nodes())  

    self.set_weight_list_and_max_weight()
    print ('self.max_weight : ', self.max_weight)

    self.set_max_degree()
    print ('self.max_degree : ', self.max_degree)

    self.max_total_W_motif = self.max_weight * self.max_weight * self.max_degree
    print ('self.max_total_W_motif : ', self.max_total_W_motif)

    W = self.get_weights_sum()
    self.p = 2*W/(self.N*(self.N-1) + 2*W)

    self.zero_W_motif = 1 - pow(self.p, 2)
    self.nonzero_W_motif_base = pow((1 - self.p), 2)

    self.single_motif_dict = {}
    self.total_motif_dict = {}
    # weights = [graph[u][v]['weight'] for (u,v) in graph.edges()]
    # max_w = max(weights)
    # self.max_total_weight = max_w * max_w * 5
    # print ('self.max_total_weight: ', self.max_total_weight)
    self.cmb = sum_combinations.Combinations(self.max_degree, self.max_weight * self.max_weight)



  @classmethod
  def from_adjmatrix(cls, adj_mat):
    return cls(nx.from_numpy_matrix(adj_mat))

  def set_weight_list_and_max_weight(self):
    # self.weighted_edges_list = []
    # self.max_weight = 0

    # for (u, v, weight) in self.graph.edges.data('weight'):
    #   self.weighted_edges_list.append((u, v, weight))
    #   if weight > self.max_weight:
    #     self.max_weight = weight
    self.weighted_edges_list = list(self.graph.edges.data('weight'))
    print ('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', self.weighted_edges_list)
    self.max_weight = max(self.weighted_edges_list, key = lambda x: x[2])[2]

  def set_max_degree(self):
    self.max_degree = max(list(map(lambda x: self.graph.degree[x], list(self.graph.nodes()))))

  def get_weights_sum(self):
    s = 0
    for (u, v, weight) in self.weighted_edges_list:
      s += weight 
    return s

  def get_edge_prob(self, w):
    return pow(self.p, w)*(1 - self.p)

  def get_nonzero_W_motif(self, k):
    total = 0
    div_pairs = math_computations.get_divisor_pairs(k)

    for (a,b) in div_pairs:
      total += pow(self.p, a+b)
    
    return self.nonzero_W_motif_base * total

  def W_motif_comb(self, combination):
    # set_trace()
    total_mult = 1
    for i in combination:
      if i not in self.single_motif_dict:
        self.single_motif_dict[i] = self.get_nonzero_W_motif(i)
      total_mult = total_mult * self.single_motif_dict[i]
    
    # for j in range(1, self.N - 1):
    #   if j > len(combination):
    #     total_mult = total_mult * self.zero_W_motif
    #   total_mult = total_mult * j
    #   if not total_mult == float("inf"):
    #     print (">>>>>>>>>>>>>>>> ", total_mult, j)
    total_mult = total_mult * pow(self.zero_W_motif, self.N - 2 - len(combination))
    all_permutations = math.factorial(self.N - 2)
    zero_permutations = math.factorial(self.N - 2 - len(combination))
    nonzero_permutations = 1
    counts = Counter(combination)
    for k in counts:
      nonzero_permutations = nonzero_permutations * math.factorial(counts[k])

    d = all_permutations / (zero_permutations * nonzero_permutations)
    # print ("total_mult: ", total_mult)
    # print ("num of digits of d: ", int(math.log10(d))+1)

    # return total_mult
    return d * total_mult

  def get_total_W_motif(self, n):
    if n == 0:
      return pow(self.zero_W_motif, self.N - 2)
 
 
    # print ('before calc combinations')
    s_time = time.time()

    # find all combinations 

    # arr = [0] * n; 
    # list_of_combinations = list()
    # math_computations.findCombinationsUtil(list_of_combinations, arr, 0, self.max_weight * self.max_weight, n, 5)
    # list_of_combinations = math_computations.find_combinations_dp(n)
    list_of_combinations = self.cmb.find_combinations_dp(n)

    # list_combinations = math_computations.findCombinations(n)
    # print ('time to calc combinations: ', time.time() - s_time)
    total_sum = 0
    # print ("list_of_combinations: ", list_of_combinations)
    # set_trace()
    # print (os.cpu_count())
    pool = multiprocessing.Pool(4)
    # print (len(list_of_combinations))
    res_list = pool.map(self.W_motif_comb, list_of_combinations)
    total_sum = sum(res_list)
    # for comb in list_of_combinations:
    #   # print ('comb: ', comb)
    #   # print (len(comb))
    #   # set_trace()

    #   if len(comb) <= self.N - 2:
    #     # set_trace()
    #     a = self.W_motif_comb(comb)
    #     # print ('comb prob: ', a)
    #     total_sum += a
    
    return total_sum


  def get_p_value(self, W_star):
    print ('*******Started calculating pvalue*******')

    if W_star == 0:
      total = (1 - self.get_total_W_motif(0))
      print ('In get_p_value() >>> p_value = ', total)    
      return total

    total = 0
    # W_max = 126
    W_max = self.max_total_W_motif + 1
    for w in range(W_star, W_max):
      # print ('In get_p_value() >>> W = ', w)
      if w not in self.total_motif_dict:
        self.total_motif_dict[w] = self.get_total_W_motif(w)
      total += self.total_motif_dict[w]

    print ('In get_p_value() >>> p_value = ', total)    
    return total

