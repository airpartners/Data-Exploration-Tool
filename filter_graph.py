from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from time import strftime, strptime, mktime
from csv_file_paths import raw_csv_paths, processed_csv_paths

import pandas as pd

class FilterGraph():

    wind_dict = {'N': [0, 22.5],
                 'NE': [22.5, 67.5],
                 'E': [67.5, 112.5],
                 'SE': [112.5, 157.5],
                 'S': [157.5, 202.5],
                 'SW': [202.5, 247.5],
                 'W': [247.5, 292.5],
                 'NW': [292.5, 337.5]}

    def __init__(self):
        self.list_of_sensor_dataframes = []
        for file_id, processed_file in enumerate(processed_csv_paths):
            # append the next sensor's worth of data to the list
            self.list_of_sensor_dataframes.append(self.prepare_data(raw_csv_paths[file_id], processed_file))
            pass

    def prepare_data(self, raw_file, processed_file):
        processed_file_exists = True
        try:
            df_processed = pd.read_csv(processed_file, skiprows = [0, 1])
        except(FileNotFoundError):
            processed_file_exists = False

        if processed_file_exists:
            cols = pd.MultiIndex.from_tuples([("row_id", ''), ("timestamp_local", ''),
                                              ("pm25", "percentile5"), ("pm25", "hourly_mean"), ("pm25", "percentile95"),
                                              ("wind_direction_cardinal", '')])
            df_processed.columns = cols
            df_processed["timestamp_local"] = pd.to_datetime(df_processed["timestamp_local"], format = "%Y-%m-%d %H:%M:%S")
            return df_processed

        df_raw = pd.read_csv(raw_file)
        df_processed = df_raw.copy()[["timestamp_local", "pm25", "wind_dir"]]
        df_processed["timestamp_local"] = pd.to_datetime(df_raw["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        df_processed["date"] = df_processed["timestamp_local"].dt.date

        def discrete_wind_direction(degrees, wind_dict = FilterGraph.wind_dict):
            for direction, bounds in wind_dict.items():
                if degrees >= bounds[0] and degrees < bounds[1]:
                    return direction
                # else: # the direction is between 337.5 and 360 degrees
            return "N"

        df_processed["wind_direction_cardinal"] = df_processed["wind_dir"].apply(discrete_wind_direction)

        # continuous aggregation functions (e.g. for PM2.5)
        def percentile5(df):
            return df.quantile(0.05)
        def percentile95(df):
            return df.quantile(0.95)
        # def hourly_mean(df):
        #     return df.mean()

        # discrete aggregation for wind direction
        def hourly_mode(df):
            return df.mode()

        resample_frequency = "1H"
        df_processed = df_processed.set_index("timestamp_local")
        # the following line takes the bulk of the time to run. It is very slow:
        df_processed = df_processed.resample(resample_frequency).agg(
            {"pm25": [percentile5, "mean", percentile95],
            "wind_direction_cardinal": hourly_mode}
        ).reset_index()

        # store the processed and downsampled dataframe to a csv, to be read next time
        df_processed.to_csv(processed_file)

        return df_processed

    def update_figure(self, which_sensor, start_date, end_date, wind_direction):

        df_processed = self.list_of_sensor_dataframes[which_sensor]

        df_filtered = df_processed[
            (df_processed["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (df_processed["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]

        if wind_direction is not None:
            df_filtered = df_filtered[
                df_filtered["wind_direction_cardinal"] == wind_direction
            ]
        # else: if wind_direction is None: pass

        fig = go.Figure([
            go.Scatter(
                name = 'Average',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["hourly_mean"],
                mode = 'lines',
                line = dict(color = 'rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name = '95th Percentile',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["percentile95"],
                mode = 'lines',
                marker = dict(color = "#444"),
                line = dict(width = 0),
                showlegend = False
            ),
            go.Scatter(
                name = '5th Percentile',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["percentile5"],
                marker = dict(color = "#444"),
                line = dict(width = 0),
                mode = 'lines',
                fillcolor = 'rgba(68, 68, 68, 0.3)',
                fill = 'tonexty',
                showlegend = False
            )
        ])

        fig.update_layout(
            yaxis_title='PM2.5',
            # title='PM2.5',
            hovermode="x",
            margin={'t': 0}, # removes the awkward whitespace where the title used to be
        )

        return fig