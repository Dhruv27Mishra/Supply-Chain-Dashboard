import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Datasets
inventory_df = pd.read_csv("inventory_data.csv")
transportation_df = pd.read_csv("transportation_data.csv")
order_df = pd.read_csv("order_data.csv")
reverse_logistics_df = pd.read_csv("reverse_logistics_data.csv")

# Sample location coordinates 
location_coords = {
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'Chicago': (41.8781, -87.6298),
    'Houston': (29.7604, -95.3698),
    'Phoenix': (33.4484, -112.0740)
}

# Add latitude and longitude columns
transportation_df['Origin Lat'] = transportation_df['Origin'].map(lambda loc: location_coords.get(loc, (0, 0))[0])
transportation_df['Origin Lon'] = transportation_df['Origin'].map(lambda loc: location_coords.get(loc, (0, 0))[1])
transportation_df['Destination Lat'] = transportation_df['Destination'].map(lambda loc: location_coords.get(loc, (0, 0))[0])
transportation_df['Destination Lon'] = transportation_df['Destination'].map(lambda loc: location_coords.get(loc, (0, 0))[1])

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

COLOR_SCHEME = {
    'background': '#ffc107',  # Yellow
    'text': '#007bff',  # Blue
    'graph_background': '#ffffff',  # White
    'button_color': '#007bff',  # Blue
    'button_text_color': '#ffffff',  # White
    'border_color': '#007bff',  # Blue
    'highlight': '#007bff',  # Blue
    'highlight_text': '#ffffff'  # White
}

# Layout 
app.layout = html.Div(style={'backgroundColor': COLOR_SCHEME['background'], 'padding': '20px'}, children=[
    html.H1("Walmart Supply Chain Dashboard", style={'textAlign': 'center', 'color': COLOR_SCHEME['text']}),

    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker',
                start_date=order_df['Order Date'].min(),
                end_date=order_df['Order Date'].max(),
                display_format='YYYY-MM-DD',
                style={'width': '100%', 'padding': '10px', 'borderColor': COLOR_SCHEME['border_color']}
            )
        ], width=6),

        dbc.Col([
            dcc.Dropdown(
                id='warehouse-dropdown',
                options=[{'label': warehouse, 'value': warehouse} for warehouse in inventory_df['Warehouse Location'].unique()],
                multi=True,
                placeholder="Select Warehouse",
                style={'width': '100%', 'borderColor': COLOR_SCHEME['border_color']}
            )
        ], width=6)
    ], style={'margin': '20px 0'}),

    dbc.Row([
        dbc.Col([
            dcc.Input(
                id='product-search',
                type='text',
                placeholder='Search Products...',
                style={'width': '100%', 'padding': '10px', 'borderColor': COLOR_SCHEME['border_color']}
            ),
        ], width=6),

        dbc.Col([
            html.Button("Download Inventory Data", id='download-inventory', n_clicks=0, style={
                'width': '100%',
                'padding': '10px',
                'backgroundColor': COLOR_SCHEME['button_color'],
                'color': COLOR_SCHEME['button_text_color'],
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontSize': '16px'
            })
        ], width=6)
    ], style={'margin': '20px 0'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='real-time-tracking', style={'backgroundColor': COLOR_SCHEME['graph_background']})
        ], width=6),

        dbc.Col([
            dcc.Graph(id='kpi-metrics', style={'backgroundColor': COLOR_SCHEME['graph_background']})
        ], width=6)
    ], style={'margin': '20px 0'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H2("Inventory Levels", style={'color': COLOR_SCHEME['text']})),
                dbc.CardBody(dcc.Graph(id='inventory-graph', style={'backgroundColor': COLOR_SCHEME['graph_background']}))
            ], style={'marginBottom': '20px', 'borderColor': COLOR_SCHEME['border_color']}),

            dbc.Card([
                dbc.CardHeader(html.H2("Transportation Status", style={'color': COLOR_SCHEME['text']})),
                dbc.CardBody([
                    dcc.Graph(id='transportation-map', style={'backgroundColor': COLOR_SCHEME['graph_background']}),
                    html.Button("Refresh Data", id='refresh-button', n_clicks=0, style={
                        'margin': '10px',
                        'padding': '10px',
                        'backgroundColor': COLOR_SCHEME['button_color'],
                        'color': COLOR_SCHEME['button_text_color'],
                        'border': 'none',
                        'borderRadius': '5px',
                        'cursor': 'pointer',
                        'fontSize': '16px'
                    })
                ])
            ], style={'marginBottom': '20px', 'borderColor': COLOR_SCHEME['border_color']}),

            dbc.Card([
                dbc.CardHeader(html.H2("Order Fulfillment Rate", style={'color': COLOR_SCHEME['text']})),
                dbc.CardBody(dcc.Graph(id='order-fulfillment-graph', style={'backgroundColor': COLOR_SCHEME['graph_background']}))
            ], style={'marginBottom': '20px', 'borderColor': COLOR_SCHEME['border_color']}),

            dbc.Card([
                dbc.CardHeader(html.H2("Returns Trend Analysis", style={'color': COLOR_SCHEME['text']})),
                dbc.CardBody(dcc.Graph(id='returns-trend-graph', style={'backgroundColor': COLOR_SCHEME['graph_background']}))
            ], style={'marginBottom': '20px', 'borderColor': COLOR_SCHEME['border_color']})
        ])
    ])
])

