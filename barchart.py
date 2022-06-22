from statistics import mean
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)

# df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv') # Lauren
df_major = pd.read_csv('C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv') # Ian

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
    # #mode value
    # data_mode = df_filtered.mode(axis=0)

    # fig = px.bar(
    #     x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    #     y=data_mean if data_stats == 'mean' else data_median, # if data_stats == 'median' else data_mode,
    #     color=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    #     height=550,
    #     barmode="group",
    #     text_auto=True
    # )

    fig=go.Figure()

    mean_sn45 = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, ]
    median_sn45 = [110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110]

    fig.add_bar(x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    y=mean_sn45 if data_stats == 'mean' else median_sn45,
    text=mean_sn45 if data_stats == 'mean' else median_sn45,
    name='entire dataset mean' if data_stats == 'mean' else 'entire dataset median')


    fig.add_bar(x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    y=data_mean if data_stats == 'mean' else data_median,
    text=data_mean if data_stats == 'mean' else data_median,
    name='selected data mean' if data_stats == 'mean' else 'selected data median',
    error_y =
        dict(
            type = 'data', # value of error bar given in data coordinates
            array = [50] * len(mean_sn45),
            visible = True
        )
    ) # if data_stats == 'median' else data_mode


    # for string in ['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML']:
    #     fig.add_shape(type="line",
    #         x0=string[0],
    #         y0=mean_sn45 if data_stats == 'mean' else median_sn45,
    #         x1=string[+1],
    #         y1=mean_sn45[0]+1 if data_stats == 'mean' else median_sn45[0]+1,
    #         line=dict(color='#0000FF', width = 4, dash='dashdot'))

    # i=0
    # while i <= len(mean_sn45):
    #     fig.add_bar(x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2','bin0','bin1','bin2','bin3','bin4','bin5','no_ae', 'tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    #         y=data_mean if data_stats == 'mean' else data_median,
    #         text=data_mean if data_stats == 'mean' else data_median,
    #         name='selected data mean' if data_stats == 'mean' else 'selected data median',
    #         secondary_y=True if mean_sn45[i] >= data_mean[i] else False
    #         ) # if data_stats == 'median' else data_mode

    #     i=i+1



    fig.update_layout(barmode="overlay")
    fig.update_traces(width=0.55)
    fig.update_layout(title_text="Change the title",
                title_font_size=30)


    print(type(enumerate(mean_sn45)))
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)