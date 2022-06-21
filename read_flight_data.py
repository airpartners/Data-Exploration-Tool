import pandas as pd
from pathlib import Path
import os
from csv_file_paths import flight_csv_dir, processed_flight_dir


def process_flights(csv_path, parquet_path):
    df = pd.read_csv(csv_path, parse_dates=[["Date", "Time"]])

    resample_frequency = "1H"
    df["Date_Time"] = pd.to_datetime(df["Date_Time"], format = "%Y-%m-%d %H:%M:%S")

    def sum_grouped_by_opr(df):
        return df.groupby("Opr").agg("sum")

    df["count"] = 1
    df_processed = df[["Date_Time", "Opr", "count"]].set_index("Date_Time").resample(resample_frequency).agg(sum_grouped_by_opr).reset_index()

    print("=========  df_processed  ===========")
    print(df_processed.head())

    df_processed.to_parquet(parquet_path)

# call process_flights on all the files
for root, dirs, files in os.walk(flight_csv_dir):
    for filename in files:
        csv_path = os.path.join(root, filename)

        parquet_path = os.path.join(processed_flight_dir, Path(filename).with_suffix(".parquet"))
        process_flights(csv_path, parquet_path)
