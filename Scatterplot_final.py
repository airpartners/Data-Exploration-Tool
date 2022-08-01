import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graph_frame import GraphFrame

class Scatter(GraphFrame):
    def get_explanation(self):
        return [
            html.P([html.B("Correlation Plot:"), " Shows relationships between different variables at the same time. ",
            "Select a sensor location and a date range between September 2019 and April 2020. You can choose what to display on the x-axis and y-axis respectively, and a correlation line is going to display in the graph to show the correlation between your y-axis variable and your x-axis variable. ",
        ]),
            html.P(["For example, if you choose “temperature” on the x-axis and “PM2.5” on the axis, the coefficient m of the displayed equation “PM2.5 = m * temperature + c” indicates how much PM2.5 concentration is correlated to the temperature. ",
            "The R squared value shows how scattered the data points are, and the range goes from 0 to1. A higher R squared value (generally equals or exceeds 0.4) means a more convincing x-axis variable coefficient (m)."
        ])
        ]

    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At",
                        self.sensor_picker(),
                        ", what was the correlation between",
                        self.correlation_xvar(),
                        " and",
                        # self.correlation_yvar(),
                        self.pollutant_picker(my_id = 'pollutant-dropdown', multi = True, show_flights = True),
                        " for dates in the range of ",
                        self.date_picker('date-picker-range'),
                        "?"
                    ],
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id=self.get_id('scatterplot'))
            ]

    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('scatterplot'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('date-picker-range'), 'start_date'),
            Input(self.get_id('date-picker-range'), 'end_date'),
            Input(self.get_id('x-axis'), 'value'),
            Input(self.get_id('pollutant-dropdown'), 'value'),
            )

        def update_figure(which_sensor, start_date, end_date, xaxis_column_name, yaxis_column_name):
            df = self.data_importer.get_data_by_sensor(which_sensor)
            df = self.filter_by_date(df, start_date, end_date)

            df = df.round(2)
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

            fig = px.scatter(df, x=xaxis_column_name, y=yaxis_column_name,
                    trendline="ols",
                    hover_name=df.index,
                    # log_x=True, size_max=15
                )


            # fig.update_xaxes(title=xaxis_column_name,
            #                 type='linear' if xaxis_type == 'Linear' else 'log')

            # fig.update_yaxes(title=str(yaxis_column_name),
            #                 type='linear' if yaxis_type == 'Linear' else 'log')


            fig.update_layout(
                transition_duration = 500,
                margin = {'t': 0}, # removes the awkward whitespace where the title used to be
            )

            # # set title and caption
            # string1 = "Scatter plot"
            # myTitle = '<b>'+string1+'</b>'

            # string2 = 'This is the caption'
            # myCaption = string2


            # fig.update_layout(title=go.layout.Title(
            #     text=myTitle, font=dict(
            #     family="Courier New, monospace",
            #     size=22,
            #     color="#000000"
            #     ))
            # )

            return fig
