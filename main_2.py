import numpy as np
from pdb import set_trace
import time
from preprocess import read_benchmark
from hyptest import fdr
import matplotlib.pyplot as plt
import plot_graph
import community as community_louvain
import csv
from utils import save_file
import os.path
import networkx as nx
import sys
import json
import math
from wrg import WRG
from hyptest import fdr
from utils import insignificant_edges
import community as community_louvain
# import gecmi







if __name__ == "__main__":
    mut = 0.1
    benchmark_name = 'N512_k6_no_com'
    # benchmark_name = 'gn'

    # Read the graph and community detection
    # recalculate weights
    # multi-hypothesis testing
    # remove insignificant edges
    # community detection

        
    # config = json.loads(open(sys.argv[1]).read())

    # graph_name = config['graph_name']
    # graph_filename = '/content/drive/My Drive/datasets/{}/{}.graphml'.format(graph_name, graph_name)
 
    # G = nx.read_graphml(graph_filename)
    
    # for (u, v) in G.edges():
    #   # print (u, v, G[u][v]['weight'])
    #   weight = G[u][v]['weight']
    #   G[u][v]['weight'] = min(int(math.log10(weight))+1, 2)

    adj_mat = read_benchmark.get_network_adjmat('../benchmarks/{}/mut_{}.nse'.format(benchmark_name, mut))
    # adj_mat = read_benchmark.get_network_adjmat('../benchmarks/{}.nse'.format(benchmark_name))

    G = nx.from_numpy_matrix(adj_mat)

    print (len(G.nodes()))
    print (len(G.edges()))
# ##  Draw graph
#     gold_partition = read_benchmark.get_community_partition('../benchmarks/{}.cnl'.format(benchmark_name))
#     print ('Gold partition: ', gold_partition)
#     pos = nx.spring_layout(G)
#     plot_graph.plot_com(G, pos, gold_partition, '../benchmarks/{}_partition.png'.format(benchmark_name))
#     set_trace()
# ##
    weights = [G[u][v]['weight'] for (u,v) in G.edges()]
    print ('max weight is {}'.format(max(weights)))
    wrg = WRG(G)
    # print (wrg.weighted_edges_list[0:10])
    print (wrg.p)


    p_values = np.array([])
    edge_list = []

    for (u,v) in G.edges():
      start_time = time.time()
      print ('In main >>> started ({},{}) edge.'.format(u,v))
      total_W_motif = 0
      common_neighbors = nx.common_neighbors(G, u, v)
      print ('len of common neighbors: {}'.format(len(list(common_neighbors))))
      for c in nx.common_neighbors(G, u, v):
        W_motif = G[u][c]['weight'] * G[v][c]['weight']
        # print ('W_motif: ', W_motif)
        total_W_motif += W_motif

      
      print ('total_W_motif: ', total_W_motif)
      pval = wrg.get_p_value(total_W_motif)
      # print ('pval: ', pval)
      print ('In main >>> p_value({},{}) = {} in {} seconds.\n'.format(u,v, pval, time.time() - start_time))
      
      p_values = np.append(p_values, pval)
      edge_list.append((u, v))

    print (p_values)
    print (len(p_values))

    # multi-hypothesis testing
    sig = fdr.get_significant_pvals(p_values, 0.1)
    
    edges_to_remove = insignificant_edges.get_insignificant_edges(sig, edge_list)

    print ('# of comminities (Gold):', read_benchmark.get_num_of_communities('../benchmarks/{}/mut_{}.cnl'.format(benchmark_name, mut)))
    # print ('# of comminities (Gold):', read_benchmark.get_num_of_communities('../benchmarks/{}.cnl'.format(benchmark_name)))


    print ('length of G.edges() before edge removal: ', len(list(G.edges())))
    init_partition = community_louvain.best_partition(G)
    read_benchmark.save_community(init_partition, '../benchmarks/{}/mut_{}_1.cnl'.format(benchmark_name, mut))
    # read_benchmark.save_community(init_partition, '../benchmarks/{}_1.cnl'.format(benchmark_name))


    init_comm_arr = []
    init_communities = []
    for node in init_partition:
      init_comm_arr.append((node, init_partition[node]))
      if init_partition[node] not in init_communities:
        init_communities.append(init_partition[node])
    print ('init # of communities: ', len(init_communities))

    print (edges_to_remove)
    print ('length of edges_to_remove: ', len(edges_to_remove))
    # print ('length of G.edges(): ', len(list(G.edges())))

    for e in edges_to_remove:
      G.remove_edge(*e)

    print ('length of G.edges(): ', len(list(G.edges())))
    partition = community_louvain.best_partition(G)
    # print (type(partition))
    # print (partition)
    # print (len(partition))

    read_benchmark.save_community(partition, '../benchmarks/{}/mut_{}_2.cnl'.format(benchmark_name, mut))
    # read_benchmark.save_community(partition, '../benchmarks/{}_2.cnl'.format(benchmark_name))

    comm_arr = []
    communities = []
    for node in partition:
      comm_arr.append((node, partition[node]))
      if partition[node] not in communities:
        communities.append(partition[node])
    print (comm_arr)
    print (len(comm_arr))
    print ('new # of communities: ', len(communities))

    # init_comm_arr = read_benchmark.get_community_array()
    # print (init_comm_arr)
    # print (len(init_comm_arr))

    # print( gecmi.calc_nmi_and_error(init_comm_arr, comm_arr, 0.1, 0.1 ) )
