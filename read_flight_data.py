import pandas as pd
from pathlib import Path
import os
from csv_file_paths import flight_csv_dir, processed_flight_dir, final_flights

class FlightLoader():
    """Class for loading and processing the flight data from Logan Airport. To run, initialize the FlightLoader object with a
`csv_dir`, `parquet_dir`, and `final_parquet_file`, then run flight_loader.process_files() and then flight_loader.combine_files().
When it's done creating the files on your computer, you can use the function add_flight_data contained in the file add_flight_data.py
to add flight data into an existing dataframe.
    """
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

        self.df_combined = None

    def process_files(self):

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

        # export the dataframeto a large parquet file, to be joined with the air quality dataframe
        self.df_combined.to_parquet(self.final_parquet_file)

    def process_csv(self, csv_path, parquet_path):
        col_names = pd.read_csv(csv_path, nrows=0).columns.tolist() # get the column names without reading the whole file

        if "Date" in col_names and "Time" in col_names:
            df = pd.read_csv(csv_path, parse_dates=[["Date", "Time"]])
            df["Date"] = df["Date_Time"]
        else:
            df = pd.read_csv(csv_path)

        resample_frequency = "1H"
        df["Date_Time"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d %H:%M:%S")
        df["RW_group"] = df["RW"].apply(self.get_RW_group)

        df_processed = df[["Date_Time", "Opr", "RW_group"]].set_index("Date_Time").resample(resample_frequency).agg(self.count_grouped_by, cols = ["Opr", "RW_group"]).reset_index()

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

    def add_parquet(self, parquet_path):
        if self.df_combined is None:
            self.df_combined = pd.read_parquet(parquet_path)
        else:
            df_new = pd.read_parquet(parquet_path)
            pd.concat([self.df_combined, df_new], axis = 'index')

def main():
    loader = FlightLoader(flight_csv_dir, processed_flight_dir, final_flights)
    loader.process_files()
    loader.combine_files()

    df_flights = pd.read_parquet(final_flights)
    print(df_flights.head())
    print(len(df_flights.index))
    pass

main()