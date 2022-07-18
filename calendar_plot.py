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
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
        ]


    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At ",
                        self.sensor_picker(),
                        ", what was the level of ",
                        self.pollutant_picker(multi = False),
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
            Input(self.get_id('pollutant-dropdown'), 'value')
            )

        def update_figure(which_sensor, pollutant):

            if isinstance(pollutant, str):
                pollutant = [pollutant]

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # calculate daily average                
            df=df.resample('D').mean()

            # df.index = pd.date_range('01/01/2018',
            #                         periods=8,
            #                         freq='W')

            # print(df.index)
            # pollution_level = np.array(df[pollutant])
            # pollution_level = list(np.average(pollution_level.reshape(-1, 24), axis=1))
            

            start_date = df.index[0]
            end_date = df.index[-1]
            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
                "value": df[pollutant].squeeze()
            })
            print(dummy_df)

            # creating the plot
            fig = calplot(dummy_df,
                    x='ds',
                    y='value',
                    # data=df[pollutant]
                    colorscale=[(0,"white"),(0.000001,"green"),(0.5,"yellow"),(0.75,"red"),(1,"purple")],
                    # colorbar=True
            )

            return fig

