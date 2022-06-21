import pandas as pd
from csv_file_paths import flight_csv_paths, processed_flight_paths

flights_raw = pd.read_csv(flight_csv_paths[0], parse_dates=[["Date", "Time"]])

print(flights_raw.head())

resample_frequency = "1H"
flights_raw["Date_Time"] = pd.to_datetime(flights_raw["Date_Time"], format = "%Y-%m-%d %H:%M:%S")

print(flights_raw.head())

def n_rows(df):
    return len(df.index)

def sum_grouped_by_opr(df):
    return df.groupby("Opr").agg(n_rows)

flights_raw["count"] = 1
df_processed = flights_raw[["Date_Time", "Opr", "count"]].set_index("Date_Time").resample(resample_frequency).agg(sum_grouped_by_opr).reset_index()

print("=========  df_processed  ===========")
print(df_processed.head())

df_processed.to_parquet(processed_flight_paths[0])

pass