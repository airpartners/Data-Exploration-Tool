from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from matplotlib.pyplot import text
from datetime import date

from filter_graph import FilterGraph # import from supporting file

# define HTML styles for text and dropdown menus. Use this to change font size, alignment, etc.
text_style = {
    "display": "inline-block", # if you take this out, all successive elements will be displayed on separate lines
    "transform": "translateY(0%)", # vertical alignment
    "position": "relative",
    "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
    "font-size" : "30px",
    "font-family": "Arial",
    "line-height": "0%", # helps reduce the line spacing
}
dropdown_style = {
    "display": "inline-block",
    "width": "200px",
    "height": "30px",
    "margin-left": "10px",
    "font-size": "20px",
    "font-family": "Arial",
    "line-height": "0%", # helps reduce the line spacing
}

date_picker_style = {
    "display": "inline-block",
    # "width": "200px",
    "height": "40px",
    "margin-left": "10px",
    # "font-family": "Arial",
    "line-height": "0%", # helps reduce the line spacing
}

app = Dash(__name__) # initialize the app

# then, flesh out the app's contents using dash.html components (https://dash.plotly.com/dash-html-components)
app.layout = html.Div([
    html.Div([
        html.Div(html.P("At "), style = text_style),
        html.Div([
            dcc.Dropdown(options = [
                {'label': 'Sensor 1', 'value': '0'},
                {'label': 'Sensor 2', 'value': '1'},
                {'label': 'Sensor 3', 'value': '2'},
                {'label': 'Sensor 4', 'value': '3'},
                {'label': 'Sensor 5', 'value': '4'},
                {'label': 'Sensor 6', 'value': '5'},
                ], value = '0', id = "which-sensor"),
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
        ], value = 'NE', id = "wind-direction"),
        ], style = dropdown_style),
        html.Div(html.P("?"), style = text_style),
    ]),
    dcc.Graph(id='graph-with-slider'),
])

filter_graph = FilterGraph()

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('which-sensor', 'value'),
    Input('start-date', 'date'),
    Input('end-date', 'date'),
    Input('wind-direction', 'value'),
)
def update_figure(which_sensor, start_date, end_date, wind_direction):
    if which_sensor is None:
        which_sensor = 0
    return filter_graph.update_figure(int(which_sensor), start_date, end_date, wind_direction)


if __name__ == '__main__':
    app.run_server(debug=True)