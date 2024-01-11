from itertools import combinations

import networkx as nx
import matplotlib.pyplot as plt

class Hypergraph:
    def __init__(self, edges):
        self.edges = edges
def convertHypertoNormal(hypergraph):
     graph_edges = set()
     node_mapping = {}

     for hyperedge in hypergraph.edges:
         hyperedge_id = frozenset(hyperedge)
         graph_edges.add(hyperedge_id)

         for node in hyperedge:
             if node not in node_mapping:
                 node_mapping[node] = set()
             node_mapping[node].add(hyperedge_id)

     return graph_edges, node_mapping


def print_graph(graph_edges, node_mapping):
    print("Nodes:")
    for node, hyperedges in node_mapping.items():
        print(f"{node}: {hyperedges}")

    print("\nEdges:")
    for edge in graph_edges:
        print(edge)
def hypergraph_to_bipartite(hypergraph):
    bipartite_graph = {"left": set(), "right": set()}

    for hyperedge in hypergraph.edges:
        bipartite_graph["left"].add(frozenset(hyperedge))
        for node in hyperedge:
            bipartite_graph["right"].add(node)

    return bipartite_graph

def print_bipartite_graph(bipartite_graph):
    print("Left Nodes (Hyperedges):")
    for node in bipartite_graph["left"]:
        print(node)
    print("\nRight Nodes:")
    for node in bipartite_graph["right"]:
        print(node)
def hypergraph_to_clique(hypergraph):
    return   list(nx.find_cliques(hypergraph))


def k_cliques(graph):
    # 2-cliques
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = 2

    while cliques:
        # result
        yield k, cliques

        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))
        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1


def print_cliques(graph):
    for k, cliques in k_cliques(graph):
        info = k, len(cliques), cliques[:3]
        print("cli" , cliques)
        print('%d-cliques: #%d, %s ...' % info)
def hypergraph_to_star(hypergraph):
    central_node = "Center"
    star_edges = [tuple(hyperedge) for hyperedge in hypergraph.edges]
    star_edges.append((central_node, *range(1, len(hypergraph.edges) + 1)))
    return star_edges

def lawler_expansion(hypergraph, vertex_set):
    # Calculate Lawler-Expansion
    edges_leaving_set = sum(len(hyperedge) for hyperedge in hypergraph.edges if any(node in vertex_set for node in hyperedge))
    expansion = edges_leaving_set / len(vertex_set) if len(vertex_set) > 0 else 0
    return expansion
hypergraph = nx.Graph()
hypergraph.add_edges_from([(1, 3 ), (2, 3), (4, 6), (6, 3) , (4, 3) ,(5,6), (5,1) ])

graph_edges, node_mapping = convertHypertoNormal(hypergraph)
print_graph(graph_edges, node_mapping)
bipartite_graph = hypergraph_to_bipartite(hypergraph)
print_bipartite_graph(bipartite_graph)
clique_structure = hypergraph_to_clique(hypergraph)
print("Clique Structure:", clique_structure)
max_clique_graph = nx.make_max_clique_graph(hypergraph)
print("max_clique_graph:", max_clique_graph)
print("max_clique_graph nodes :", max_clique_graph)
print("------------------")

print_cliques(hypergraph)
# Draw the original graph
plt.figure(figsize=(8, 4))
plt.subplot(121)
nx.draw(hypergraph, with_labels=True, font_weight='bold')
plt.title("Original Graph")

# Draw the maximal clique graph
plt.subplot(122)
nx.draw(max_clique_graph, with_labels=True, font_weight='bold')
plt.title("Maximal Clique Graph")
star_structure = hypergraph_to_star(hypergraph)

plt.tight_layout()
plt.show()
print("Star Structure:", star_structure)
vertex_set = {1, 2}
lawler_expansion_value = lawler_expansion(hypergraph, vertex_set)
print("Lawler-Expansion Value:", lawler_expansion_value)