import pandas as pd
from csv_file_paths import final_flights

def add_flight_data(df, date_time_column_name = "timestamp_local"):
    df_flights = pd.read_parquet(final_flights)

    return df.merge(df_flights, left_on = date_time_column_name, right_on = "Date_Time")