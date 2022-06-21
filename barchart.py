from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


app = Dash(__name__)

df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df = df_major.copy()
df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df["date"] = df["timestamp_local"].dt.date


resample_frequency = '1H'
df_downsampled = df.copy()
df_downsampled = df_downsampled.set_index("timestamp_local")
df_downsampled = df_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()

app.layout = html.Div([
    dcc.Graph(id='bar-plot'),
    dcc.DatePickerRange(
        clearable = True,
        with_portal = True,
        start_date = (sd := df['date'].min()).strftime("%Y-%m-%d"),
        end_date = (sd + pd.Timedelta(2, "days")).strftime("%Y-%m-%d"),
        # end_date = df_minor['date'].max().strftime("%Y-%m-%d"),
        id='my-date-picker-range'
    ),
    html.Div([
            dcc.Dropdown(
                ['mean', 'median'],
                id='data-stats'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
])

@app.callback(
    Output('bar-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('data-stats', 'value')
)




def update_figure(start_date, end_date, data_stats):
   
    df_filtered = df_downsampled[
            (df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]   
    df_filtered = df_filtered.drop(columns=['pressure', 'noise', 'co_ae', 'no2_ae', 'timediff'])


    #mean value
    data_mean = df_filtered.mean(axis=0)
    #median value
    data_median = df_filtered.median(axis=0)
    #mode value
    data_mode= df_filtered.mode(axis=0)

    mmm = [data_mean, data_median]
    print(df_filtered.iloc[: , -39:].any())
    temp = df_filtered.copy()
    temp = temp.head(39)

    fig = px.bar(
        x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
        y=data_mean if data_stats == 'mean' else data_median,
        color=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
        height=600,
        barmode="group",
        text_auto=True
    ) 
    fig.update_traces(width=0.8)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)