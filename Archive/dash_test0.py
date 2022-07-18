from dash import Dash, dcc, html, Input, Output
import plotly.express as px
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

    df_filtered = df_minor[
        (df_minor["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) & (df_minor["timestamp_local"].dt.date <= pd.Timestamp(end_date).date())
    ]

    print("size of filtered dataframe = ", df_filtered.size)
    print("number of rows:", len(df_filtered.index))

    fig = px.line(df_filtered, x="timestamp_local", y='pm25',
                    #  size="pop", color="continent", hover_name="country",
                    #  log_x=True, size_max=55
                    )

    # fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
