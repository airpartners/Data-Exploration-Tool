from asyncore import poll
import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from graph_frame import GraphFrame


class Polar(GraphFrame):

    def get_explanation(self):
        return [
            html.P([html.B("Polar Plot:"), " Shows the pollution levels at a certain location based on wind speed and direction. ",
            "Select a sensor location, select a date range between September 2019 and April 2020, and select one pollutant at a time. ",
            ]),
            html.P([
            "The directions shown on the polar plot represent the direction the wind was blowing ", html.B("from"), ". ",
            "This type of graph can help with locating pollution sources, particularly if a large number of pollutants are ",
            "blowing in from a certain direction."
            ]),
        ]


    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At",
                        self.sensor_picker(),
                        ", what were the concentrations of ",
                        self.pollutant_picker(multi = False, show_flights = False),
                        " on the date range of ",
                        self.date_picker(),
                        "?"
                    ],
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id=self.get_id('polar'))
            ]

    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('polar'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input( self.get_id('date-picker-range'), 'start_date'),
            Input( self.get_id('date-picker-range'), 'end_date'),
            Input(self.get_id('pollutant-dropdown'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date, pollutant):
            df = self.data_importer.get_data_by_sensor(which_sensor)
            df = self.filter_by_date(df, start_date, end_date)
            df = df.round(2)

            wind_speed_labels = ["Calm", "Moderate", "Strong"]
            wind_direction_labels = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

            n_angles = len(wind_direction_labels)
            angles = [-1]
            angles.extend(range(int(360 / n_angles / 2), int(360 - 360 / n_angles / 2), int(360 / (n_angles - 1))))
            angles.append(361)

            df["ws_category"] = pd.cut(df["ws"], bins = [0, 1.5, 7.9, 100], labels = wind_speed_labels)
            df["wd_category"] = pd.cut(df["wd"] % 360, bins = angles, labels = wind_direction_labels)
            df_polar = df.groupby(["ws_category", "wd_category"]).mean()

            # print("Filtering by pollutant: ", pollutant)

            limit={
                'co.ML': [0,9000],
                'correctedNO': [0,71000],
                'no2.ML': [0,71000],
                'o3.ML': [0,93000],
                'pm1.ML': [0,20],
                'pm25.ML': [0,20],
                'pm10.ML': [0,67]
            }

            fig = make_subplots(rows = 1, cols = 3, subplot_titles = wind_speed_labels, specs = [[{"type": "polar"}]*3])
            for i, label in enumerate(wind_speed_labels):
                df_subplot = df_polar.loc[label]
                # print(df_polar.head(2))
                fig.add_trace(
                    go.Scatterpolar(
                        r = df_subplot[pollutant],
                        theta = df_subplot.index,
                        # size = df_subplot[pollutant],
                        # opacity = 0.4,
                        # color = df_subplot[pollutant],
                        # color_continuous_scale = [(0,"green"), (0.5,"yellow"), (0.75,"red"), (1,"purple")],
                        # range_color = limit[pollutant],
                        # hover_name = df.index,
                        # template = "plotly_dark",
                    ),
                    row = 1,
                    col = i + 1,
                )

            fig.update_polars(
                angularaxis = {
                    "direction": "clockwise",
                }
            )
            fig.update_traces(fill='toself')

            # add another column which is hour converted to degrees
            # fig.update_layout(
            #     polar={
            #         "angularaxis": {
            #             "tickmode": "array",
            #             "tickvals": list(range(0, 360, 360 // 8)),
            #             "ticktext": ['N','NE','E','SE','S','SW','W','NW'],
            #         }
            #     }
            # )

            # fig.layout.annotations =[dict(showarrow=False,
            #                     text='Wind Speed (m/s)',
            #                     xanchor='left',
            #                     yanchor='bottom',
            #                     font=dict(size=12 ))]

            # margins = 200
            # fig.update_layout(margin = {'t': 0, 'l': margins, 'r': margins})

            return fig