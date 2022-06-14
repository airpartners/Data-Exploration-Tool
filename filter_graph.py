from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from time import strftime, strptime, mktime

import pandas as pd

class FilterGraph():
    def __init__(self):
        self.df_major = pd.read_csv("C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv")
        self.df_minor = self.df_major.copy()[["timestamp_local", "pm25"]]
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

    def update_figure(self, start_date, end_date):

        self.df_filtered = self.df_downsampled[
            (self.df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (self.df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
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
            title='PM2.5',
            hovermode="x"
        )

        return fig