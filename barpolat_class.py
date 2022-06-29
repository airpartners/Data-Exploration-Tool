import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from csv_file_paths import processed_csv_paths

class BarPolar():
    def __init__(self):
        self.df = pd.read_parquet( processed_csv_paths[0])

    def update_figure(self, start_date, end_date):
        self.df_filtered = self.df[
            (self.df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (self.df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date())
        ]
        # fig = px.scatter_polar(self.df_filtered, r="ws", theta="wd", size=[10]*len(self.df_filtered), opacity=0.05)

        fig = go.Figure(go.Barpolar(
            # r=wd,
            # theta=ws,
            r=self.df_filtered['ws'],
            theta=self.df_filtered['wd'],
            width=20,
            # marker_color=["#E4FF87", '#709BFF', '#709BFF', '#FFAA70', '#FFAA70', '#FFDF70', '#B6FFB4'],
            # marker_line_color="black",
            # marker_line_width=2,
            opacity=0.8
        ))
        return fig

