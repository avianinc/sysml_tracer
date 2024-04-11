# SysML v2 API Tracer

## Overview

This tool assists SysML API developers in tracing and visualizing the highly nested relationships within a SysML v2 model. It uses a Python script and Jupyter notebooks to generate interactive network graphs that display these relationships.

## Setup

### Prerequisites

- An Anaconda environment is recommended for managing dependencies.
- Ensure a SysMLv2 Pilot Implementation API server is set up and accessible.

### Installation

1. Clone this repository to your local machine.
2. Create a new conda environment:

    ```bash
    conda create --name sysmlv2_vis python=3.8
    ```

3. Activate the newly created environment:

    ```bash
    conda activate sysmlv2_vis
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Creating and Publishing the Sample SysMLv2 Model

1. Navigate to the `/notebooks` directory.
2. Open `simple_constraint_model.ipynb` with Jupyter Notebook or JupyterLab.
3. Follow the instructions within the notebook to create and publish the sample SysMLv2 model to your SysMLv2 Pilot Implementation API server.

### Querying the Published Model

1. Still within the `/notebooks` directory, open `query_full_model.ipynb`.
2. Execute the notebook to query the simple model you previously published.
3. The results of this notebook will be saved to `/data/query_results.json`. Keep the models simple to limit the size of the NetworkX graph.

### Visualizing the Model

- **Using the Python Script:** Run the `sysml_graph.py` script. Upon completion, an interactive Plotly graph will be saved to `/html_out/sysmlv2_network_graph.html` and automatically opened in your web browser for review.

- **Below is an example graph**
![SysMLv2 Network Graph](/images/sysmlv2_network_graph.png)

- **Using a Jupyter Notebook:** Open `build_sysml_graph.ipynb` in the `/notebooks` folder. This notebook replicates the capability of the `sysml_graph.py` script, presenting the Plotly image within a notebook cell. A link to nbviewer online is provided for an example graph since Plotly network graphs do not render when committed to Git.

## Note

The purpose of this tool is to simplify the process of tracing the highly nested relationships of a SysMLv2 model for API developers. Limit the size of the NetworkX graph by keeping models simple to ensure efficient processing and visualization.

For further details or support, please refer to the official documentation of each tool and library used within this project.