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
            "blowing in from a certain direction.",
            "The three graphs represent when the wind was blowing at different speeds. Generally, calm wind is associated with higher pollutant concentrations."
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
                        ", what was the concentration of",
                        self.pollutant_picker(multi = False, show_flights = False),
                        "associated with wind blowing from a specific direction, over the date range of ",
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
            df = df.rename(columns={
                "pm10.ML": "PM10 (μg/m^3)", 
                "pm25.ML": "PM2.5 (μg/m^3)",
                "pm1.ML": "PM1 (μg/m^3)",
                "co.ML": "CO (ppb)",
                "correctedNO": "NO (ppb)",
                "no2.ML": "NO2 (ppb)",
                "o3.ML": "O3 (ppb)",
                "temp_manifold": "Temperature (°C)",
                "rh_manifold": "Humidity (%)",
                "ws": "Wind Speed (m/s)",
                "adverse_flight_count": "Adverse Takeoffs/Landings",
                "count": "Total Takeoffs/Landings",
            })

            wind_speed_labels = ["Calm Wind", "Moderate Wind", "Strong Wind"]
            wind_direction_labels = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

            n_angles = len(wind_direction_labels)
            angles = [-1]
            angles.extend(range(int(360 / n_angles / 2), int(360 - 360 / n_angles / 2), int(360 / (n_angles - 1))))
            angles.append(361)

            df["ws_category"] = pd.cut(df["Wind Speed (m/s)"], bins = [0, 1.5, 7.9, 100], labels = wind_speed_labels)
            df["wd_category"] = pd.cut(df["wd"] % 360, bins = angles, labels = wind_direction_labels)
            # df_polar = df.groupby(["ws_category", "wd_category"]).mean()
            df_polar = df.groupby(["ws_category", "wd_category"]).agg(
                    # q05 = (pollutant, lambda df: df.quantile(0.05)),
                    q25 = (pollutant, lambda df: df.quantile(0.25)),
                    q50 = (pollutant, lambda df: df.quantile(0.50)),
                    q75 = (pollutant, lambda df: df.quantile(0.75)),
                    # q95 = (pollutant, lambda df: df.quantile(0.95)),
            )
            df_polar = df_polar.round(2)

            # quantiles = ["q05", "q25", "q50", "q75", "q95"][::-1]
            # colors = ["#FEF001", "#FFCE03", "#FD9A01", "#FD6104", "#F00505"][::-1]
            quantiles = ["q25", "q50", "q75"][::-1]
            colors = ["#FEF001", "#FD9A01", "#F00505"][::-1]


            # print("Filtering by pollutant: ", pollutant)

            limit = {
                'co.ML': [0,9000],
                'correctedNO': [0,71000],
                'no2.ML': [0,71000],
                'o3.ML': [0,93000],
                'pm1.ML': [0,20],
                'pm25.ML': [0,20],
                'pm10.ML': [0,67]
            }

            hover_trace_name = {
                "q25": "25th percentile",
                "q50": "median",
                "q75": "75th percentile"
            }

            fig = make_subplots(rows = 1, cols = 3, subplot_titles = wind_speed_labels, specs = [[{"type": "polar"}]*3])
            for i, label in enumerate(wind_speed_labels):
                df_subplot = df_polar.loc[label]
                for j, quantile in enumerate(quantiles):

                    # print(df_polar.head(2))
                    fig.add_trace(
                        go.Scatterpolar(
                            r = df_subplot[quantile],
                            theta = df_subplot.index,
                            marker_color = colors[j],
                            # size = df_subplot[pollutant],
                            # opacity = 0.4,
                            # color = df_subplot[pollutant],
                            # color_continuous_scale = [(0,"green"), (0.5,"yellow"), (0.75,"red"), (1,"purple")],
                            # range_color = limit[pollutant],
                            name = hover_trace_name[quantile],
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
            fig.update_traces(
                fill='toself',
                hovertemplate = '<br>Wind direction: %{theta}<br>Concentration: %{r}'

            )
            fig.update_layout(showlegend=False)

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
            fig.update_layout(margin = {'t': 0})

            return fig