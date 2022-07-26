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
            html.P([html.B("Calendar Plot:"), " Shows the pollution levels at a certain sensor over the entire data collection period. ",
            "Select a sensor location and a pollutant to show. ",
            "Each horizontal strip represents 365 days of data. Each square represents the average concentration levels for one day. ",
            "Each column represents one week (the top row is all Mondays, etc.)"]
            )
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
                        self.pollutant_picker(multi = False, show_flights = True),
                        " over the entire date range for that sensor?",
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

            df = df.rename(columns={
                "pm10.ML": "PM10 (μg/m^3)", 
                "pm25.ML": "PM2.5 (μg/m^3)",
                "pm1.ML": "PM1 (μg/m^3)",
                "co,ML": "CO (ppb)",
                "correctedNO": "NO (ppb)",
                "no2.ML": "NO2 (ppb)",
                "o3.ML": "O3 (ppb)",
                "temp_manifold": "Temperature (°C)",
                "rh_manifold": "Humidity (%)",
                "ws": "Wind Speed (m/s)",
                "adverse_flight_count": "Adverse Takeoffs/Landings",
                "count": "Total Takeoffs/Landings",
            })


            start_date = df.index[0]
            end_date = df.index[-1]
            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
                "value": df[pollutant].squeeze()
            })

            # creating the plot
            fig = calplot(dummy_df,
                    x='ds',
                    y='value',
                    # data=df[pollutant]
                    years_title=True,
                    colorscale=[(0,"white"),(0.000000000001,"green"),(0.5,"yellow"),(0.8,"red"),(1,"purple")],
                    showscale=True
            )

            return fig

