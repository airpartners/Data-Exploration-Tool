import pandas as pd
from pathlib import Path
import os
from csv_file_paths import flight_csv_dir, processed_flight_dir, final_flights

class FlightLoader():
    """Class for loading and processing the flight data from Logan Airport. To run, initialize the FlightLoader object with a
`csv_dir`, `parquet_dir`, and `final_parquet_file`, then run flight_loader.process_files() and then flight_loader.combine_files().
When it's done creating the files on your computer, you can use the function add_flight_data_to contained in the file add_flight_data_to.py
to add flight data into an existing dataframe.
    """

    adverse_runways = {
        "sn45": {
            "D": ["22R", "22L", "4R", "4L"],
            "A": ["22R", "22L"]
            },
        "sn72": {
            "D": ["22R", "22L", "4R", "4L"],
            "A": ["22R", "22L"]
            },
        "sn46": {
            "D": ["33L", "15R", "15L"],
            "A": ["33L", "15R", "15L"]
            },
        "sn62": {
            "D": ["33L", "15R", "15L"],
            "A": ["33L", "15R", "15L"]
            },
        "sn67": {
            "D": ["9", "27"],
            "A": ["27"]
            },
        "sn49": {
            "D": ["22R", "22L", "4R", "4L"],
            "A": ["22R", "22L"]
            },
    }

    adverse_wind_dir = {
        "sn45": ["S", "SW"],
        "sn72": ["S", "SW"],
        "sn46": ["E", "SE", "NE"],
        "sn62": ["E", "SE", "NE"],
        "sn67": ["W", "NW"],
        "sn49": ["W", "SW"],
    }


    def __init__(self, csv_dir, parquet_dir, final_parquet_file) -> None:
        """`csv_dir` should be the path to a directory on your computer with a list of CSV files to be parsed.
The Logan Airport data comes in a bunch of files separated by month, which can be downloaded sheet-wise from this google spreadsheet (April 2020 - May 2021):
https://docs.google.com/spreadsheets/d/1WVQCzpq_QVtPJT4BSEq30PJzRrDLvqC5/edit?usp=sharing&ouid=117838158522092401592&rtpof=true&sd=true,
as well as this single CSV file for (June 2019 - April 2020): https://drive.google.com/file/d/1Dpxr71i97ktTbSn2OxsrzduH2EAr5HeF/view.
`parquet_dir` is the directory to dump the processed files when `process_files()` is called. One parquet file will be created for each CSV file in `csv_dir`.
When `combine_files()` is called, it takes all the processed files in `parquet_dir` and concatenates them into one large parquet file for easy access.
`final_parquet_file` is the file location, ending in `.parquet`, where the final concatenated data file will be stored.
"""
        self.csv_dir = csv_dir
        self.parquet_dir = parquet_dir
        self.final_parquet_file = final_parquet_file

        self.df_flights = None

        self.process_files()
        self.combine_files()

    def process_files(self):

        try:
            return pd.read_parquet(final_flights)
        except(FileNotFoundError):
            print(f'In DataImporter, looking for a processed file at "{final_flights}"')
            print(f'Processed file does not exist; reading raw CSV files from "{self.csv_dir}" instead.')

        # first, process all the csv files to create parquet files
        for root, dirs, files in os.walk(self.csv_dir):
            for filename in files:
                csv_path = os.path.join(root, filename)

                parquet_path = os.path.join(self.parquet_dir, Path(filename).with_suffix(".parquet"))
                if not os.path.exists(parquet_path):
                    self.process_csv(csv_path, parquet_path)

    def combine_files(self):
        # then, concatenate all the processed parquet files into one long dataframe
        for root, dirs, files in os.walk(self.parquet_dir):
            for filename in files:
                print("Concatenating file:", filename)
                parquet_path = os.path.join(root, filename)
                self.add_parquet(parquet_path)

        # sort values
        self.df_flights.sort_values("Date_Time", inplace = True)

        # export the dataframeto a large parquet file, to be joined with the air quality dataframe
        print(f'Finished performing processing. Now saving as "{self.final_parquet_file}."')
        self.df_flights.to_parquet(self.final_parquet_file)

    def process_csv(self, csv_path, parquet_path):
        col_names = pd.read_csv(csv_path, nrows=0).columns.tolist() # get the column names without reading the whole file

        if "Date" in col_names and "Time" in col_names:
            df = pd.read_csv(csv_path, parse_dates=[["Date", "Time"]])
            df["Date"] = df["Date_Time"]
        else:
            df = pd.read_csv(csv_path)

        resample_frequency = "1H"
        df["Date_Time"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d %H:%M:%S")
        # df["RW_group"] = df["RW"].apply(self.get_RW_group)
        df["RW_group"] = df["RW"]

        df_processed = df[["Date_Time", "Opr", "RW_group"]].set_index("Date_Time").resample(resample_frequency).agg(self.count_grouped_by, cols = ["Opr", "RW_group"]).reset_index()

        # pivot the table to get one column for departures and one row for arrivals
        # df_processed = df_processed.pivot_table(index = "Date_Time", columns = "RW_group", values = "count", aggfunc = "max")

        df_processed.to_parquet(parquet_path)
        print("Finished processing", csv_path)

    def count_grouped_by(self, df, cols = "Opr"):
        df["count"] = 1
        return df.groupby(cols).agg("sum")

    def get_RW_group(self, RW):
        if RW in ["22R", "22L", "22D"]:
            return "South-West"
        if RW in ["4L", "4R"]:
            return "North-East"
        if RW in ["27", "9", "15R", "33L"]:
            return "North-West"
        # else:
        return "Other"

    def is_adverse_runway(self, RW, opr, sensor_name = None):
        if sensor_name is None:
            return None
        if opr not in ["D", "A"]:
            return None
        # else:
        return RW in self.adverse_runways[sensor_name][opr]

    def add_parquet(self, parquet_path):
        if self.df_flights is None:
            self.df_flights = pd.read_parquet(parquet_path) 
        else:
            df_new = pd.read_parquet(parquet_path)
            self.df_flights = pd.concat([self.df_flights, df_new], axis = 'index')

    def add_flight_data_to(self, df, sensor_name = None, date_time_column_name = "timestamp_local"):
        self.df_flights["is_adverse_runway"] = self.df_flights.apply(lambda df: self.is_adverse_runway(df["RW_group"], df["Opr"], sensor_name), axis = 1)
        self.df_flights["adverse_flight_count"] = self.df_flights.apply(lambda df: df["count"] if df["is_adverse_runway"] else 0, axis = 1)
        self.df_flights2 = self.df_flights.groupby(["Date_Time"])[["adverse_flight_count", "count"]].sum()
        df_combined = df.reset_index().merge(self.df_flights2, left_on = date_time_column_name, right_on = "Date_Time").set_index(date_time_column_name)
        df_combined = df_combined.rename(columns = {"Date_Time": date_time_column_name})
        return df_combined