import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_cytoscape as cyto
import json

# Load the JSON data from the provided file
with open('data/qrc.json', 'r') as f:
    data = json.load(f)

# Define the function to create Cytoscape elements from JSON data
def create_elements_from_json(data):
    elements = []
    
    for node_data in data:
        node_id = node_data.get('@id')

        # Collect all data for the tooltip display
        tooltip_data = '\n'.join([f'{key}: {value}' for key, value in node_data.items()])

        # Create the node with its tooltip
        elements.append({
            'data': {'id': node_id},
            'position': {'x': 20, 'y': 20},  # Dummy positions
            'grabbable': True,
            'selectable': True,
            'classes': 'node-tooltip',
            'title': tooltip_data  # This will be used to show on hover
        })

        # Create edges
        for key, value in node_data.items():
            if isinstance(value, dict) and '@id' in value:
                target_id = value['@id']
                elements.append({
                    'data': {'source': node_id, 'target': target_id}
                })

    return elements

elements = create_elements_from_json(data)

app = dash.Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='network-graph',
        elements=elements,
        style={'width': '100%', 'height': '400px'},
        layout={'name': 'cose'},  # CoSE layout
        stylesheet=[{
            'selector': '.node-tooltip',
            'style': {
                'content': 'data(id)',
                'text-valign': 'bottom',
                'text-halign': 'right',
                'background-color': '#0074D9'
            }
        }, {
            'selector': '.edge-tooltip',
            'style': {
                'content': 'data(id)',
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': '#9dbaea',
                'arrow-scale': 1
            }
        }, {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': '#9dbaea',
                'arrow-scale': 1
            }
        }]
    )
])

@app.callback(
    Output('network-graph', 'stylesheet'),
    [
        Input('network-graph', 'selectedNodeData'),
        Input('network-graph', 'selectedEdgeData')
    ],
    prevent_initial_call=True
)
def update_stylesheet(selected_node_data, selected_edge_data):
    if not selected_node_data and not selected_edge_data:
        return [{
            'selector': 'node',
            'style': {
                'background-color': '#0074D9'
            }
        }, {
            'selector': 'edge',
            'style': {
                'line-color': '#9dbaea'
            }
        }]
    
    stylesheet = [{
        'selector': 'node',
        'style': {
            'background-color': '#0074D9'
        }
    }, {
        'selector': 'edge',
        'style': {
            'line-color': '#9dbaea'
        }
    }]

    if selected_node_data:
        for node in selected_node_data:
            stylesheet.append({
                'selector': f'node[id = "{node["id"]}"]',
                'style': {
                    'background-color': 'red'
                }
            })

    if selected_edge_data:
        for edge in selected_edge_data:
            stylesheet.append({
                'selector': f'edge[source="{edge["source"]}"][target="{edge["target"]}"]',
                'style': {
                    'line-color': 'red'
                }
            })

    return stylesheet

if __name__ == '__main__':
    app.run_server(debug=True)