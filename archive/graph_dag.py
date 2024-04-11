import json
import networkx as nx
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt

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
        attributes = {
            '@type': element.get('@type', 'No Type'),
            'name': element.get('name', ''),
            'value': element.get('value', ''),
            'operator': element.get('operator', ''),
        }
        node_label = '\n'.join(f'{key}: {val}' for key, val in attributes.items() if val)
        G.add_node(node_id, label=node_label)
        node_info[node_id] = '<br>'.join([f'{k}: {v}' for k, v in element.items() if v])
        
    for key, value in element.items():
        if isinstance(value, dict) and value.get('@id'):
            target_id = value.get('@id')
            G.add_edge(node_id, target_id)
            edge_hover_info[(node_id, target_id)] = f'{key} → {target_id}'

# Check if the loaded graph is a DAG
if not nx.is_directed_acyclic_graph(G):
    raise ValueError("The graph must be a Directed Acyclic Graph (DAG) to use a hierarchical layout.")

# Use Graphviz 'dot' layout for hierarchical positioning of nodes
pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')

# Plotly visualization
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='text',
    mode='lines')

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    textposition='bottom center',
    hoverinfo='text',
    marker=dict(
        color='LightSkyBlue',
        size=10,
        line=dict(width=2)))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += (x,)
    node_trace['y'] += (y,)
    node_trace['text'] += (G.nodes[node]['label'],)
    node_trace['hovertext'] += (node_info.get(node, ''),)

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])
    edge_hover_text = edge_hover_info.get(edge, '')
    edge_trace['text'] += tuple([edge_hover_text, ''])

fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
    title='<br>Network graph made with Python',
    titlefont=dict(size=16),
    showlegend=False,
    margin=dict(b=0, l=0, r=0, t=25),
    annotations=[dict(text="By: Your Name/Your Organization", showarrow=False)],
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# Display the interactive graph in a browser
plot(fig, filename='Hierarchical-DAG.html')