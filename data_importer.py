import pandas as pd
import os
from csv_file_paths import raw_csv_paths, processed_csv_paths, stats_file # import paths to csv files from another file in this repo.
    # you should make a copy of csv_file_paths.py and change the path names to match the file locations on your computer.

class DataImporter():
    columns_to_keep = {
        # 'date_local': 'numeric',
        # 'timestamp': 'numeric',
        # 'timestamp_local': 'numeric',
        # 'temp_box': 'numeric',
        'temp_manifold': 'numeric',
        'rh_manifold': 'numeric',
        'pressure': 'numeric',
        'noise': 'numeric',
        # 'solar': 'numeric',
        # 'wind_dir': 'numeric',
        # 'wind_speed': 'numeric',
        # 'co': 'numeric',
        # 'no': 'numeric',
        # 'no2': 'numeric',
        # 'o3': 'numeric',
        # 'pm1': 'numeric',
        # 'pm25': 'numeric',
        # 'pm10': 'numeric',
        # 'co2': 'numeric',
        'bin0': 'numeric',
        'bin1': 'numeric',
        'bin2': 'numeric',
        'bin3': 'numeric',
        'bin4': 'numeric',
        'bin5': 'numeric',
        # 'no_ae': 'numeric',
        # 'co_ae': 'numeric',
        # 'no2_ae': 'numeric',
        # 'date': 'numeric',
        # 'originaldate': 'numeric',
        # 'timestamp.x': 'numeric',
        # 'originaldate.x': 'numeric',
        # 'timestamp.y': 'numeric',
        # 'originaldate.y': 'numeric',
        # 'original_met_time': 'numeric',
        # 'tmpc': 'numeric',
        'wd': 'numeric',
        'ws': 'numeric',
        # 'day': 'numeric',
        'correctedNO': 'numeric',
        # 'timediff': 'numeric',
        # 'removeCO': 'numeric',
        # 'igor_date': 'numeric',
        # 'igor_date_local': 'numeric',
        # 'timestamp.ML': 'numeric',
        'co.ML': 'numeric',
        # 'no.ML': 'numeric',
        'no2.ML': 'numeric',
        'o3.ML': 'numeric',
        # 'flag': 'numeric',
        'pm1.ML': 'numeric',
        'pm25.ML': 'numeric',
        'pm10.ML': 'numeric',
        # 'date.ML': 'numeric',
        # 'originaldate.ML': 'numeric',
        'wind_direction_cardinal': 'discrete',
    }
    numeric_columns_to_keep = [col for col, val in columns_to_keep.items() if val == 'numeric']

    def __init__(self):
        self.list_of_sensor_dataframes = []
        for raw_file_path, processed_file_path in zip(raw_csv_paths, processed_csv_paths):
            # append the next sensor's worth of data to the list
            self.list_of_sensor_dataframes.append(self.prepare_data(raw_file_path, processed_file_path))
        self.df_stats = self.make_stats()

    def check_pre_processed_file(self, processed_file_path):
        """Takes in the expected path to a pre-processed parquet file. First, it checks whether the processed file exists in the
        specified location. If the processed file exists, it reads the processed file and returns it.
        If the processed file does not exist, returns None. A new processed file will be generated in prepare_data().
        If you change the processing method, delete the csv_file_paths.processed_csv_paths files, and use this funciton
        to regenerate them according to the new processing scheme.
        """
        try:
            df_processed = pd.read_parquet(processed_file_path) # skip the column names
        except(FileNotFoundError):
            print(f'In DataImporter, looking for a processed file at "{processed_file_path}"')
            print(f'Processed file does not exist; performing processing and saving as "{processed_file_path}".')
            return None
        return df_processed

    def prepare_data(self, raw_file, processed_file):
        """Takes in paths to two files. First, it checks whether the processed parquet file exists in the specified
        location. If the processed file exists, it reads the processed file and returns it.
        If the processed file does not exist, then this function generates the processed dataframe from the raw data csv file.
        It stores the processed parquet file in the processed_file location.
        """
        # Read the processed file and return it if it exists
        df_processed = self.check_pre_processed_file(processed_file)
        if df_processed is not None:
            return df_processed

        # The processed file has not yet been created. Read the raw data file and process it
        df_raw = pd.read_csv(raw_file)
        # df_processed = df_raw[["timestamp_local", "pm25", "wind_dir"]] # select useful columns
        # convert timestamps to datetime objects, interpretable by Pandas
        df_processed = df_raw
        df_processed["timestamp_local"] = pd.to_datetime(df_raw["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        # df_processed["date"] = df_processed["timestamp_local"].dt.date # create date column
        # create a new column with cardinal wind directions
        wind_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
        wind_breaks = [0, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, 360]


        df_processed["wind_direction_cardinal"] = pd.cut(df_processed["wind_dir"], wind_breaks, right = False, labels = wind_labels, ordered = False)

        # define functions which will be used in the resample().agg() call below
        def percentile5(df):
            return df.quantile(0.05)
        def percentile95(df):
            return df.quantile(0.95)
        def my_mode(df):
            mode = df.mode()
            return mode[0] if not mode.empty else None

        # The following line resamples the dataframe based on the timestamps in the "timestamp_local" column.
        # resmaple() works on the index of the dataframe, so we use set_index before and reset_index afterward.
        # The resample_frequency is a string like "1H" or a np.timeDelta64 object.
        # The agg() function controls how to combine the data that is placed in the same bin.
        # agg() can take a single function, a list of functions, or a dictionary of {columns: funcitons} if you want
        # to apply different aggregation functions to different columns.
        # The functions can be in quotes if they are funcitons Pandas will recognize; you can also pass in user-defined
        # functions, such as for taking specific percentiles. Lambda functions will also work.

        # Sadly, the resampling and aggregation process takes a long time (several seconds to a minute) to run. It is much faster
        # using built-in functions like "mean" (presumably because these are vectorized), as opposed to user-defined functions.

        df_processed.set_index("timestamp_local", inplace = True)
        df_processed = df_processed[self.columns_to_keep]

        agg_funcs = {}
        for col_name, col_type in self.columns_to_keep.items():
            if col_type == 'numeric':
                agg_funcs[col_name] = "mean"
            else:
                agg_funcs[col_name] = my_mode

        # agg_funcs.pop("timestamp_local") # remove this because it will become the index

        resample_frequency = "1H"
        df_processed = df_processed.resample(resample_frequency).agg(agg_funcs)


        # store the processed and downsampled dataframe to a csv, to be read next time
        df_processed.to_parquet(processed_file)
        return df_processed

    def get_data_by_sensor(self, sensor_id, numeric_only = False):
        if numeric_only:
            return self.list_of_sensor_dataframes[sensor_id][self.numeric_columns_to_keep]
        # else:
        return self.list_of_sensor_dataframes[sensor_id]

    def get_sensor_name_from_file(self, filename):
        return os.path.basename(filename).split('-')[0]

    def get_all_sensor_names(self):
        sensor_names = []
        for filename in raw_csv_paths:
            sensor_names.append(self.get_sensor_name_from_file(filename))
        return sensor_names

    def make_stats(self):
        df_stats = self.check_pre_processed_file(stats_file)
        if df_stats is not None: # then the processed file already exists, and we don't need to recalculate it
            return df_stats

        iterables = [self.get_all_sensor_names(), ["mean", "median"]]
        columns = pd.MultiIndex.from_product(iterables, names = ["sensor", "agg_func"])
        df_stats = pd.DataFrame(index = self.numeric_columns_to_keep, columns = columns)

        for i, raw_file in enumerate(raw_csv_paths):
            print(f"Generating stats from {raw_file}")
            sensor_name = self.get_sensor_name_from_file(raw_file)
            df_raw = pd.read_csv(raw_file)
            df_stats[sensor_name, "mean"] = df_raw[self.numeric_columns_to_keep].mean(axis = 0)
            df_stats[sensor_name, "median"] = df_raw[self.numeric_columns_to_keep].median(axis = 0)

        df_stats.to_parquet(stats_file)
        return df_stats
