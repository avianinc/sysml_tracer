import json
import plotly.graph_objects as go
import networkx as nx
from plotly.offline import plot

# Load and parse the JSON file
with open('data/qrc.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize a directed graph in networkx
G = nx.DiGraph()

# Process nodes and edges and build hover text details
node_info = {}
edge_hover_info = {}
for element in data:
    node_id = element.get('@id')
    if node_id:
        # Collect the required attributes, if present
        attributes = {
            '@type': element.get('@type', 'No Type'),
            'name': element.get('name', ''),
            'value': element.get('value', ''),
            'operator': element.get('operator', ''),
        }
        node_label = '\n'.join(f'{key}: {val}' for key, val in attributes.items() if val)
        G.add_node(node_id, label=node_label)
        # Store the full JSON data of the node for hover info
        node_info[node_id] = '<br>'.join([f'{k}: {v}' for k, v in element.items() if v])
        
    # Add edges and store connection data for hover info
    for key, value in element.items():
        if isinstance(value, dict) and value.get('@id'):
            target_id = value.get('@id')
            G.add_edge(node_id, target_id)
            edge_hover_info[(node_id, target_id)] = f'{key} → {target_id}'

# Use a layout algorithm to position the nodes
node_id_to_position = nx.spring_layout(G)

# Initialize edge trace for Plotly
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='text',
    mode='lines',
    text=[])

# Add edge positions to the edge trace and the respective hover text
for edge in G.edges():
    x0, y0 = node_id_to_position[edge[0]]
    x1, y1 = node_id_to_position[edge[1]]
    edge_trace['x'] += (x0, x1, None)
    edge_trace['y'] += (y0, y1, None)
    edge_hover_text = edge_hover_info.get(edge, '')
    edge_trace['text'] += (edge_hover_text, edge_hover_text, None)

# Initialize node trace for Plotly
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hovertext=[],
    hoverinfo='text',
    textposition='bottom center',
    marker=dict(
        showscale=False,
        color='LightSkyBlue',
        size=10,
        line_width=2))

# Add node positions, labels, and hover texts to the node trace
for node in G.nodes():
    x, y = node_id_to_position[node]
    node_trace['x'] += (x,)
    node_trace['y'] += (y,)
    node_trace['text'] += (G.nodes[node]['label'],)
    node_trace['hovertext'] += (node_info.get(node, ''),)

# Create the figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Interactive network graph',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# Display the interactive graph in a browser
plot(fig, filename='network.html')