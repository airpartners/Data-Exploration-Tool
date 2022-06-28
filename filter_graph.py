import plotly.graph_objs as go
import pandas as pd
from data_importer import DataImporter

class FilterGraph():

    def __init__(self, data_importer = None):
        if data_importer is not None:
            self.data_importer = data_importer
        else:
            self.data_importer = DataImporter() # initialize the data

    def filter_by_date(self, df, start_date, end_date):
        if start_date and end_date:
            return \
                df[
                    (df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                    (df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
                ]
        # else:
        return df

    def filter_by_wind_direction(self, df, wind_direction):
        if wind_direction is not None:
            return df[ df["wind_direction_cardinal", "my_mode"] == wind_direction ]
        # else:
        return df

    def update_figure(self, which_sensor, start_date, end_date, wind_direction):

        # select which sensor data to draw from
        df = self.data_importer.get_data_by_sensor(which_sensor)

        # filter by timestamp and wind direction
        df = self.filter_by_date(df, start_date, end_date)
        df = self.filter_by_wind_direction(df, wind_direction)

        # create the figure. It consists of a Figure frame and three lines created with go.Scatter()
        fig = go.Figure([
            go.Scatter(
                name = 'Average',
                x = df["timestamp_local"],
                y = df["pm25"]["mean"],
                mode = 'lines',
                line = dict(color = 'rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name = '95th Percentile',
                x = df["timestamp_local"],
                y = df["pm25"]["percentile95"],
                mode = 'lines',
                marker = dict(color = "#444"),
                line = dict(width = 0),
                showlegend = False
            ),
            go.Scatter(
                name = '5th Percentile',
                x = df["timestamp_local"],
                y = df["pm25"]["percentile5"],
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