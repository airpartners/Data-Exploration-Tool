from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


app = Dash(__name__)



df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df = df_major.copy()
df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df["date"] = df["timestamp_local"].dt.date

resample_frequency = '1H'
df_downsampled = df.copy()
df_downsampled = df_downsampled.set_index("timestamp_local")
df_downsampled = df_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()

stats = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/stats.csv')
df_stats = pd.DataFrame(stats)
df_stats = df_stats.drop([15, 22, 23, 24, 29, 30, 35])


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
                ['Mean', 'Median'],
                'Mean',
                id='data-stats'
            ),
            dcc.RadioItems(
                options=[{'label': i, 'value': i} for i in ['Show Percentage Error', 'Hide Percentage Error']],
                value='Show',
                id='percentage-error',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
])

@app.callback(
    Output('bar-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('data-stats', 'value'),
    Input('percentage-error','value')
)


def update_figure(start_date, end_date, data_stats, percentage_error):
   
    df_filtered = df_downsampled[
            (df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]   
    df_filtered = df_filtered.drop(columns=['no_ae', 'co_ae', 'no2_ae', 'co2', 'removeCO','timediff','flag'])


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

    sn45_mean = df_stats['sn45_mean']
    sn45_median = df_stats['sn45_median']
    # sn45_mean = sn45_mean.reset_index('variable_name')
    # sn45_median = sn45_median.reset_index('variable_name')
    # print(sn45_median['co'])

    

    


    standdev = []
    quotients_mean = []
    quotients_median = []
    error_by_mean = []
    error_by_median = []

    for i in df_downsampled.columns[1:]:
            standdev.append(np.nanstd(df_downsampled[i])) # if means!=0.000000 else standdev_mean.append(0)

    for mean,means,i in zip(data_mean,sn45_mean,standdev):
        quotients_mean.append(mean/means) if means!=0.000000 else quotients_mean.append(0)
        error_by_mean.append((i-means)/means) if means!=0.000000 else error_by_mean.append(0)


    for median, medians,i in zip (data_median, sn45_median,standdev):
        quotients_median.append(median/medians) if medians!=0.000000 else quotients_median.append(0)
        error_by_median.append((i-medians)/medians) if medians!=0.000000 else error_by_median.append(0)


    fig = make_subplots(rows=1, cols=3, subplot_titles=('Meterology Data','Gas Pollutents','Particle Pollutents'))
    
    fig.add_hline(y=1, line_width=3, line_dash="dot", line_color="navy")

    fig.add_trace(
        go.Bar(
            x=['temp_box','temp_manifold','rh_manifold','pressure','noise','solar','wind_dir','wind_speed'],
            y=quotients_mean[0:8] if data_stats == 'Mean' 
            else  quotients_median[0:8],
            text=quotients_mean[0:8] if data_stats == 'Mean' else quotients_median[0:8],
            opacity=1,
            marker_color=px.colors.qualitative.T10[2],
            name='Meterology Data',
            showlegend=False,   
            error_y =
                dict(
                    type='data', # value of error bar given in data coordinates
                    array=error_by_mean[0:8] if data_stats == 'Mean' else error_by_median[0:8],
                    visible = True if percentage_error=='Show Percentage Error' else False
                )
        ),
    row=1, col=1
    )


    fig.add_trace(
        go.Bar(
            x=['co','no','no2','o3'],
            y=quotients_mean[8:12] if data_stats == 'Mean' 
            else  quotients_median[8:12],
            text=quotients_mean[8:12] if data_stats == 'Mean' else quotients_median[8:12],
            opacity=1,
            marker_color=px.colors.qualitative.T10[0],       
            name='Gas Pollutent',                 
            showlegend=False,   
            error_y =
                dict(
                    type='data', # value of error bar given in data coordinates
                    array=error_by_mean[8:12] if data_stats == 'Mean' else error_by_median[8:12],
                    visible = True if percentage_error=='Show Percentage Error' else False
                )
        ),
    row=1, col=2
    )


    fig.add_trace(
        go.Bar(
            x=['pm1','pm25','pm10','particle size 0','particle size 1','particle size 2','particle size3','particle size4','particle size 5'],
            y=quotients_mean[12:21] if data_stats == 'Mean' 
            else  quotients_median[12:21],
            text=quotients_mean[12:21] if data_stats == 'Mean' else quotients_median[12:21],
            opacity=1,
            marker_color=px.colors.qualitative.T10[1],      
            name='Particle Pollutent',
            showlegend=False,
            error_y =
                dict(
                    type='data', # value of error bar given in data coordinates
                    array=error_by_mean[12:21] if data_stats == 'Mean' else error_by_median[12:21],
                    visible = True if percentage_error=='Show Percentage Error' else False
                )
        ),
    row=1, col=3
    )

    
    fig.add_hline(y=1, line_width=3, line_dash="dot", line_color="navy", annotation=None)




    # fig.add_bar(
    #     x=['temp_box','temp_manifold','rh_manifold','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','bin0','bin1','bin2','bin3','bin4','bin5', 'tmpc', 'wd', 'ws', 'correctedNO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    #     y=quotients_mean if data_stats == 'Mean' else  quotients_median,
    #     text=data_mean if data_stats == 'Mean' else data_median,
    #     name='Data Standardized by Mean' if data_stats == 'Mean' else 'Data Standardized by Median'
    #     # error_y =
    #     #     dict(
    #     #         type='data', # value of error bar given in data coordinates
    #     #         array=error_by_mean if data_stats == 'Mean' else error_by_median,
    #     #         visible = True
    #     #     )
    # )
    

    # fig.add_bar(x=['temp_box','temp_manifold','rh_manifold','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','bin0','bin1','bin2','bin3','bin4','bin5','tmpc', 'wd', 'ws', 'correctedNO', 'removeCO', 'co.ML', 'no.ML', 'o2.ML', 'o3.ML', 'flag', 'pm1.ML', 'pm25.ML', 'pm10.ML'],
    # y=data_mean if data_stats == 'Mean' else data_median,
    # text=data_mean if data_stats == 'Mean' else data_median,
    # name='selected data mean' if data_stats == 'Mean' else 'selected data median') # if data_stats == 'median' else data_mode 

    fig.update_layout(barmode="overlay")
    fig.update_traces(width=0.55)
    fig.update_layout(title_text="Bar Chart of Standardized Data",
                title_font_size=30)

    # fig.update_traces(
    #     hoverinfo=[data_mean[12:21]]
    #     # hovertemplate =
    #     #         '<b>mean of filtered data</b>: %{marker.size:,}<br>'+ "<extra></extra>"+
    #     #         '<b>mean of entire data set</b>: %{sn45_mean[12:21]}<br>'+
    #     #         '<b>percentage error</b>: %{y:.2f}'
    #     #         if data_stats == 'Mean' else 
    #     #         '<br><b>median of filtered data</b>: %{data_median[12:21]}<br>'+
    #     #         '<br><b>median of entire data set</b>: %{sn45_median[12:21]}<br>'+
    #     #         '<b>percentage error</b>: %{y:.2f}',
    #     #     marker_size=data_mean[12:21],
    # )

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)