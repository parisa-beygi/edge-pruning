import networkx as nx
import numpy as np 

def get_egos(filename):
  # filename = '/content/drive/My Drive/datasets/vnet/vnet.graphml'
  G = nx.read_graphml(filename)

  for n in G.nodes():
    yield (n, nx.ego_graph(G, n))

  # return ego, nx.to_numpy_matrix(ego, weight = None)
  

def get_edge_ego_networks(filename):
  G = nx.read_graphml(filename)

  nodes = list(G.nodes())
  for (i, n) in enumerate(nodes):
    for (j, m) in enumerate(nodes[i+1:]):
      if G.has_edge(n,m):
        yield (n, m, nx.ego_graph(G, n), nx.ego_graph(G, m))
  