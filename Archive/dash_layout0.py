from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime

from filter_graph import FilterGraph # import from supporting file (contained in this repo)

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
    # "width": "200px", # not used or doesn't work
    "height": "40px",
    "margin-left": "10px",
    # "font-family": "Arial", # not used or doesn't work
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
                            # note: in order to set the default value, you have to set value = {the VALUE you want}.
                            # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
                            value = '0', # default value
                            id = "which-sensor", # javascript id, used in @app.callback to reference this element, below
                            clearable = False # prevent users from deselecting all sensors
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
                            date = datetime.date(2019, 12, 1), # default value
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
                            date = datetime.date(2020, 1, 1), # default value
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
        # Placeholder for a graph to be created.
        # This graph will be updated in the @app.callback: update_figure function below
        dcc.Graph(id='graph-to-update'),
    ]
)

# Create an instance of the FilterGraph class from filter_graph.py (contained in this repo)
# FilterGraph loads all of the data and contains the main plotting function for slicing the data according to the filters
# and displaying it in the dcc.Graph 'graph-to-update' initialized above.
filter_graph = FilterGraph()

# the @app.callback decorator calls update_figure() whenever one of the Input elements changes.
# The first argument of the Input is the id of the dcc element being listened to (for example, the id 'which-sensor'
# is associated with the dcc.Dropdown element for choosing the sensor to display).
# The second argument is the parameter of the dcc element to look at. For Dropdowns, the parameter you want is 'value';
# for DatePickers, you want to get the 'date'.
# The results of the four Inputs become the four arguments to update_figure(). These are then passed to filter_graph.update_figure().
# The Output sets the dcc.Graph element's 'figure' parameter to the output of the update_figure() function.
# update_figure() returns a plotly.graph_objs.Figure object.
@app.callback(
    Output('graph-to-update', 'figure'),
    Input('which-sensor', 'value'),
    Input('start-date', 'date'),
    Input('end-date', 'date'),
    Input('wind-direction', 'value'),
)
def update_figure(which_sensor, start_date, end_date, wind_direction):
    # call the corresponding function on the FilterGraph object containing all the data and the graphing funcionality
    return filter_graph.update_figure(int(which_sensor), start_date, end_date, wind_direction)

# Run the server (by default, it runs on the local machine at the IP address 127.0.0.1:8050.
# You can view the server running by typing that IP address into your browser or going to http://127.0.0.1:8050/.
if __name__ == '__main__':
    app.run_server(debug=True)