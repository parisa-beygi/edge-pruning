
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from preprocess import read_egos
import csv
import sys
import json
from matplotlib.patches import Rectangle


def plot_weight_hists(G, removed_edge_list, save_filename):
  plt.figure()
  # print (G.edges.data('weight'))
  weights = [weight for (u, v, weight) in G.edges.data('weight')]
  print (len(weights))
  n_bins = 20

  # for e in removed_edge_list:
  #   G.remove_edge(*e)

  G.remove_edges_from(removed_edge_list)

  new_weights = [weight for (u, v, weight) in G.edges.data('weight')]
  # ( (b, a) [a < b] ) 
  print ('**************************')
  # print (new_weights)
  print (len(G.edges()))
  print (len(new_weights))
  num_plots = {False: 1, True: 2}[len(new_weights) > 0]
  x = [weights, new_weights] if num_plots == 2 else weights
  # fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
  print (num_plots, x)
  colors = ['blue', 'red'] 
  plt.hist(x, n_bins, density=True, histtype='bar', color=colors[0:num_plots], label=colors[0:num_plots])
  #create legend
  handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in colors]
  labels= ["before edge removal","after edge removal"]
  plt.legend(handles, labels)

  plt.xlabel('Edge weight')
  plt.ylabel('Probability')
  plt.title('Histogram of edge weights')
  


  # plt.legend(prop={'size': 10})
  # plt.set_title('bars with legend')

  # fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
  # axs[1].hist(weights, bins=n_bins)
  # axs[2].hist(new_weights, bins=n_bins)

  # print (x)
  # fig.tight_layout()
  plt.savefig(save_filename)


if __name__ == "__main__":
  
  config = json.loads(open(sys.argv[1]).read())

  graph_name = config['graph_name']
  graph_filename = '/content/drive/My Drive/datasets/{}/{}.graphml'.format(graph_name, graph_name)
  # print (graph_filename)
  q = config['significance_level']

  removed_edge_list_filename = '../outputs/{}/removed_edges/q_{}/{}.csv'.format(graph_name, q, '{}')
  save_filename = '../outputs/{}/tests/weights/q_{}/weight_hist_{}.png'.format(graph_name, q, '{}')
  
  
  count = 0
  for (n, ego) in read_egos.get_egos(graph_filename):
    count += 1
    if count > 30:
      break
    # n = 'n1'
    with open(removed_edge_list_filename.format(n), 'r') as read_obj:
      # pass the file object to reader() to get the reader object
      csv_reader = csv.reader(read_obj)
      # Get all rows of csv from csv_reader object as list of tuples
      list_of_tuples = list(map(tuple, csv_reader))
      # display all rows of csv
      # print(list_of_tuples)

      plot_weight_hists(ego, list_of_tuples, save_filename.format(n))