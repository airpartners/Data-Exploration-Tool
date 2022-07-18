import pandas as pd

# df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code.csv')
# df = df_major.copy()
# df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
# df["date"] = df["timestamp_local"].dt.date


# resample_frequency = '1H'
# df_downsampled = df.copy()
# df_downsampled = df_downsampled.set_index("timestamp_local")
# df_downsampled = df_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


# #mean value
# mean_sn45 = df_downsampled.mean(axis=0)
# #median value
# median_sn45 = df_downsampled.median(axis=0)
# df_sn45={'sn45_mean': mean_sn45, 'sn45_median': median_sn45}
# dict45 = pd.DataFrame(df_sn45) 

# print(dict45)  


'''
sn45
'''
df45_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df45 = df45_major.copy()
df45["timestamp_local"] = pd.to_datetime(df45_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df45["date"] = df45["timestamp_local"].dt.date


resample_frequency = '1H'
df45_downsampled = df45.copy()
df45_downsampled = df45_downsampled.set_index("timestamp_local")
df45_downsampled = df45_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn45 = df45_downsampled.mean(axis=0)
#median value
median_sn45 = df45_downsampled.median(axis=0)





'''
sn46
'''
df46_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn46-final-w-ML-PM.csv')
df46 = df46_major.copy()
df46["timestamp_local"] = pd.to_datetime(df46_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df46["date"] = df46["timestamp_local"].dt.date


resample_frequency = '1H'
df46_downsampled = df46.copy()
df46_downsampled = df46_downsampled.set_index("timestamp_local")
df46_downsampled = df46_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn46 = df46_downsampled.mean(axis=0)
#median value
median_sn46 = df46_downsampled.median(axis=0)




'''
sn49
'''
df49_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn49-final-w-ML-PM.csv')
df49 = df49_major.copy()
df49["timestamp_local"] = pd.to_datetime(df49_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df49["date"] = df49["timestamp_local"].dt.date


resample_frequency = '1H'
df49_downsampled = df49.copy()
df49_downsampled = df49_downsampled.set_index("timestamp_local")
df49_downsampled = df49_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn49 = df49_downsampled.mean(axis=0)
#median value
median_sn49 = df49_downsampled.median(axis=0)






'''
sn62
'''
df62_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn62-final-w-ML-PM.csv')
df62 = df62_major.copy()
df62["timestamp_local"] = pd.to_datetime(df62_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df62["date"] = df62["timestamp_local"].dt.date


resample_frequency = '1H'
df62_downsampled = df62.copy()
df62_downsampled = df62_downsampled.set_index("timestamp_local")
df62_downsampled = df62_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn62 = df62_downsampled.mean(axis=0)
#median value
median_sn62 = df62_downsampled.median(axis=0)





'''
sn67
'''
df67_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn67-final-w-ML-PM.csv')
df67 = df67_major.copy()
df67["timestamp_local"] = pd.to_datetime(df67_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df67["date"] = df67["timestamp_local"].dt.date


resample_frequency = '1H'
df67_downsampled = df67.copy()
df67_downsampled = df67_downsampled.set_index("timestamp_local")
df67_downsampled = df67_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn67 = df67_downsampled.mean(axis=0)
#median value
median_sn67 = df67_downsampled.median(axis=0)





'''
sn72
'''
df72_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn72-final-w-ML-PM.csv')
df72 = df72_major.copy()
df72["timestamp_local"] = pd.to_datetime(df72_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df72["date"] = df72["timestamp_local"].dt.date


resample_frequency = '1H'
df72_downsampled = df72.copy()
df72_downsampled = df72_downsampled.set_index("timestamp_local")
df72_downsampled = df72_downsampled.resample(resample_frequency).agg('mean').reset_index() # .mean()


#mean value
mean_sn72 = df72_downsampled.mean(axis=0)
#median value
median_sn72 = df72_downsampled.median(axis=0)






df_snxx={
    'sn45_mean': mean_sn45, 'sn45_median': median_sn45,
    'sn46_mean': mean_sn46, 'sn46_median': median_sn46,
    'sn49_mean': mean_sn49, 'sn49_median': median_sn49,
    'sn62_mean': mean_sn62, 'sn62_median': median_sn62,
    'sn67_mean': mean_sn67, 'sn67_median': median_sn67, 
    'sn72_mean': mean_sn72, 'sn72_median': median_sn72,
    }
dict = pd.DataFrame(df_snxx) 

# saving the dataframe 
dict.to_csv('stats.csv') 

