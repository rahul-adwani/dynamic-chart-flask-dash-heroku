import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
import plotly.graph_objects as go

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/")
    
    dash_app.layout = html.Div([
        html.P("Select Stock Code:"),
        dcc.Dropdown(style={'width':'200px'},
                id='stock-list',
                options=[
                {'label': 'IBM', 'value': 'IBM'},
                {'label': 'Infosys', 'value': 'INFY'},
                {'label': 'TESCO PLC', 'value': 'TSCO.LON'},
                {'label': 'Daimler AG', 'value': 'DAI.DEX'},
                {'label': 'Shopify Inc', 'value': 'SHOP.TRT'},
                {'label': 'Reliance', 'value': 'RELIANCE.BSE'}],
                value='Select'
                ),
        html.Br(),
        html.P(id='selected-stock-code'),
        html.Div(id="output-graph"),
        ])

    @dash_app.callback(
        Output("selected-stock-code", "children"),
        Output("output-graph", "children"),
        Input("stock-list", "value"))
    def update_data(symbol):
        function = 'TIME_SERIES_DAILY'
        apikey = 'SZ1H8MS5IERRJ4F8'
        datatype = 'csv'
        URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(symbol) + '&apikey=SZ1H8MS5IERRJ4F8&datatype=csv'
        df = pd.read_csv(URL)
        if 'timestamp' in df.columns:
            fig = get_stock_price_fig(df)
            return dcc.Graph(figure=fig), 'Code Selected: {}'.format(symbol)
        else:
            return 'Select a Stock Code from the list.', 'No Company to Display'
        
    def get_stock_price_fig(df):
        colors = px.colors.qualitative.Plotly
        fig = go.Figure()
        fig.add_traces(go.Scatter(x=df['timestamp'], y = df['open'], name='Open', mode = 'lines', line=dict(color=colors[0])))
        fig.add_traces(go.Scatter(x=df['timestamp'], y = df['close'], name= 'Close', mode = 'lines', line=dict(color=colors[1])))
        #fig.add_traces(go.Scatter(x=df['timestamp'], y = df['high'], text='High', mode = 'lines', line=dict(color=colors[3])))
        #fig.add_traces(go.Scatter(x=df['timestamp'], y = df['low'], text='Low', mode = 'lines', line=dict(color=colors[4])))
        return fig
    
    return dash_app

if __name__ == '__main__':
    app.run_server(debug=True)