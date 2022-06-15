from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from time import strftime, strptime, mktime

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
        minor_csv_path = "C:/dev/Air Partners/Data Analysis/data/temp/sn45-final-w-ML-PM.csv"
        minor_file_found = True
        try:
            self.df_downsampled = pd.read_csv(minor_csv_path, skiprows = [0, 1])
            # print(self.df_downsampled.head(5))
        except(FileNotFoundError):
            minor_file_found = False

        if minor_file_found:
            cols = pd.MultiIndex.from_tuples([("row_id", ''), ("timestamp_local", ''), ("pm25", "percentile5"), ("pm25", "hourly_mean"), ("pm25", "percentile95"),
                                              ("wind_dir", "percentile5"), ("wind_dir", "hourly_mean"), ("wind_dir", "percentile95"), ])
            # self.df_downsampled.set_index(cols)
            self.df_downsampled.columns = cols
            print(self.df_downsampled.head(5))
            self.df_downsampled["timestamp_local"] = pd.to_datetime(self.df_downsampled["timestamp_local"], format = "%Y-%m-%d %H:%M:%S")
            return

        major_csv_path = "C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv"
        self.df_major = pd.read_csv(major_csv_path)
        self.df_minor = self.df_major.copy()[["timestamp_local", "pm25", "wind_dir"]]
        self.df_minor["timestamp_local"] = pd.to_datetime(self.df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        self.df_minor["date"] = self.df_minor["timestamp_local"].dt.date

        def percentile5(df):
            return df.quantile(0.05)
        def percentile95(df):
            return df.quantile(0.95)
        def hourly_mean(df):
            return df.mean()

        resample_frequency = "1H"
        self.df_downsampled = self.df_minor.copy()
        self.df_downsampled = self.df_downsampled.set_index("timestamp_local")
        self.df_downsampled = self.df_downsampled.resample(resample_frequency).agg([percentile5, hourly_mean, percentile95]).reset_index() # .mean()

        self.df_downsampled.to_csv(minor_csv_path)

    def update_figure(self, start_date, end_date, wind_direction):
        print("HELLOOOOO WORLD")
        print("WIND DIRECTION:", wind_direction)

        self.df_filtered = self.df_downsampled[
            (self.df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (self.df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]

        if wind_direction is not None:
            self.df_filtered = self.df_filtered[
                (self.df_filtered["wind_dir"] >= FilterGraph.wind_dict[wind_direction][0]) &
                (self.df_filtered["wind_dir"] <  FilterGraph.wind_dict[wind_direction][1])
            ]

        fig = go.Figure([
            go.Scatter(
                name='Average',
                x=self.df_filtered["timestamp_local"],
                y=self.df_filtered["pm25"]["hourly_mean"],
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name='95th Percentile',
                x=self.df_filtered["timestamp_local"],
                y=self.df_filtered["pm25"]["percentile95"],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='5th PErcentile',
                x=self.df_filtered["timestamp_local"],
                y=self.df_filtered["pm25"]["percentile5"],
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