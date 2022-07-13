from dash import html, dcc, Input, Output
from plotly_calplot import calplot # $pip install plotly-calplot
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from graph_frame import GraphFrame


class CalendarPlot(GraphFrame):
    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At ",
                        self.sensor_picker(),
                        "in the date range of ",
                        self.date_picker(),
                        ", what was the level of ",
                        self.pollutant_picker(),
                        "?",
                    ],
                    style = self.text_style
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                # html.Div(
                    # chilfwidren = [
                dcc.Graph(id = self.get_id('calendar-plot')),
                    # ],
                    # style = {'display': 'flex'}
                # ),
            ]


    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('calendar-plot'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            Input(self.get_id('pollutant-dropdown'), 'value')
            )

        def update_figure(which_sensor, start_date, end_date, pollutant):

            if isinstance(pollutant, str):
                pollutant = [pollutant]

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # filter by timestamp and wind direction
            df = self.filter_by_date(df, start_date, end_date)




            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
            })

            # creating the plot
            fig = calplot(
                    x=dummy_df["ds"],
                    y=df[pollutant]
            )

            return fig

