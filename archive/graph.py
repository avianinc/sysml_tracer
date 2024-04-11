import json
import networkx as nx
import matplotlib.pyplot as plt

# Load and parse the JSON file
with open('data.json', 'r') as json_file:
    data = json.load(json_file)

# Create a new directed graph
graph = nx.DiGraph()

# Iterate over the JSON data and add nodes and edges to the graph
for element in data:
    # Each element is assumed to be a node, where '@id' is the unique identifier
    node_id = element.get('@id')
    if node_id:
        graph.add_node(node_id)
    
    # Check all fields of the element to find any other '@id' references
    # These references will be considered as edges in the graph
    for key, value in element.items():
        if isinstance(value, dict) and value.get('@id'):
            graph.add_edge(node_id, value.get('@id'))

# Draw the graph
plt.figure(figsize=(12, 12))  # Set the size of the graph
pos = nx.spring_layout(graph)  # Set the layout to spread nodes nicely
nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
plt.show()