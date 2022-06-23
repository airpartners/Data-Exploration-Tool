from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

class BarChart():
    def __init__(self):
        self.df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
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


    def update_figure(self,start_date, end_date, data_stats, percentage_error):
        '''
        Main plotting function
        '''
        self.df_filtered = self.df_downsampled[
                (self.df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                (self.df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
            ]   
        self.df_filtered = self.df_filtered.drop(columns=['no_ae', 'co_ae', 'no2_ae', 'co2', 'removeCO','timediff','flag'])

        
        #mean of the filtered data
        data_mean = self.df_filtered.mean(axis=0)
        #median of the filtered data
        data_median = self.df_filtered.median(axis=0)

        fig=go.Figure()

        #make two separate lists of the means and medians of the entire dataset
        sn45_mean = self.df_stats['sn45_mean']
        sn45_median = self.df_stats['sn45_median']

        
        

        #calculate standard deviation of filtered data
        standdev = []
        for i in self.df_downsampled.columns[1:]:
                standdev.append(np.nanstd(self.df_downsampled[i])) # if means!=0.000000 else standdev_mean.append(0)

        #mean standardization: divide filtered data mean by entire dataset mean
        quotients_mean = []
        #mean percentage error: divide standard deviation of filtered data mean by entire dataset mean
        error_by_mean = []
        for mean,means,i in zip(data_mean,sn45_mean,standdev):
            quotients_mean.append(mean/means) if means!=0.000000 else quotients_mean.append(0)
            error_by_mean.append((i-means)/means) if means!=0.000000 else error_by_mean.append(0)

        #median standardization: divide filtered data median by entire dataset median
        quotients_median = []
        #median percentage error: divide standard deviation of filtered data median by entire dataset median
        error_by_median = []
        for median, medians,i in zip (data_median, sn45_median,standdev):
            quotients_median.append(median/medians) if medians!=0.000000 else quotients_median.append(0)
            error_by_median.append((i-medians)/medians) if medians!=0.000000 else error_by_median.append(0)



        #create subplots
        fig = make_subplots(rows=1, cols=3, subplot_titles=('Meterology Data','Gas Pollutents','Particle Pollutents'))
        

        #first subplot of meterology data
        fig.add_trace(
            go.Bar(
                x=['temp_box','temp_manifold','rh_manifold','pressure','noise','solar','wind_dir','wind_speed'],
                y=quotients_mean[0:8] if data_stats == 'Mean' 
                else  quotients_median[0:8],
                text=quotients_mean[0:8] if data_stats == 'Mean' else quotients_median[0:8],
                opacity=1,
                marker_color=px.colors.qualitative.T10[2],
                name='meterology data',
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


        #second subplot of pollutent gas concentration data
        fig.add_trace(
            go.Bar(
                x=['co','no','no2','o3'],
                y=quotients_mean[8:12] if data_stats == 'Mean' 
                else  quotients_median[8:12],
                text=quotients_mean[8:12] if data_stats == 'Mean' else quotients_median[8:12],
                opacity=1,
                marker_color=px.colors.qualitative.T10[0],       
                name='pollutent gas data',                 
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

        #third subplot of pollutent particle concentration data
        fig.add_trace(
            go.Bar(
                x=['pm1','pm25','pm10','particle size 0','particle size 1','particle size 2','particle size3','particle size4','particle size 5'],
                y=quotients_mean[12:21] if data_stats == 'Mean' 
                else  quotients_median[12:21],
                text=quotients_mean[12:21] if data_stats == 'Mean' else quotients_median[12:21],
                opacity=1,
                marker_color=px.colors.qualitative.T10[1],      
                name='pollutent particle data',
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

        #add title
        fig.update_layout(title_text="Bar Chart of Standarized Data", title_font_size=30)
        #mark the line y=1 i.e. when filtered mean/median equals entire dataset mean/median
        fig.add_hline(y=1, line_width=3, line_dash="dot", line_color="navy", annotation=None)

        return fig
