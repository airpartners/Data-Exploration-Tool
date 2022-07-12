from asyncore import poll
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
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
                        "At ",
                        dcc.Dropdown(
                            options = [{'label': self.sensor_locations[name], 'value': i} for i, name in enumerate(sensor_names)],

                            # note: in order to set the default value, you have to set value = {the VALUE you want}.
                            # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
                            value = 0, # default value
                            id = self.get_id("which-sensor"), # javascript id, used in @app.callback to reference this element, below
                            clearable = False, # prevent users from deselecting all sensors
                            style = self.dropdown_style
                        ),
                        "in the date range of ",
                        dcc.DatePickerRange(
                            display_format = 'MM/DD/Y',
                            min_date_allowed = datetime.date(2019, 9, 8),
                            max_date_allowed = datetime.date(2021, 3, 5),
                            start_date = datetime.date(2019, 12, 1), # default value
                            end_date = datetime.date(2019, 12, 31), # default value
                            id = self.get_id('date-picker-range'),
                        ),
                        ", what was the value of ",
                        dcc.Dropdown(
                            options = [{'label': var_name, 'value': var} for var, var_name in
                                list(self.particles_vars.items()) + list(self.gas_vars.items()) + list(self.flight_vars.items())],
                            # options = [{'label': name, 'value': i} for i, name in enumerate(sensor_names)],
                            value='pm25.ML',
                            multi = True,
                            id = self.get_id('pollutant-dropdown'),
                            style = self.dropdown_style_2
                        ),
                        "?",
                        daq.BooleanSwitch(
                            id = self.get_id('normalize-height'),
                            on = True,
                            style = {'display': 'block'},
                            label = "Ignore units",
                            labelPosition = "top"
                        ),
                    ],
                    style = self.text_style
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                # html.Div(
                    # chilfwidren = [
                dcc.Graph(id = self.get_id('graph-to-update')),
                    # ],
                    # style = {'display': 'flex'}
                # ),
            ]

    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('graph-to-update'), 'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('date-picker-range'), 'start_date'),
            Input(self.get_id('date-picker-range'), 'end_date'),
            Input(self.get_id('pollutant-dropdown'), 'value'),
            Input(self.get_id('normalize-height'), 'on'),
        )
        def update_figure(which_sensor, start_date, end_date, pollutant, normalize_height):
            print(f"Graph with id {self.id_num} being called back!")

            if isinstance(pollutant, str):
                pollutant = [pollutant]

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # filter by timestamp and wind direction
            df = self.filter_by_date(df, start_date, end_date)
            # df = self.filter_by_wind_direction(df, wind_direction)

            if normalize_height:
                df = self.normalize_height(df)

            # create the figure. It consists of a Figure frame and three lines created with go.Scatter()

            fig = px.line(df, df.index, y = pollutant)

            # fig = go.Figure([
            #     go.Line(
            #         name = 'Average',
            #         x = df.index,
            #         y = df,
            #         fill = pollutant,
            #         # mode = 'lines',
            #         # line = dict(color = 'rgb(31, 119, 180)'),
            #     ),
                # go.Scatter(
                #     name = '95th Percentile',
                #     x = df.index,
                #     y = df["pm25.ML"],
                #     mode = 'lines',
                #     marker = dict(color = "#444"),
                #     line = dict(width = 0),
                #     showlegend = False
                # ),
                # go.Scatter(
                #     name = '5th Percentile',
                #     x = df.index,
                #     y = df["pm25.ML"],
                #     marker = dict(color = "#444"),
                #     line = dict(width = 0),
                #     mode = 'lines',
                #     fillcolor = 'rgba(68, 68, 68, 0.3)',
                #     fill = 'tonexty',
                #     showlegend = False
                # )
            # ])

            if len(pollutant) == 1:
                y_label = self.all_vars[pollutant[0]]
            else:
                y_label = 'Pollutant (refer to legend)'

            fig.update_layout(
                xaxis_title = 'Timestamp',
                yaxis_title = y_label,
                # title='PM2.5',
                hovermode = "x", # where the magic happens
                margin = {'t': 0}, # removes the awkward whitespace where the title used to be
            )

            if normalize_height:
                fig.layout.yaxis.tickformat = ',.0%'

            for idx, poll in enumerate(pollutant):
                fig.data[idx].name = self.all_vars[poll]
                fig.data[idx].hovertemplate = self.all_vars[poll]

            return fig