
def get_insignificant_edges(sig, edge_list):
  removed_edges = []
  for k in range(len(sig)):
    if not sig[k]:
      edge = edge_list[k]
      removed_edges.append(edge)
  
  return removed_edges