from dash import html, dcc, Input, Output
from plotly_calplot import calplot # $pip install plotly-calplot
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from graph_frame import GraphFrame


class CalendarPlot(GraphFrame):
    def get_explanation(self):
        return [
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
        ]


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
            Input(self.get_id('date-picker-range'), 'start_date'),
            Input(self.get_id('date-picker-range'), 'end_date'),
            Input(self.get_id('pollutant-dropdown'), 'value')
            )

        def update_figure(which_sensor, start_date, end_date, pollutant):

            if isinstance(pollutant, str):
                pollutant = [pollutant]

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # filter by timestamp and wind direction
            df = self.filter_by_date(df, start_date, end_date)


            # df.index = pd.date_range('01/01/2018',
            #                         periods=8,
            #                         freq='W')

            # print(df.index)
            # pollution_level = np.array(df[pollutant])
            # pollution_level = list(np.average(pollution_level.reshape(-1, 24), axis=1))

            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
                "value": np.random.randint(
                    low=0, high=30,
                    size=(pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1,),
            })

            # creating the plot
            fig = calplot(dummy_df,
                    x='ds',
                    y='value',
                    # data=df[pollutant]
                    # cmap='YlGn',
                    # colorbar=True
            )

            return fig

