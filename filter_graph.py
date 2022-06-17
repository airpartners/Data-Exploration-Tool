import plotly.graph_objs as go
import pandas as pd
from csv_file_paths import raw_csv_paths, processed_csv_paths # import paths to csv files from another file in this repo.
    # you should make a copy of csv_file_paths.py and change the path names to match the file locations on your computer.

class FilterGraph():

    def __init__(self):
        self.list_of_sensor_dataframes = []
        for raw_file_path, processed_file_path in zip(raw_csv_paths, processed_csv_paths):
            # append the next sensor's worth of data to the list
            self.list_of_sensor_dataframes.append(self.prepare_data(raw_file_path, processed_file_path))
            pass

    def discrete_wind_direction(self, degrees):
        """Takes in a wind direction in degrees and bins it into cardinal directions"""
        wind_dict = {
            'N': [0, 22.5],
            'NE': [22.5, 67.5],
            'E': [67.5, 112.5],
            'SE': [112.5, 157.5],
            'S': [157.5, 202.5],
            'SW': [202.5, 247.5],
            'W': [247.5, 292.5],
            'NW': [292.5, 337.5],
        }
        for direction, bounds in wind_dict.items():
            if degrees >= bounds[0] and degrees < bounds[1]:
                return direction
            # else: # the direction is between 337.5 and 360 degrees
        return "N"

    def check_pre_processed_file(self, processed_file_path):
        """Takes in the expected path to a pre-processed csv file. First, it checks whether the processed file exists in the
        specified location. If the processed file exists, it reads the processed file and returns it.
        If the processed file does not exist, returns None. A new processed file will be generated in prepare_data().
        If you change the processing method, delete the csv_file_paths.processed_csv_paths files, and use this funciton
        to regenerate them according to the new processing scheme.
        """
        try:
            df_processed = pd.read_parquet(processed_file_path) # skip the column names
        except(FileNotFoundError):
            print('pre-processed file not found at "{processed_file_path}"')
            return None
        return df_processed
        # The agg() function used during processing creates a nested column structure, which is expected by update_figure().
        # When the file is saved to a CSV, the nested structure goes away, so we have to recreate it using a MultiIndex.
        # The fist element in each tuple is the top-level column, then the next element is the sub-column.
        # If the second element is blank, there are no sub-columns.
        # The resulting column names have a similar structure to this:
        # ----------------------------------------------------------------------------------------------------------- #
        #           row_id    |  timestamp_local |                  pm25                    | wind_direction_cardinal #
        #                     |                  | percentile5 | hourly_mean | percentile95 |                         #
        # --------------------+------------------+-------------+-------------+--------------+------------------------ #
        # 0      1 2019-09-07 | 16:00:00         |    0.433924 |    0.456453 |     0.479401 |                       W #
        # ...                                                                                                         #
        cols = pd.MultiIndex.from_tuples(
            [
                ("row_id", ''),
                ("timestamp_local", ''),
                ("pm25", "percentile5"),
                ("pm25", "hourly_mean"),
                ("pm25", "percentile95"),
                ("wind_direction_cardinal", '')
            ]
        )
        # Then, rename the columns to the MultiIndex
        df_processed.columns = cols
        # CSV files also do a bad job of storing datetimes in a format the Pandas recognizes as a datetime. Convert it.
        df_processed["timestamp_local"] = pd.to_datetime(df_processed["timestamp_local"], format = "%Y-%m-%d %H:%M:%S")
        return df_processed

    def prepare_data(self, raw_file, processed_file):
        """Takes in paths to two csv files. First, it checks whether the processed file exists in the specified
        location. If the processed file exists, it reads the processed file and returns it.
        If the processed file does not exist, then this function generates the processed dataframe from the raw data file.
        It stores the processed csv file in the processed_file location.
        """
        # Read the processed file and return it if it exists
        df_processed = self.check_pre_processed_file(processed_file)
        if df_processed is not None:
            return df_processed

        # The processed file has not yet been created. Read the raw data file and process it
        df_raw = pd.read_csv(raw_file)
        df_processed = df_raw[["timestamp_local", "pm25", "wind_dir"]] # select useful columns
        # convert timestamps to datetime objects, interpretable by Pandas
        df_processed["timestamp_local"] = pd.to_datetime(df_raw["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
        df_processed["date"] = df_processed["timestamp_local"].dt.date # create date column
        # create a new column with cardinal wind directions
        wind_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
        wind_breaks = [0, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, 360]


        df_processed["wind_direction_cardinal"] = pd.cut(df_processed["wind_dir"], wind_breaks, right = False, labels = wind_labels, ordered = False)
        # df_processed["wind_direction_cardinal"] = df_processed["wind_dir"].apply(self.discrete_wind_direction)

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
        # using built-in functions like "mean" (presumably because these are vectorized), as opposed to user-defined functions.s
        resample_frequency = "1H"
        df_processed = df_processed.set_index("timestamp_local").resample(resample_frequency).agg(
            {
                "pm25": [percentile5, "mean", percentile95],
                "wind_direction_cardinal": my_mode
            }
        ).reset_index()

        # store the processed and downsampled dataframe to a csv, to be read next time
        df_processed.to_parquet(processed_file)
        return df_processed

    def update_figure(self, which_sensor, start_date, end_date, wind_direction):

        # select which sensor data to draw from
        df_processed = self.list_of_sensor_dataframes[which_sensor]

        # filter by timestamp
        df_filtered = df_processed[
            (df_processed["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
            (df_processed["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
        ]

        # filter by wind direction
        if wind_direction is not None:
            df_filtered = df_filtered[
                df_filtered["wind_direction_cardinal", "my_mode"] == wind_direction
            ]
        # else: if wind_direction is None: pass

        # create the figure. It consists of a Figure frame and three lines created with go.Scatter()
        fig = go.Figure([
            go.Scatter(
                name = 'Average',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["mean"],
                mode = 'lines',
                line = dict(color = 'rgb(31, 119, 180)'),
            ),
            go.Scatter(
                name = '95th Percentile',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["percentile95"],
                mode = 'lines',
                marker = dict(color = "#444"),
                line = dict(width = 0),
                showlegend = False
            ),
            go.Scatter(
                name = '5th Percentile',
                x = df_filtered["timestamp_local"],
                y = df_filtered["pm25"]["percentile5"],
                marker = dict(color = "#444"),
                line = dict(width = 0),
                mode = 'lines',
                fillcolor = 'rgba(68, 68, 68, 0.3)',
                fill = 'tonexty',
                showlegend = False
            )
        ])

        fig.update_layout(
            yaxis_title = 'PM2.5',
            # title='PM2.5',
            hovermode = "x", # where the magic happens
            margin = {'t': 0}, # removes the awkward whitespace where the title used to be
        )

        return fig