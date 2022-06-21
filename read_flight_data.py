import pandas as pd
from pathlib import Path
import os
from csv_file_paths import flight_csv_dir, processed_flight_dir, final_flights

class FlightLoader():
    def __init__(self, csv_dir, parquet_dir, final_parquet_file) -> None:
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

        df["count"] = 1
        df_processed = df[["Date_Time", "Opr", "count"]].set_index("Date_Time").resample(resample_frequency).agg(self.sum_grouped_by_opr).reset_index()

        print("=========  df_processed  ===========")
        print(df_processed.head())

        df_processed.to_parquet(parquet_path)

    def sum_grouped_by_opr(df):
        return df.groupby("Opr").agg("sum")

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