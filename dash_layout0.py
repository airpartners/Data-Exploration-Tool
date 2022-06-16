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

# Then, flesh out the app's contents using dash.html components (https://dash.plotly.com/dash-html-components)
# the app.layout is formatted like an html document. It consists of nested Divs containing P blocks for text,
# and Dash Core Component (dcc) elements for dropdown menus, date pickers, etc. Each element can accept several
# parameters that tell it how to behave; probably the most important is the `style=` parameter, which describes
# standard html formatting expressed as a dictionary of name:value pairs (names and values are both strings).
# The style dictionaries that are used for formatting various elements are defined above.
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    html.P("At "),
                    style = text_style
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options = [
                                {'label': 'Sensor 1', 'value': '0'},
                                {'label': 'Sensor 2', 'value': '1'},
                                {'label': 'Sensor 3', 'value': '2'},
                                {'label': 'Sensor 4', 'value': '3'},
                                {'label': 'Sensor 5', 'value': '4'},
                                {'label': 'Sensor 6', 'value': '5'},
                            ],
                            value = '0', # default value
                            id = "which-sensor" # javascript id, used in @app.callback to reference this element, below
                        ),
                    ],
                    style = dropdown_style
                ),
                html.Div(
                    html.P(", what were the pollution levels between"),
                    style = text_style
                ),

                html.Div(
                    [
                        dcc.DatePickerSingle(
                            display_format='MM/DD/Y',
                            date = date(2019, 12, 1), # default value
                            id = 'start-date',
                        ),
                    ],
                    style = date_picker_style
                ),
                html.Div(
                    html.P(" and "),
                    style = text_style
                ),
                html.Div(
                    [
                        dcc.DatePickerSingle(
                            date = date(2020, 1, 1), # default value
                            display_format='MM/DD/Y',
                            id = 'end-date',
                        ),
                    ],
                    style = date_picker_style
                ),
                html.Div(
                    html.P("when the wind was blowing"),
                    style = text_style
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options = [
                                {'label': 'North',     'value': 'N'},
                                {'label': 'Northeast', 'value': 'NE'},
                                {'label': 'East',      'value': 'E'},
                                {'label': 'Southeast', 'value': 'SE'},
                                {'label': 'South',     'value': 'S'},
                                {'label': 'Southwest', 'value': 'SW'},
                                {'label': 'West',      'value': 'W'},
                                {'label': 'Northwest', 'value': 'NW'},
                            ],
                            value = 'NE', id = "wind-direction"
                        ),
                    ],
                    style = dropdown_style
                ),
                html.Div(
                    html.P("?"),
                    style = text_style
                ),
            ]
        ),
        # placeholder for a graph to be created
        dcc.Graph(id='graph-to-update'), # this graph will be updated in the @app.callback: update_figure function below
    ]
)

filter_graph = FilterGraph()

@app.callback(
    Output('graph-to-update', 'figure'),
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