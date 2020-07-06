import numpy as np
#from bicm import BiCM
from gcm import GCM
from pdb import set_trace
import time
#from preprocess import make_bi
from preprocess import read_egos
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


if __name__ == "__main__":
    # set_trace()
    start_time = time.time()

    config = json.loads(open(sys.argv[1]).read())

    # counter = 0
    q = config['significance_level']
    qq = config['q']
    graph_name = config['graph_name']
    graph_filename = '/content/drive/My Drive/datasets/{}/{}.graphml'.format(graph_name, graph_name)
    null_probs_filename = '/content/drive/My Drive/edge_significance_testing/outputs/{}/null_model_probabilities/cm/{}.csv'.format(graph_name, '{}')
   
    stats_filename = '../outputs/{}/statistics/q_{}.csv'.format(graph_name, q)
    if os.path.exists(stats_filename):
      os.remove(stats_filename)

    file_stats = open(stats_filename, 'a')
    csv_stats=csv.writer(file_stats)
    csv_stats.writerow(["#Nodes", "#Edges", "#Significant Edges", "#Removed Edges", "#Communities", "#New Communities", "#Significant Edges/#Edges"])

    for (n, ego) in read_egos.get_egos(graph_filename):
      # counter += 1
      # if counter > 30:
      #   break
      mat = nx.to_numpy_matrix(ego, weight = None)  
      nodes = np.array(ego.nodes())
    
      prev_num_edges = len(ego.edges())

      gcm = GCM(nodes, mat)

      if not os.path.exists(null_probs_filename.format(n + '_matrix')): 
        time_bef_make_bicm = time.time()
        # print ("make_cm started!")
        # cm.make_bicm()
        gcm.make_cm()
        print ("%%%%%% make_cm took {} seconds.".format(time.time() - time_bef_make_bicm))

        print ("input network and the shape:")
        print (mat)
        print (mat.shape)

        print ("link probabilitie accroding to CM:")
        print (gcm.adj_matrix)

        save_file.save_array(gcm.adj_matrix, null_probs_filename.format(n + '_matrix'))
        save_file.save_array(nodes, null_probs_filename.format(n + '_nodes'), formatt = '%s')

      
      else:
        gcm.adj_matrix = save_file.load(null_probs_filename.format(n + '_matrix'))


      pvalues_filename = '../outputs/{}/pvalues/common_neighbors/{}.csv'.format(graph_name, '{}')

      if not os.path.exists(pvalues_filename.format(n)):
        time_bef_calc_pvals = time.time()
        # cm.lambda_motifs( False, filename = "../outputs/pvalues_movies.csv", delim = '\t', binary = False)
        gcm.lambda_motifs(filename = pvalues_filename.format(n), delim = '\t', binary = False)
        print ("%%%%%% lambda_motifs took {} seconds.".format(time.time() - time_bef_calc_pvals))
        #
        # # cm.lambda_motifs( False, filename = "outputs/pvalues_col.csv", delim = '\t', binary = False)
        #
      sig = fdr.get_significant_pvals(pvalues_filename.format(n), qq)
      # print (sig)
    

      #first compute the best partition
      partition = community_louvain.best_partition(ego)
      # print (len(partition))
      prev_num_comm = len(set(partition.values()))

      ego_pos = nx.spring_layout(ego)
      # plot_graph.plott_communities(ego, partition, '../outputs/{}/plots/q_{}/{}_0.png'.format(graph_name, q, n))
      plot_graph.plot_com(ego, ego_pos, partition, '../outputs/{}/plots/q_{}/{}_0.png'.format(graph_name, q, n))


      print ('Started removing insignificant edges ...')
    
      # n = len(mat)
      edges_to_remove = []
    
      csv_edges_out=csv.writer(open('../outputs/{}/removed_edges/q_{}/{}.csv'.format(graph_name, q, n), 'w'))
      # set_trace()
      for k in range(len(sig)):
        if not sig[k]:
          [i, j] = gcm.flat2triumat_idx(k, len(nodes))
          if mat[i,j] == 1:
            mat[i,j] = 0 
            mat[j,i] = 0
            e = (nodes[i], nodes[j])
            edges_to_remove.append(e)
            csv_edges_out.writerow(e)
            ego.remove_edge(nodes[i], nodes[j])
    
      # print ('Adjacency matrix after removing edges:')
      # print (mat)

      rem_num_edges = len(edges_to_remove)

      #first compute the best partition
      partition = community_louvain.best_partition(ego)
      # print (len(partition))
      curr_num_comm = len(set(partition.values()))

      # plot_graph.plott_communities(ego, partition, '../outputs/{}/plots/q_{}/{}_1.png'.format(graph_name, q, n))
      plot_graph.plot_com(ego, ego_pos, partition, '../outputs/{}/plots/q_{}/{}_1.png'.format(graph_name, q, n))

      file_stats = open(stats_filename, 'a')
      csv_stats=csv.writer(file_stats)
      csv_stats.writerow((len(nodes), prev_num_edges, len(ego.edges()), rem_num_edges, prev_num_comm, curr_num_comm, len(ego.edges())//prev_num_edges))
      # print ('______________Statistics______________')
      # print ('num of nodes: {}'.format(len(nodes)))
      # print ('num of edges: {}'.format(prev_num_edges))    
      # print ('num of communities: {}'.format(prev_num_comm))

      # print ('removed num of edges: {}'.format(rem_num_edges))    
      # print ('num of significant edges: {}'.format(len(ego.edges())))    
      # print ('num of communities after revoming insifnificant edges: {}'.format(curr_num_comm))

    