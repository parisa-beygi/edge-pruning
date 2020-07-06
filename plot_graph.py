import community as community_louvain
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def plot_com(G, pos, partition, filename):
  plt.figure(figsize=(20,20))

  labels = {}
  for (node_id, name) in list(G.nodes.data('name')):
    labels[node_id] = name

  # pos = nx.spring_layout(G)
  # color the nodes according to their partition
  cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
  nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=500,
                        cmap=cmap, node_color=list(partition.values()))
  nx.draw_networkx_labels(G,pos,labels,font_size=30)
  nx.draw_networkx_edges(G, pos, alpha=0.5)
  plt.savefig(filename)      



def plott_communities(G, partition, filename):

  # #drawing
  # size = float(len(set(partition.values())))
  # pos = nx.spring_layout(G, scale = 2)
  # count = 0.
  # for com in set(partition.values()) :
  #     count = count + 1.
  #     list_nodes = [nodes for nodes in partition.keys()
  #                                 if partition[nodes] == com]
  #     # print (list_nodes)
  #     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
  #                                 node_color = 'r')
  #     nx.draw_networkx_labels(G,pos,labels,font_size=5,font_color=com)

  # nx.draw_networkx_edges(G, pos, alpha=0.5)
  # plt.savefig(filename)

  nodes_list = list(G.nodes())
  labels = {}
  for (node_id, name) in list(G.nodes.data('name')):
    labels[node_id] = name


  plt.figure()

  values = [partition.get(node) for node in G.nodes()]
  # nx.draw_networkx_labels(G, pos=nx.spring_layout(G))
  # print (values)
  nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, with_labels=True, labels = labels, node_size=50)
  plt.savefig(filename)



if __name__ == "__main__":
  filename = '/content/drive/My Drive/datasets/got/got.graphml'
  G = nx.read_graphml(filename)

  partition = community_louvain.best_partition(G)
  pos = nx.spring_layout(G)

  plot_com(G, pos, partition, '../outputs/test_graph_color.png')