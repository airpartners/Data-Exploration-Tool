from shutil import which
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from pandas import *

class ScatterPlot():
    def __init__(self):
        self.df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Final Time Series/sn46-final-w-ML-PM.csv')
        self.df = self.df_major.copy()
        self.df["timestamp_local"] = pd.to_datetime(self.df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        self.df["date"] = self.df["timestamp_local"].dt.date

        resample_frequency = '1H'
        self.df_downsampled = self.df.copy()
        self.df_downsampled = self.df_downsampled.set_index("timestamp_local")
        self.df_downsampled = self.df_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()

        self.stats = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/stats.csv')
        self.df_stats = pd.DataFrame(self.stats)
        self.df_stats = self.df_stats.drop([15, 22, 23, 24, 29, 30, 35])

    def update_figure(self, start_date, end_date, xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
        target_len = 100
        seconds_range = int((pd.Timestamp(end_date) - pd.Timestamp(start_date)) / np.timedelta64(1, 'm') // 2)
        # print("seconds_range: ", seconds_range)
        # print(str(seconds_range // target_len) + "T")

        self.df_filtered = self.df_downsampled[
            (self.df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) & (self.df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date())
        ]

        fig = px.scatter(self.df_filtered, x=xaxis_column_name, y=yaxis_column_name,
            trendline="ols",
            hover_name='timestamp_local',
            # log_x=True, size_max=15
        )

        # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

        fig.update_xaxes(title=xaxis_column_name,
                        type='linear' if xaxis_type == 'Linear' else 'log')

        fig.update_yaxes(title=str(yaxis_column_name),
                        type='linear' if yaxis_type == 'Linear' else 'log')


        # spector_data = sm.datasets.spector.load(as_pandas=False)
        # spector_data.exog = sm.add_constant(spector_data.exog, prepend=False)

        # # Fit and summarize OLS model
        # mod = sm.OLS(spector_data.endog, spector_data.exog)
        # res = mod.fit()
        # print(res.summary())

        fig.update_layout(transition_duration=500)

        # set title and caption
        string1 = "Scatter plot"
        myTitle = '<b>'+string1+'</b>'

        string2 = 'This is the caption'
        myCaption = string2


        fig.update_layout(title=go.layout.Title(
            text=myTitle, font=dict(
            family="Courier New, monospace",
            size=22,
            color="#000000"
            ))
        )

        # fig.update_layout(annotations=[
        #    go.layout.Annotation(
        #         showarrow=False,
        #         text=myCaption,
        #         xanchor='right',
        #         x=10,
        #         xshift=275,
        #         yanchor='top',
        #         y=-5,
        #         font=dict(
        #             family='Aria',
        #             size=16,
        #             color="#000000"
        #         )
        #     )
        # ])

        return fig

