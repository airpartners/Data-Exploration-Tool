# function to load files
import pandas as pd
import numpy as np

class Load():
    def __init__(self):
        self.stats = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/stats.csv')
        self.df_stats = pd.DataFrame(self.stats)
        #drop ['solar', 'no_ae', 'co_ae', 'no2_ae', 'co2', 'removeCO','timediff','flag'] because we don't need them
        self.df_stats = self.df_stats.drop([0,5,6,7,8,9,10,11,12,13,14,15,22,23,24,25,28,29,30,35])

    def calculate(self, start_date, end_date, sensor):

        self.df_major = pd.read_csv(sensor)
        self.df = self.df_major.copy()
        self.df["timestamp_local"] = pd.to_datetime(self.df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        self.df["date"] = self.df["timestamp_local"].dt.date

        resample_frequency = '1H'
        self.df_downsampled = self.df.copy()
        self.df_downsampled = self.df_downsampled.set_index("timestamp_local")
        self.df_downsampled = self.df_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()

        self.df_filtered = self.df_downsampled[
                (self.df_downsampled["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                (self.df_downsampled["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
            ]

        self.df_filtered = self.df_filtered.drop(columns=[
            'temp_box','solar','wind_dir','wind_speed','co','no','no2','o3','pm1','pm25','pm10','co2',
            'no_ae', 'co_ae', 'no2_ae', 'tmpc', 'correctedNO', 'removeCO','timediff','flag'
            ])

        #mean of the filtered data
        data_mean = self.df_filtered.mean(axis=0)
        #median of the filtered data
        data_median = self.df_filtered.median(axis=0)
        mean_index=str(sensor[47:51]+'_mean')
        median_index=str(sensor[47:51]+'_median')
        snxx_mean = self.df_stats[mean_index]
        snxx_median = self.df_stats[median_index]


        standdev = []
        for i in self.df_filtered.columns[1:]:
                standdev.append(np.nanstd(self.df_filtered[i])) if self.df_filtered[i] is not str else standdev.append(None)

        #mean standardization: divide filtered data mean by entire dataset mean
        quotients_mean = []
        #mean percentage error: divide standard deviation of filtered data mean by entire dataset mean
        error_by_mean = []
        #median standardization: divide filtered data median by entire dataset median
        quotients_median = []
        #median percentage error: divide standard deviation of filtered data median by entire dataset median
        error_by_median = []
        for mean,means,median,medians,i in zip (data_mean,snxx_mean,data_median, snxx_median,standdev):
            quotients_mean.append(mean/means) if means is not str and means!=0.000000 else quotients_mean.append(0)
            error_by_mean.append(abs((i-means)/means)) if means is not str and means!=0.000000 else error_by_mean.append(0)
            quotients_median.append(median/medians) if medians is not str and medians!=0.000000 else quotients_median.append(0)
            error_by_median.append(abs((i-medians)/medians)) if medians is not str and medians!=0.000000 else error_by_median.append(0)


        round_quotients_mean = list([round(num,3) for num in quotients_mean])
        round_quotients_median = list([round(num,3) for num in quotients_median])

        return round_quotients_mean, round_quotients_median