# Callbacks for graph updation
@app.callback(
    Output('real-time-tracking', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_real_time_tracking(start_date, end_date):
    filtered_df = inventory_df[(inventory_df['Current Stock Level'] > 0)]
    latest_data = filtered_df.groupby('Product ID').apply(lambda x: x.sort_values('Current Stock Level').iloc[-1]).reset_index(drop=True)
    
    fig = px.scatter(latest_data, x='Product ID', y='Current Stock Level', color='Warehouse Location', size='Current Stock Level',
                     title="Real-time Tracking of Items",
                     labels={"Product ID": "Product ID", "Current Stock Level": "Current Stock Level"})
    fig.update_layout(title_x=0.5, plot_bgcolor=COLOR_SCHEME['graph_background'],
                      xaxis_title="Product ID", yaxis_title="Current Stock Level",
                      title_font_size=24, xaxis_title_font_size=18, yaxis_title_font_size=18)
    return fig

@app.callback(
    Output('kpi-metrics', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_kpi_metrics(start_date, end_date):
    filtered_orders_df = order_df[(order_df['Order Date'] >= start_date) & (order_df['Order Date'] <= end_date)]
    total_orders = filtered_orders_df['Order ID'].count()
    on_time_orders = filtered_orders_df[filtered_orders_df['Fulfillment Status'] == 'On Time'].shape[0]
    delayed_orders = total_orders - on_time_orders

    fig = px.bar(x=['Total Orders', 'On Time Orders', 'Delayed Orders'],
                 y=[total_orders, on_time_orders, delayed_orders],
                 labels={'x': 'KPI', 'y': 'Value'},
                 title="Key Performance Indicators (KPIs)")
    fig.update_layout(title_x=0.5, plot_bgcolor=COLOR_SCHEME['graph_background'],
                      xaxis_title="KPI", yaxis_title="Value",
                      title_font_size=24, xaxis_title_font_size=18, yaxis_title_font_size=18)
    return fig

@app.callback(
    Output('inventory-graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('warehouse-dropdown', 'value')]
)
def update_inventory_graph(start_date, end_date, selected_warehouses):
    filtered_df = inventory_df[(inventory_df['Current Stock Level'] > 0)]
    if selected_warehouses:
        filtered_df = filtered_df[filtered_df['Warehouse Location'].isin(selected_warehouses)]
    
    fig = px.bar(filtered_df, x="Product Name", y="Current Stock Level", color="Warehouse Location", title="Current Inventory Levels")
    fig.update_layout(title_x=0.5, plot_bgcolor=COLOR_SCHEME['graph_background'])
    return fig

@app.callback(
    Output('transportation-map', 'figure'),
    Input('refresh-button', 'n_clicks')
)
def update_transportation_map(n_clicks):
    fig = px.scatter_mapbox(transportation_df, lat='Origin Lat', lon='Origin Lon',
                            color="Status", size_max=15, zoom=3,
                            mapbox_style="carto-positron",
                            title="Transportation Status Map")
    fig.update_layout(title_x=0.5, mapbox=dict(center=dict(lat=37.0902, lon=-95.7129), zoom=4),
                      title_font_size=24)
    return fig

@app.callback(
    Output('order-fulfillment-graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_order_fulfillment_graph(start_date, end_date):
    filtered_df = order_df[(order_df['Order Date'] >= start_date) & (order_df['Order Date'] <= end_date)]
    fulfillment_status_counts = filtered_df['Fulfillment Status'].value_counts()

    fig = px.pie(values=fulfillment_status_counts, names=fulfillment_status_counts.index,
                 title="Order Fulfillment Rate")
    fig.update_layout(title_x=0.5, plot_bgcolor=COLOR_SCHEME['graph_background'],
                      title_font_size=24)
    return fig

@app.callback(
    Output('returns-trend-graph', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('warehouse-dropdown', 'value')]
)
def update_returns_trend_graph(start_date, end_date, selected_warehouses):
    # Filter data
    filtered_df = reverse_logistics_df[
        (reverse_logistics_df['Return Date'] >= start_date) &
        (reverse_logistics_df['Return Date'] <= end_date)
    ].copy()  

    if selected_warehouses:
        filtered_df = filtered_df[filtered_df['Warehouse Location'].isin(selected_warehouses)]
    
    # Month column
    filtered_df.loc[:, 'Month'] = pd.to_datetime(filtered_df['Return Date']).dt.to_period('M').astype(str)
    
    # Return trends
    return_trends = filtered_df.groupby('Month').size().reset_index(name='Returns')
    
    # Line chart for trends
    fig = px.line(return_trends, x='Month', y='Returns', title="Returns Trend Analysis")
    fig.update_layout(title_x=0.5, plot_bgcolor=COLOR_SCHEME['graph_background'],
                      xaxis_title="Month", yaxis_title="Number of Returns",
                      title_font_size=24, xaxis_title_font_size=18, yaxis_title_font_size=18)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
