from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import datetime
from filter_graph import FilterGraph # import from supporting file (contained in this repo)

from graph_frame import GraphFrame

class TimeSeries(GraphFrame):
    def get_html(self):
        sensor_names = self.data_importer.get_all_sensor_names()
        # children = ...
        return \
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
                                    options = [{'label': name, 'value': i} for i, name in enumerate(sensor_names)],

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
                        # html.Div(
                        #     html.P("when the wind was blowing"),
                        #     style = self.text_style
                        # ),
                        # html.Div(
                        #     [
                        #         dcc.Dropdown(
                        #             options = [
                        #                 {'label': 'North',     'value': 'N'},
                        #                 {'label': 'Northeast', 'value': 'NE'},
                        #                 {'label': 'East',      'value': 'E'},
                        #                 {'label': 'Southeast', 'value': 'SE'},
                        #                 {'label': 'South',     'value': 'S'},
                        #                 {'label': 'Southwest', 'value': 'SW'},
                        #                 {'label': 'West',      'value': 'W'},
                        #                 {'label': 'Northwest', 'value': 'NW'},
                        #             ],
                        #             value = 'NE', id = self.get_id("wind-direction")
                        #         ),
                        #     ],
                        #     style = self.dropdown_style
                        # ),
                        html.Div(
                            html.P("?"),
                        ),
                    ]
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id = self.get_id('graph-to-update')),

                # html.Button('Add New Graph', id = self.get_id('add-new-graph'), n_clicks = 0),
            ]

    def add_graph_callback(self):
        self.graph_obj = self.TimeSeriesGraph(self.data_importer)

        @self.app.callback(
            Output(self.get_id('graph-to-update'), 'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            # Input(self.get_id('wind-direction'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date):# , wind_direction):
            print(f"Graph with id {self.id_num} being called back!")
            return self.graph_obj.update_figure(int(which_sensor), start_date, end_date)# , wind_direction)

    class TimeSeriesGraph(FilterGraph):
        def update_figure(self, which_sensor, start_date, end_date):#, wind_direction):

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # filter by timestamp and wind direction
            df = self.filter_by_date(df, start_date, end_date)
            # df = self.filter_by_wind_direction(df, wind_direction)

            # create the figure. It consists of a Figure frame and three lines created with go.Scatter()
            fig = go.Figure([
                go.Scatter(
                    name = 'Average',
                    x = df.index,
                    y = df["pm25.ML"],
                    mode = 'lines',
                    line = dict(color = 'rgb(31, 119, 180)'),
                ),
                go.Scatter(
                    name = '95th Percentile',
                    x = df.index,
                    y = df["pm25.ML"],
                    mode = 'lines',
                    marker = dict(color = "#444"),
                    line = dict(width = 0),
                    showlegend = False
                ),
                go.Scatter(
                    name = '5th Percentile',
                    x = df.index,
                    y = df["pm25.ML"],
                    marker = dict(color = "#444"),
                    line = dict(width = 0),
                    mode = 'lines',
                    fillcolor = 'rgba(68, 68, 68, 0.3)',
                    fill = 'tonexty',
                    showlegend = False
                )
            ])

            fig.update_layout(
                yaxis_title = 'PM2.5',
                # title='PM2.5',
                hovermode = "x", # where the magic happens
                margin = {'t': 0}, # removes the awkward whitespace where the title used to be
            )

            return fig