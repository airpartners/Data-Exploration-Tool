from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime

from torch import CharStorage

from filter_graph import FilterGraph # import from supporting file (contained in this repo)

class GraphFrame():

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

    def __init__(self, id_num, chart_type = 0) -> None:
        self.id_num = id_num
        self.graph_frame = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            html.P("At "),
                            style = self.text_style
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
                                    id = self.get_id("which-sensor"), # javascript id, used in @app.callback to reference this element, below
                                    clearable = False # prevent users from deselecting all sensors
                                ),
                            ],
                            style = self.dropdown_style
                        ),
                        html.Div(
                            html.P(", what were the pollution levels between"),
                            style = self.text_style
                        ),

                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    display_format='MM/DD/Y',
                                    date = datetime.date(2019, 12, 1), # default value
                                    id = self.get_id('start-date'),
                                ),
                            ],
                            style = self.date_picker_style
                        ),
                        html.Div(
                            html.P(" and "),
                            style = self.text_style
                        ),
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    date = datetime.date(2020, 1, 1), # default value
                                    display_format='MM/DD/Y',
                                    id = self.get_id('end-date'),
                                ),
                            ],
                            style = self.date_picker_style
                        ),
                        html.Div(
                            html.P("when the wind was blowing"),
                            style = self.text_style
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
                                    value = 'NE', id = self.get_id("wind-direction")
                                ),
                            ],
                            style = self.dropdown_style
                        ),
                        html.Div(
                            html.P("?"),
                            style = self.text_style
                        ),
                    ]
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id = self.get_id('graph-to-update')),
            ]
        )

    def get_id(self, id_str):
        return id_str + "-" + str(self.id_num)

    def add_graph_callback(self, app):
        self.filter_graph = FilterGraph()

        @app.callback(
            Output(self.get_id('graph-to-update'), 'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            Input(self.get_id('wind-direction'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date, wind_direction):
            print(f"Graph with id {self.id_num} being called back!")
            return self.filter_graph.update_figure(int(which_sensor), start_date, end_date, wind_direction)

class Page():
    def __init__(self, app, chart_types = [0, 0]) -> None:
        self.app = app
        self.chart_types = chart_types

        self.graphs = []
        for id_num, chart_type in enumerate(self.chart_types):
            graph = GraphFrame(id_num, chart_type)
            graph.add_graph_callback(self.app)
            self.graphs.append(graph.graph_frame)

        self.next_id_num = id_num + 1 # prepare for the next graph to be added

        self.button = html.Button('+', id = 'submit-val', n_clicks = 0)
        self.add_button_callback()

        self.layout = html.Div(self.graphs + [self.button], id = 'main')

    def add_button_callback(self):
        @self.app.callback(
            Output('main', 'children'),
            Input('submit-val', 'n_clicks'),
        )
        def add_graph(n_clicks):
            if n_clicks == 0:
                return self.graphs + [self.button]

            print("YOU HAVE CLICKED THE BUTTON!!! CONGRATULATIONS!")
            print("next_id_num:", self.next_id_num)
            self.chart_types.append(0)

            graph = GraphFrame(self.next_id_num, 0)
            self.next_id_num += 1
            graph.add_graph_callback(self.app)
            self.graphs.append(graph.graph_frame)

            return self.graphs + [self.button]

    def get_layout(self):
        return self.layout

if __name__ == '__main__':
    app = Dash(__name__) # initialize the app

    p = Page(app, chart_types = [0, 0])
    app.layout = html.Div(p.get_layout())

    app.run_server(debug=True)