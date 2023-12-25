from re import compile
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from math import prod

COMPONENTS_RE = compile(r"[a-z]+")

nodes = defaultdict(list)
for line in open("input.txt"):
    node, *components = COMPONENTS_RE.findall(line)
    nodes[node].extend(components)
    for c in components:
        nodes[c].append(node)

# Analyze graph visually
g = nx.Graph(nodes)
pos = nx.spectral_layout(g)
nx.draw(g, pos=pos, with_labels=True)
plt.savefig("graph_part_1.png")

# After analyzing the graph, we can see the three edges that are connecting two largers sets of nodes
# We can remove them and then count how many nodes are left in each set
edges_to_remove = [("qdp", "jxx"), ("mlp", "qqq"), ("zbr", "vsx")]
for edge in edges_to_remove:
    g.remove_edge(*edge)


subgraphs = list(nx.connected_components(g))
print(prod(len(s) for s in subgraphs))
