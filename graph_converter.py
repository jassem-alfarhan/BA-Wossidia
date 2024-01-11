from itertools import combinations

import networkx as nx
# convert nx graph to biparite nx graph
def convertgraphtobipartite(graph):
    bipartite_graph = nx.Graph()
    bipartite_graph.add_nodes_from(graph.nodes(data=True), bipartite=0)
    bipartite_graph.add_nodes_from(graph.edges(), bipartite=1)
    bipartite_graph.add_edges_from(graph.edges())
    return bipartite_graph

def convertgraphtoClique(graph):
    Clique_graph = nx.Graph()
    nx.find_cliques(Clique_graph)
    clique = set()
    for hyperedge in graph.edges:
        clique.update(hyperedge)


    return Clique_graph
def convertgraphtoStar(graph):
    central_node = "Center"
    star_edges = [tuple(hyperedge) for hyperedge in graph.edges]
    star_edges.append((central_node, *range(1, len(graph.edges) + 1)))
    return star_edges


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
        print('%d-cliques: #%d, %s ...' % info)


# get wooida fata as normal graph
def get_normal_graph(json_data):
    G = nx.Graph()
    G.clear()
    for node_id, node_data in json_data["result"]["nodes"].items():
        if not G.has_node(node_id):  # Check if the node already exists
            G.add_node(int(node_id), **node_data)
    for edge_id, edge_data in json_data["result"]["edges"].items():
        if len(edge_data.get("links", [])) <= 2:
          node_0 = edge_data["links"]["0"]["node"]
          node_1 = edge_data["links"]["1"]["node"]
          if not G.has_node(node_0):
            G.add_node(node_0)
          if not G.has_node(node_1):
            G.add_node(node_1)
          if not G.has_edge(node_0, node_1):
            G.add_edge(node_0, node_1, **edge_data)
        else:
            node_0 = edge_data["links"]["0"]["node"]
            node_1 = edge_data["links"]["1"]["node"]
            node_2 = edge_data["links"]["2"]["node"]
            if not G.has_node(node_0):
                G.add_node(node_0)
            if not G.has_node(node_1):
                G.add_node(node_1)
            if not G.has_node(node_2):
                G.add_node(node_2)
            if not G.has_edge(node_0, node_1):
                G.add_edge(node_0, node_1, **edge_data)
            if not G.has_edge(node_1, node_2):
                G.add_edge(node_1, node_2, **edge_data)
    return  G
