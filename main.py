import json
from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests

app = Flask(__name__)

# Create an empty NetworkX graph
G = nx.Graph()

# Route to display the form and visualize the graph
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    if request.method == 'POST':
        url = request.form['url']

        # Make a GET request to the URL to retrieve JSON data
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()

            # Clear the existing graph
            G.clear()

            # Add nodes and edges from the JSON data
            for node_id, node_data in json_data["result"]["nodes"].items():
                if not G.has_node(node_id):  # Check if the node already exists
                    G.add_node(node_id, **node_data)

            for edge_id, edge_data in json_data["result"]["edges"].items():
                G.add_edge(
                    edge_data["links"]["0"]["node"],
                    edge_data["links"]["1"]["node"],
                    **edge_data
                )
                graphml_filename = 'graph.graphml'
                # Convert node and edge data to strings
                # Add nodes and edges from the JSON data

                expoergraph = nx.Graph()
            for node_id, node_data in json_data["result"]["nodes"].items():
                    expoergraph.add_node(node_id, attr_data=json.dumps(node_data))

            for edge_id, edge_data in json_data["result"]["edges"].items():
                    expoergraph.add_edge(
                        edge_data["links"]["0"]["node"],
                        edge_data["links"]["1"]["node"],
                        attr_data=json.dumps(edge_data)
                    )

                # Save the graph to GraphML format
            nx.write_graphml(expoergraph, graphml_filename)



        else:
            return "Failed to retrieve JSON data from the URL."


    # Generate a graph visualization
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=10)

    # Convert the graph visualization to a PNG image
    plt.axis('off')
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode()

    # Get node and edge data for tables
    node_data = {}
    for node_id, attributes in G.nodes(data=True):
        node_data[node_id] = attributes

    edge_data = {}
    for u, v, attributes in G.edges(data=True):
        edge_data[(u, v)] = attributes

    # Render the HTML template with the graph image and data tables
    return render_template('index.html', graph_image=img_base64, node_data=node_data, edge_data=edge_data)


# Route to display the initial form
@app.route('/')
def index():
    return render_template('index.html', graph_image=None, node_data=None, edge_data=None)

if __name__ == '__main__':
    app.run(debug=True)
