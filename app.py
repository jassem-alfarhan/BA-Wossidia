import json
from flask import Flask, request ,jsonify
import networkx as nx
import json
import requests
from flask_cors import CORS
from networkx.readwrite import json_graph

from graph_converter import convertgraphtobipartite, k_cliques, get_normal_graph, print_cliques

app = Flask(__name__)

CORS(app)
# Create an empty NetworkX graph
G = nx.Graph()

# Route to display the form and visualize the graph
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    if request.method == 'POST':
        data = request.get_json()
        url = data['url']
        # Make a GET request to the URL to retrieve JSON data
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            X =  get_normal_graph(json_data)
            print("X " , X)

            # Clear the existing graph
            G.clear()
            hyperedges = []  # To store hyperedges
            # Add nodes and edges from the JSON data
            for node_id, node_data in json_data["result"]["nodes"].items():
                if not G.has_node(node_id):  # Check if the node already exists
                    G.add_node(node_id, **node_data)

            for edge_id, edge_data in json_data["result"]["edges"].items():
                node_0 = str(edge_data["links"]["0"]["node"])
                node_1 = str(edge_data["links"]["1"]["node"])
                if not G.has_node(node_0):
                    G.add_node(node_0)
                if not G.has_node(node_1):
                    G.add_node(node_1)
                if not G.has_edge(node_0, node_1):
                    G.add_edge(node_0, node_1, **edge_data)


            nodes = []
            edges = []

            for node_id, node_data in json_data["result"]["nodes"].items():
                nodes.append({
                    "id": node_id,
                    "label": node_data.get("label", str(node_id)) ,
                    "info": node_data })
            for edge_id, edge_data in json_data["result"]["edges"].items():
                if len(edge_data.get("links", [])) <= 2:
                    edges.append({
                        "from": edge_data["links"]["0"]["node"],
                        "to": edge_data["links"]["1"]["node"],
                        "info": edge_data,
                        "id": edge_id
                    })
                else:
                    links = edge_data.get("links", {})

                    # Iterate over the values of the dictionary
                    nodes_list = [link["node"] for link in links.values()]
                    hyperedges.append({
                        "id": edge_id,
                        "label": edge_data.get("label", str(edge_id)),
                        "nodes": nodes_list
                    })




            normalnodes = []
            normaledges = []

            for node_id, node_data in json_data["result"]["nodes"].items():
                normalnodes.append({
                    "id": int(node_id),
                    "label": node_data.get("label", str(node_id)) ,
                    "info": node_data })
            for edge_id, edge_data in json_data["result"]["edges"].items():
                if len(edge_data.get("links", [])) <= 2:
                    node_0 = edge_data["links"]["0"]["node"]
                    node_1 = edge_data["links"]["1"]["node"]
                    normaledges.append({
                        "from": node_0,
                        "to": node_1,
                        "info": edge_data,
                        "id": edge_id
                    })
                else:
                    node_0 = edge_data["links"]["0"]["node"]
                    node_1 = edge_data["links"]["1"]["node"]
                    node_2 = edge_data["links"]["2"]["node"]

                    # Iterate over the values of the dictionary

                    normaledges.append({
                        "from": node_0,
                        "to": node_1,
                        "info": edge_data,
                        "id": edge_id
                    })
                    normaledges.append({
                        "from": node_1,
                        "to": node_2,
                        "info": edge_data,
                        "id": edge_id*2
                    })
