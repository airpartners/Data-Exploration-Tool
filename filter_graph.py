from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from time import strftime, strptime, mktime

import pandas as pd

class FilterGraph():
    major_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn46-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn49-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn62-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn67-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn72-final-w-ML-PM.csv",
    ]

    minor_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/temp/sn45-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/temp/sn46-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/temp/sn49-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/temp/sn62-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/temp/sn67-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/temp/sn72-final-w-ML-PM.csv",
    ]

    wind_dict = {'N': [0, 22.5],
                 'NE': [22.5, 67.5],
                 'E': [67.5, 112.5],
                 'SE': [112.5, 157.5],
                 'S': [157.5, 202.5],
                 'SW': [202.5, 247.5],
                 'W': [247.5, 292.5],
                 'NW': [292.5, 337.5]}

    def __init__(self):
        self.sensor_data = []
        for file_id, minor_file in enumerate(FilterGraph.minor_csv_paths):
            # append the next sensor's worth of data to the list
            self.sensor_data.append(self.prepare_data(FilterGraph.major_csv_paths[file_id], minor_file))
            pass

    def prepare_data(self, major_file, minor_file):
        minor_file_found = True
        try:
            df_downsampled = pd.read_csv(minor_file, skiprows = [0, 1])
        except(FileNotFoundError):
            minor_file_found = False

        if minor_file_found:
            cols = pd.MultiIndex.from_tuples([("row_id", ''), ("timestamp_local", ''), ("pm25", "percentile5"), ("pm25", "hourly_mean"), ("pm25", "percentile95"),
                                            ("wind_direction_cardinal", '')])
            df_downsampled.columns = cols
            df_downsampled["timestamp_local"] = pd.to_datetime(df_downsampled["timestamp_local"], format = "%Y-%m-%d %H:%M:%S")
            return df_downsampled

        df_major = pd.read_csv(major_file)
        df_minor = df_major.copy()[["timestamp_local", "pm25", "wind_dir"]]
        df_minor["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        df_minor["date"] = df_minor["timestamp_local"].dt.date

        def discrete_wind_direction(degrees, wind_dict = FilterGraph.wind_dict):
            for direction, bounds in wind_dict.items():
                if degrees >= bounds[0] and degrees < bounds[1]:
                    return direction
                # else: # the direction is between 337.5 and 360 degrees
            return "N"

        df_minor["wind_direction_cardinal"] = df_minor["wind_dir"].apply(discrete_wind_direction)

        # continuous aggregation functions (e.g. for PM2.5)
        def percentile5(df):
            return df.quantile(0.05)
        def percentile95(df):
            return df.quantile(0.95)
        def hourly_mean(df):
            return df.mean()

        # discrete aggregation for wind direction
        def hourly_mode(df):
            return df.mode()

        resample_frequency = "1H"
        df_downsampled = df_minor.copy()
        df_downsampled = df_downsampled.set_index("timestamp_local")
        df_downsampled = df_downsampled.resample(resample_frequency).agg(
            {"pm25": [percentile5, "mean", percentile95],
            "wind_direction_cardinal": hourly_mode}
        ).reset_index()

        df_downsampled.to_csv(minor_file)

        return df_downsampled

    def update_figure(self, which_sensor, start_date, end_date, wind_direction):
        print("HELLOOOOO WORLD")
        print("WIND DIRECTION:", wind_direction)

        df_downsampled = self.sensor_data[which_sensor]

        df_filtered = df_downsampled[
            (df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]

        if wind_direction is not None:
            df_filtered = df_filtered[
                df_filtered["wind_direction_cardinal"] == wind_direction
            ]

        fig = go.Figure([
            go.Scatter(
                name='Average',
                x=df_filtered["timestamp_local"],
                y=df_filtered["pm25"]["hourly_mean"],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name='95th Percentile',
                x=df_filtered["timestamp_local"],
                y=df_filtered["pm25"]["percentile95"],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='5th PErcentile',
                x=df_filtered["timestamp_local"],
                y=df_filtered["pm25"]["percentile5"],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])
        fig.update_layout(
            yaxis_title='PM2.5',
            # title='PM2.5',
            hovermode="x",
            margin={'t': 0},
        )

        return fig