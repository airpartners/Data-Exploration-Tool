from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from time import strftime, strptime, mktime

import pandas as pd

print("HELLO WORLD!!! (0)")

df_major = pd.read_csv("C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv")

# df = df_major.head(int(60/2*24)) # one day of data
# df.to_csv("C:/dev/Air Partners/Data Analysis/data/east_boston/tempData1.csv")

# df_original = pd.read_csv("C:/dev/Air Partners/Data Analysis/data/east_boston/tempData1.csv")
# df = df_original.copy()
# df["timestamp_local"] = pd.to_datetime(df["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")

df_minor = df_major.copy()[["timestamp_local", "pm25"]]
df_minor["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df_minor["date"] = df_minor["timestamp_local"].dt.date

print("HELLO WORLD!!! (1)")

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.DatePickerRange(
        clearable = True,
        with_portal = True,
        start_date = (sd := df_minor['date'].min()).strftime("%Y-%m-%d"),
        end_date = (sd + pd.Timedelta(2, "days")).strftime("%Y-%m-%d"),
        # end_date = df_minor['date'].max().strftime("%Y-%m-%d"),
        id='my-date-picker-range'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_figure(start_date, end_date):
    print(start_date)
    print(end_date)
    # print(strptime(start_date, "%Y%m%d"))
    # print(pd.Timestamp(strptime(start_date, "%Y%m%d")))
    target_len = 100
    seconds_range = int((pd.Timestamp(end_date) - pd.Timestamp(start_date)) / np.timedelta64(1, 'm') // 2)
    print("seconds_range: ", seconds_range)
    print(str(seconds_range // target_len) + "T")
    # print(pd.to_datetime("5T"))

    # print("size of unfiltered dataframe = ", df_minor.size)

    resample_frequency = "1H"
    # resample_frequency = np.timedelta64(seconds_range // target_len, "m")
    # resample_frequency = str(seconds_range // target_len) + "min"

    def percentile5(df):
        return df.quantile(0.05)
    def percentile95(df):
        return df.quantile(0.95)
    def hourly_mean(df):
        return df.mean()

    df_downsampled = df_minor.copy()
    df_downsampled = df_downsampled.set_index("timestamp_local")
    df_downsampled = df_downsampled.resample(resample_frequency).agg([percentile5, hourly_mean, percentile95]).reset_index() # .mean()

    print(df_downsampled.head(5))

    df_filtered = df_downsampled[
        (df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) & (df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date())
    ]

    # print("size of filtered dataframe = ", df_filtered.size)
    # print("number of rows:", len(df_filtered.index))
    # print("column names: ", list(df_filtered.columns.values))
    # df_filtered["5th Percentile"] = df_filtered[('pm25', 'percentile5')]
    # df_filtered["mean"] = df_filtered[('pm25', 'mean')]
    # df_filtered = df_filtered.reset_index()
    # print("column names: ", list(df_filtered.columns.values))
    # df_filtered["5th Percentile"] = df_filtered.iloc[2]
    # df_filtered["mean"] = df_filtered.iloc[3]
    # df_filtered["95th Percentile"] = df_filtered.iloc[4]
    # df_filtered["5th Percentile"] = df_filtered.loc[('pm25', 'percentile5')]
    # print(df_filtered.head(2))
    # print(df_filtered[('pm25', 'percentile5')])

    # df_combined = df_filtered["timestamp_local"]
    print("heieriheoaroehaoiheoaihreihr")
    print(df_filtered["pm25"]["percentile5"])
    print(df_filtered["pm25"]["hourly_mean"])
    print("Success!")

    # fig = px.line(df_filtered, x="timestamp_local", y=[df_filtered["pm25"]["percentile5"],
    #                                                    df_filtered["pm25"]["hourly_mean"],
    #                                                    df_filtered["pm25"]["percentile95"]],
    #                 #  size="pop", color="continent", hover_name="country",
    #                 #  log_x=True, size_max=55
    #                 )

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
        title='PM2.5',
        hovermode="x"
    )

    # series_names = ["5th Percentile", "Average", "95th Percentile"]

    # for idx, name in enumerate(series_names):
    #     fig.data[idx].name = name
    #     fig.data[idx].hovertemplate = name

    # fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
