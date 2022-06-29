import pandas as pd
from data_importer import DataImporter

class FilterGraph():

    def __init__(self, data_importer = None):
        if data_importer is not None:
            self.data_importer = data_importer
        else:
            self.data_importer = DataImporter() # initialize the data

        self.stats = pd.read_csv('./stats.csv')
        self.stats = pd.DataFrame(self.stats)
        self.stats = self.stats.drop([5, 15, 22, 23, 24, 29, 30, 35])

    def filter_by_date(self, df, start_date, end_date):
        if start_date and end_date:
            return \
                df[
                    (df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                    (df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
                ]
        # else:
        return df

    def filter_by_wind_direction(self, df, wind_direction):
        if wind_direction is not None:
            return df[ df["wind_direction_cardinal", "my_mode"] == wind_direction ]
        # else:
        return df