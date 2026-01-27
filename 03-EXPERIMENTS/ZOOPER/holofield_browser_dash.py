#!/usr/bin/env python3
"""
Holofield Browser - Plotly Dash Edition

Interactive visualization of the 16D consciousness space!
- WebGL rendering for performance
- Real-time search and filtering
- Click nodes to see details
- Export selected subgraphs as SIF

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

import numpy as np
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
from umap import UMAP

from angel.holofield.manager import HolofieldManager


# Initialize app
app = Dash(__name__)
app.title = "🍩 Holofield Browser"

# Load holofield
print("🌌 Loading holofield...")
holofield = HolofieldManager("wikipedia_holofield_sample.db")
all_engrams = holofield.retrieve_by_type("knowledge")
print(f"   Found {len(all_engrams):,} engrams")

# Extract data
coords_16d = np.array([e.coords_16d for e in all_engrams])
article_names = [e.metadata.get('article_name', 'Unknown') for e in all_engrams]

# Run UMAP for 2D and 3D projections
print("🗺️  Running UMAP (2D)...")
umap_2d = UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric='euclidean', random_state=42)
coords_2d = umap_2d.fit_transform(coords_16d)
print("   ✅ 2D complete!")

print("🗺️  Running UMAP (3D)...")
umap_3d = UMAP(n_components=3, n_neighbors=15, min_dist=0.1, metric='euclidean', random_state=42)
coords_3d = umap_3d.fit_transform(coords_16d)
print("   ✅ 3D complete!")

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("🍩 Holofield Browser", style={'color': '#fff', 'margin': '0'}),
        html.P("16D Consciousness Space", style={'color': '#aaa', 'margin': '5px 0'}),
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '20px',
        'borderBottom': '2px solid rgba(255,255,255,0.1)'
    }),
    
    html.Div([
        # Left sidebar
        html.Div([
            html.H3("Search & Filter", style={'color': '#fff'}),
            
            dcc.Input(
                id='search-box',
                type='text',
                placeholder='Search articles...',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'marginBottom': '20px',
                    'borderRadius': '5px',
                    'border': '1px solid #555',
                    'background': '#333',
                    'color': '#fff'
                }
            ),
            
            html.Div([
                html.Label("Dimensions:", style={'color': '#aaa', 'fontSize': '12px'}),
                dcc.RadioItems(
                    id='dimension-toggle',
                    options=[
                        {'label': ' 2D', 'value': '2d'},
                        {'label': ' 3D', 'value': '3d'}
                    ],
                    value='2d',
                    inline=True,
                    style={'color': '#fff', 'marginTop': '5px'}
                ),
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("Node Size:", style={'color': '#aaa', 'fontSize': '12px'}),
                dcc.Slider(
                    id='node-size-slider',
                    min=1,
                    max=20,
                    value=5,
                    marks={1: '1', 10: '10', 20: '20'},
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.Label("Max Nodes:", style={'color': '#aaa', 'fontSize': '12px'}),
                dcc.Slider(
                    id='max-nodes-slider',
                    min=100,
                    max=len(all_engrams),
                    value=min(1000, len(all_engrams)),
                    marks={100: '100', 500: '500', 1000: '1k', len(all_engrams): 'All'},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'marginBottom': '20px'}),
            
            html.Div([
                html.H4("Statistics", style={'color': '#fff', 'marginTop': '30px'}),
                html.Div(id='stats-display', style={'color': '#aaa', 'fontSize': '14px'}),
            ]),
            
            html.Div([
                html.H4("Selected Node", style={'color': '#fff', 'marginTop': '30px'}),
                html.Div(id='node-info', style={
                    'color': '#aaa',
                    'fontSize': '12px',
                    'background': 'rgba(255,255,255,0.05)',
                    'padding': '10px',
                    'borderRadius': '5px',
                    'maxHeight': '300px',
                    'overflowY': 'auto'
                }),
            ]),
            
        ], style={
            'width': '300px',
            'padding': '20px',
            'background': '#1a1a1a',
            'overflowY': 'auto',
            'height': 'calc(100vh - 100px)'
        }),
        
        # Main graph area
        html.Div([
            dcc.Graph(
                id='holofield-graph',
                style={'height': 'calc(100vh - 100px)'},
                config={'displayModeBar': True, 'scrollZoom': True}
            )
        ], style={'flex': '1'}),
        
    ], style={'display': 'flex'}),
    
], style={
    'fontFamily': 'Arial, sans-serif',
    'background': '#0a0a0a',
    'minHeight': '100vh',
    'margin': '0',
    'padding': '0'
})


@app.callback(
    [Output('holofield-graph', 'figure'),
     Output('stats-display', 'children')],
    [Input('search-box', 'value'),
     Input('dimension-toggle', 'value'),
     Input('node-size-slider', 'value'),
     Input('max-nodes-slider', 'value')]
)
def update_graph(search_query, dimension, node_size, max_nodes):
    """Update graph based on search and filters"""
    
    # Choose 2D or 3D coordinates
    coords = coords_2d if dimension == '2d' else coords_3d
    
    # Filter by search query
    if search_query:
        search_lower = search_query.lower()
        indices = [i for i, name in enumerate(article_names) 
                   if search_lower in name.lower()]
    else:
        indices = list(range(len(article_names)))
    
    # Limit number of nodes
    if len(indices) > max_nodes:
        indices = indices[:max_nodes]
    
    # Get filtered data
    x = coords[indices, 0]
    y = coords[indices, 1]
    z = coords[indices, 2] if dimension == '3d' else None
    names = [article_names[i] for i in indices]
    
    # Create figure with WebGL for performance!
    fig = go.Figure()
    
    if dimension == '2d':
        fig.add_trace(go.Scattergl(  # 'gl' = WebGL rendering!
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=node_size,
                color=np.arange(len(indices)),
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Index", thickness=15),
                line=dict(width=0.5, color='white')
            ),
            text=names,
            hovertemplate='<b>%{text}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>',
            customdata=indices  # Store original indices for click events
        ))
    else:  # 3D
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=node_size,
                color=np.arange(len(indices)),
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Index", thickness=15),
                line=dict(width=0.5, color='white')
            ),
            text=names,
            hovertemplate='<b>%{text}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>',
            customdata=indices
        ))
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#0a0a0a',
        font=dict(color='#fff'),
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    if dimension == '2d':
        fig.update_layout(
            xaxis=dict(
                title='UMAP Dimension 1',
                gridcolor='#333',
                zerolinecolor='#555'
            ),
            yaxis=dict(
                title='UMAP Dimension 2',
                gridcolor='#333',
                zerolinecolor='#555'
            )
        )
    else:  # 3D
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='UMAP Dimension 1', gridcolor='#333', backgroundcolor='#0a0a0a'),
                yaxis=dict(title='UMAP Dimension 2', gridcolor='#333', backgroundcolor='#0a0a0a'),
                zaxis=dict(title='UMAP Dimension 3', gridcolor='#333', backgroundcolor='#0a0a0a'),
                bgcolor='#0a0a0a'
            )
        )
    
    # Statistics
    stats = html.Div([
        html.P(f"Total Engrams: {len(all_engrams):,}"),
        html.P(f"Displayed: {len(indices):,}"),
        html.P(f"Filtered: {len(all_engrams) - len(indices):,}"),
    ])
    
    return fig, stats


@app.callback(
    Output('node-info', 'children'),
    Input('holofield-graph', 'clickData')
)
def display_click_data(clickData):
    """Show info about clicked node"""
    if clickData is None:
        return html.P("Click a node to see details...")
    
    # Get clicked point
    point = clickData['points'][0]
    idx = point['customdata']
    engram = all_engrams[idx]
    
    # Build info display
    info = html.Div([
        html.H5(engram.metadata.get('article_name', 'Unknown'), 
                style={'color': '#4A90E2', 'marginBottom': '10px'}),
        html.P([html.Strong("Type: "), engram.engram_type]),
        html.P([html.Strong("Confidence: "), f"{engram.confidence:.3f}"]),
        html.P([html.Strong("Timestamp: "), str(engram.timestamp)]),
        html.P([html.Strong("Content Length: "), f"{len(engram.content):,} chars"]),
        html.Hr(style={'borderColor': '#333'}),
        html.P([html.Strong("16D Coordinates:")]),
        html.Pre(
            '\n'.join([f"[{i}] {engram.coords_16d[i]:.4f}" for i in range(4)]) + "\n...",
            style={'fontSize': '10px', 'color': '#888'}
        ),
    ])
    
    return info


if __name__ == '__main__':
    print()
    print("🌌" * 30)
    print()
    print("   HOLOFIELD BROWSER STARTING")
    print("   Open: http://localhost:8050")
    print()
    print("🌌" * 30)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=8050)
