import dash
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State

from mainCode import app


@app.callback(Output('output-div', 'children'),
              Input('submit-button', 'n_clicks'),
              State('stored-data', 'data'),
              State('xaxis-data', 'value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    if n is None:
        return dash.no_update
    else:
        bar_fig = px.line(data, x=x_data, y=y_data, markers=True)

        return dcc.Graph(figure=bar_fig)