# Star graph
            Starnodes = []
            Staredges = []

            for node_id, node_data in json_data["result"]["nodes"].items():
                Starnodes.append({
                    "id": int(node_id),
                    "label": node_data.get("label", str(node_id)),
                    "info": node_data})
            for edge_id, edge_data in json_data["result"]["edges"].items():
                if len(edge_data.get("links", [])) <= 2:
                    node_0 = edge_data["links"]["0"]["node"]
                    node_1 = edge_data["links"]["1"]["node"]
                    Staredges.append({
                        "from": node_0,
                        "to": node_1,
                        "info": edge_data,
                        "id": edge_id
                    })
                else:
                    node_0 = edge_data["links"]["0"]["node"]
                    node_1 = edge_data["links"]["1"]["node"]
                    node_2 = edge_data["links"]["2"]["node"]
                    Starnodes = [node for node in Starnodes if node["id"] != node_2]
                    # Iterate over the values of the dictionary

                    Staredges.append({
                        "from": node_0,
                        "to": node_1,
                        "info": edge_data,
                        "id": edge_id
                    })


            bibnodes = []
            bibedges = []

            for node_id, node_data in json_data["result"]["nodes"].items():

                bibnodes.append({
                    "id": node_id,
                    "label": node_data.get("label", str(node_id)),
                    "info": node_data ,
                     "bipartite" : 0    })
            for edge_id, edge_data in json_data["result"]["edges"].items():

                if len(edge_data.get("links", [])) <= 2:
                    node_0 = str(edge_data["links"]["0"]["node"])
                    node_1 = str(edge_data["links"]["1"]["node"])
                    bibedges.append({
                        "from": edge_data["links"]["0"]["node"],
                        "to": edge_data["links"]["1"]["node"],
                        "info": edge_data,
                        "id": edge_id
                    })
                    # Include nodes in bibnodes with bipartite information
                    bibnodes = [node for node in bibnodes if node["id"] != node_0]
                    bibnodes = [node for node in bibnodes if node["id"] != node_1]
                    bibnodes.append({
                        "id": node_0,
                        "label": node_0,
                        "bipartite": 0
                    })
                    bibnodes.append({
                        "id": node_1,
                        "label": node_1,
                        "bipartite": 1
                    })
                else:
                    node_0 = str(edge_data["links"]["0"]["node"])
                    node_1 = str(edge_data["links"]["1"]["node"])
                    node_2 = str(edge_data["links"]["2"]["node"])
                    bibnodes = [node for node in bibnodes if node["id"] != node_0]
                    bibnodes = [node for node in bibnodes if node["id"] != node_1]
                    bibnodes = [node for node in bibnodes if node["id"] != node_2]
                    bibedges.append({
                        "from": edge_data["links"]["0"]["node"],
                        "to": edge_data["links"]["1"]["node"],
                        "info": edge_data,
                        "id": edge_id
                    })
                    bibedges.append({
                        "from": edge_data["links"]["1"]["node"],
                        "to": edge_data["links"]["2"]["node"],
                        "info": edge_data,
                        "id": edge_id*2
                    })

                    bibnodes.append({
                    "id": node_0,
                    "label": node_0,
                    "bipartite": 0
                    })
                    bibnodes.append({
                    "id": node_1,
                    "label": node_1,
                    "bipartite": 1
                    })
                    bibnodes.append({
                    "id": node_2,
                    "label": node_2,
                    "bipartite": 0
                    })

            B = convertgraphtobipartite(G)
            print_cliques(X)

            C = nx.make_max_clique_graph(X)




            print("B graph", B)


            graph_json = json_graph.node_link_data( C)
            print(" bibnodes data", bibnodes)
            print(" bibedges data", bibedges)

            # Prepare the graph data in the format expected by Vis.js
            vis_data = {
                "nodes": nodes,
                "edges": edges,
                "normalnodes" : normalnodes,
                "normaledges" : normaledges ,
                "hyperedges": hyperedges,
                "bipartite": graph_json,
                "bibnodes" :  bibnodes ,
                "bibedges" :   bibedges  ,

               "starnodes" : Starnodes,
               "staredges" : Staredges,
                "cliq" : graph_json ,


            }

            return jsonify(vis_data), 200

        else:
            return "Failed to retrieve JSON data from the URL.",400






# Route to display the initial form
@app.route('/')
def index():
    return "hello world" , 200

if __name__ == '__main__':
    app.run(debug=True)
