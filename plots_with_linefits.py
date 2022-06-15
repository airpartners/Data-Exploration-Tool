from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go  


app = Dash(__name__)

df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df = df_major.copy()[["timestamp_local", "pm25", 'temp_box', 'pm10', 'no2', 'wind_dir']]
df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df["date"] = df["timestamp_local"].dt.date

# resample_frequency = "1H"
# df_downsampled = df.copy()
# df_downsampled = df_downsampled.set_index("timestamp_local")
# df_downsampled = df_downsampled.resample(resample_frequency)
# print(df_downsampled.head(10))


app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.DatePickerRange(
            clearable = True,
            with_portal = True,
            start_date = (sd := df['date'].min()).strftime("%Y-%m-%d"),
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


# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  date_value):
#     dff = df[df['timestamp_local'] == date_value]

#     fig = px.scatter(x=dff[dff['timestamp_local'] == xaxis_column_name]['pm25'],
#                      y=dff[dff['timestamp_local'] == yaxis_column_name]['pm25'],
#                      hover_name=dff[dff['timestamp_local'] == yaxis_column_name]['pm25'])

#     fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')





# def find_max_n(data, n):
#     """
#     Find the n largest values in an array
#     """
#     output = data.nlargest(n)
        
#     return output

# def days_max_gt_std(data, std):
#     """
#     Find the number of days where the maximum daily measurement is
#     above the standard used by the EPA
    
#     Inputs
#     ------
#         :param data: dataframe or Series with timestamp index and pollution data column.
#                     should already be resampled to appropriate timebase
#         :type data: pd.DataFrame or pd.Series
#         :param std: standard value used by EPA
#         :type std: float
    
#     Returns
#     -------
#         count: the number of days where the max value surpassed the standard
#     """
    
#     daily_max = data.groupby(data.index.floor('d')).max()
    
#     count = daily_max[daily_max > std].count()
    
#     return count



# def pm10_stats(data):
#     """
#     Compute the EPA monitoring report values for PM 10. Data should be in micrograms per
#     cubic meter.
    
#     Inputs
#     ------
#         :param data: dataframe or Series with timestamp index and pollution data column.
#                     should be resampled to 1h timebase
#         :type data: pd.DataFrame or pd.Series
        
#     Returns
#     -------
#         stats: dictionary of statistics
#     """
    
#     #24 hour statistics
#     mean_24h = data.resample('24h').mean()
    
#     #Highest and second-highest daily max 1-hour values
#     max12_24h = find_max_n(mean_24h, 2)
    
#     #Number of daily max 24-hour values that exceeded the level of the 24-hour standard
#     days_gt_std_24h = days_max_gt_std(mean_24h, 150)
    
#     stats = {
#         "pm10": {
#             "24h": {
#                 "mean": np.nanmean(mean_24h),
#                 "min": np.nanmin(mean_24h),
#                 "max_1": max12_24h[0],
#                 "max_2": max12_24h[1],
#                 "pct_25": np.nanpercentile(mean_24h, 25),
#                 "pct_75": np.nanpercentile(mean_24h, 75),
#                 "pct_98": np.nanpercentile(mean_24h, 98),
#                 "days_max_gt_std": days_gt_std_24h,
#             }
#         }
#     }
#     print(stats)
#     return stats
# pm10_stats(df)




def update_figure(start_date, end_date):
    target_len = 100
    seconds_range = int((pd.Timestamp(end_date) - pd.Timestamp(start_date)) / np.timedelta64(1, 'm') // 2)
    print("seconds_range: ", seconds_range)
    print(str(seconds_range // target_len) + "T")

    df_filtered = df[
        (df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) & (df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date())
    ]
    fig = px.scatter(df_filtered, x="temp_box", y=['pm25','pm10','no2'], 
        trendline="ols"
        # hover_name='pm25',
        # log_x=True, size_max=15
    )
    
    # spector_data = sm.datasets.spector.load(as_pandas=False)
    # spector_data.exog = sm.add_constant(spector_data.exog, prepend=False)

    # # Fit and summarize OLS model
    # mod = sm.OLS(spector_data.endog, spector_data.exog)
    # res = mod.fit()
    # print(res.summary())

    fig.update_layout(transition_duration=500)    
    string1 = "Behavior of variables versus temperature"
    myTitle = '<b>'+string1+'</b>'

    string2 = ' '
    myCaption = string2

    fig.update_layout(title=go.layout.Title(
        text=myTitle, font=dict(
        family="Courier New, monospace",
        size=22,
        color="#000000"
        ))
    )

    fig.update_layout(annotations=[
       go.layout.Annotation(
            showarrow=False,
            text=myCaption,
            xanchor='right',
            x=10,
            xshift=275,
            yanchor='top',
            y=-5,
            font=dict(
                family='Aria',
                size=16,
                color="#000000"
            )
        )
    ])
    results = px.get_trendline_results(fig)

    model = results.px_fit_results.iloc[0].summary()
    model.__repr__()
    print(model)
    return fig
    
    


if __name__ == '__main__':
    app.run_server(debug=True)
