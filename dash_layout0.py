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
}
dropdown_style = {
    "display": "inline-block",
    "width": "200px",
    "height": "30px",
    "margin-left": "10px",
    "font-size": "20px",
}

date_picker_style = {
    "display": "inline-block",
    # "width": "200px",
    "height": "40px",
    "margin-left": "10px",
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
        html.Div(html.P(" ?"), style = text_style),
    ]),
    dcc.Graph(id='graph-with-slider'),
])

filter_graph = FilterGraph()

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('start-date', 'date'),
    Input('end-date', 'date')
)
def update_figure(start_date, end_date):
    return filter_graph.update_figure(start_date, end_date)


if __name__ == '__main__':
    app.run_server(debug=True)