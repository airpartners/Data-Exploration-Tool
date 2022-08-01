import pandas as pd
from data_importer import DataImporter

class FilterGraph():

    def __init__(self, data_importer = None):
        if data_importer is not None:
            self.data_importer = data_importer
        else:
            self.data_importer = DataImporter() # initialize the data

    def filter_by_date(self, df, start_date, end_date):
        if start_date and end_date:
            return \
                df[
                    (df.index.date >= pd.Timestamp(start_date).date()) &
                    (df.index.date <= pd.Timestamp(end_date).date()  )
                    # (df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                    # (df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
                ]
        # else:
        return df

    def normalize_height(self, df, max_val = 1, do_it = True):
        if not do_it:
            return df
        return df / df.select_dtypes('number').max() * max_val # TODO: Write Stackoverflow answer: https://stackoverflow.com/questions/49412694/divide-two-pandas-dataframes-and-keep-non-numeric-columns

    def normalize_percent_diff(self, df, starting_val = 100, do_it = True):
        if not do_it:
            return df
        pass

    def filter_by_wind_direction(self, df, wind_direction):
        if wind_direction is not None:
            return df[ df["wind_direction_cardinal"] == wind_direction ]
            # return df[ df["wind_direction_cardinal", "my_mode"] == wind_direction ]
        # else:
        return df