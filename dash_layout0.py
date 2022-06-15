from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from matplotlib.pyplot import text
from datetime import date

from filter_graph import FilterGraph

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal')
])

text_style = {
    "transform": "translateY(0%)", # vertical alignment
    "position": "relative",
    "display": "inline-block",
    "margin-left": "10px",
    "font-size" : "30px",
    "font-family": "Arial",
    "line-height": "0%",
}
dropdown_style = {
    "display": "inline-block",
    "width": "200px",
    "height": "30px",
    "margin-left": "10px",
    "font-size": "20px",
    "font-family": "Arial",
    "line-height": "0%",
}

date_picker_style = {
    "display": "inline-block",
    # "width": "200px",
    "height": "40px",
    "margin-left": "10px",
    # "font-family": "Arial",
    "line-height": "0%",
}

app.layout = html.Div([
    html.Div([
        html.Div(html.P("At "), style = text_style),
        html.Div([
            dcc.Dropdown(['Jeffries Point', 'Logan Runway 1', 'Logan Runway 2'], 'Jeffries Point'),
        ], style = dropdown_style),
        html.Div(html.P(", what were the pollution levels between"), style = text_style),

        html.Div([
            dcc.DatePickerSingle(
                date = date(2019, 12, 1),
                display_format='MM/DD/Y',
                id = 'start-date',
            ),
        ], style = date_picker_style),
        html.Div(html.P(" and "), style = text_style),

        html.Div([
            dcc.DatePickerSingle(
                date = date(2020, 1, 1),
                display_format='MM/DD/Y',
                id = 'end-date',
            ),
        ], style = date_picker_style),
        html.Div(html.P("when the wind was blowing"), style = text_style),
        html.Div([
            dcc.Dropdown(options = [
            {'label': 'North',     'value': 'N'},
            {'label': 'Northeast', 'value': 'NE'},
            {'label': 'East',      'value': 'E'},
            {'label': 'Southeast', 'value': 'SE'},
            {'label': 'South',     'value': 'S'},
            {'label': 'Southwest', 'value': 'SW'},
            {'label': 'West',      'value': 'W'},
            {'label': 'Northwest', 'value': 'NW'},
        ], value = 'Northeast', id = "wind-direction"),
        ], style = dropdown_style),
        html.Div(html.P("?"), style = text_style),
    ]),
    dcc.Graph(id='graph-with-slider'),
])

filter_graph = FilterGraph()

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('start-date', 'date'),
    Input('end-date', 'date'),
    Input('wind-direction', 'value'),
)
def update_figure(start_date, end_date, wind_direction):
    return filter_graph.update_figure(start_date, end_date, wind_direction)


if __name__ == '__main__':
    app.run_server(debug=True)