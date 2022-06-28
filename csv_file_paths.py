import os
user_profile = os.path.basename(os.path.normpath(os.environ['USERPROFILE']))

if user_profile == "ieykamp":
    raw_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn46-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn49-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn62-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn67-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn72-final-w-ML-PM.csv",
    ]

    processed_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn45-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn46-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn49-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn62-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn67-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn72-final-w-ML-PM.parquet",
    ]

    flight_csv_dir = "C:/dev/Air Partners/Data Analysis/data/flights/raw/"

    processed_flight_dir = "C:/dev/Air Partners/Data Analysis/data/flights/processed/"

    final_flights = "C:/dev/Air Partners/Data Analysis/data/flights/final/combined_flights.parquet"

elif user_profile == "zxiong":
    raw_csv_paths = [
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv',
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn46-final-w-ML-PM.csv',
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn49-final-w-ML-PM.csv',
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn62-final-w-ML-PM.csv',
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn67-final-w-ML-PM.csv',
        'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn72-final-w-ML-PM.csv'
    ]

    processed_csv_paths = [
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn45-final-w-ML-PM.parquet",
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn46-final-w-ML-PM.parquet",
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn49-final-w-ML-PM.parquet",
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn62-final-w-ML-PM.parquet",
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn67-final-w-ML-PM.parquet",
        "C:/Users/zxiong/Desktop/Olin/Air Partners/downsampled/sn72-final-w-ML-PM.parquet",
    ]

    flight_csv_dir = "C:/dev/Air Partners/Data Analysis/data/flights/raw/"

    processed_flight_dir = "C:/dev/Air Partners/Data Analysis/data/flights/processed/"

    final_flights = "C:/dev/Air Partners/Data Analysis/data/flights/final/combined_flights.parquet"

else: # if not Ian or Lauren, feel free to make a copy of this and change the file names below:
    raw_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn45-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn46-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn49-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn62-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn67-final-w-ML-PM.csv",
        "C:/dev/Air Partners/Data Analysis/data/east_boston/sn72-final-w-ML-PM.csv",
    ]

    processed_csv_paths = [
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn45-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn46-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn49-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn62-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn67-final-w-ML-PM.parquet",
        "C:/dev/Air Partners/Data Analysis/data/parquet/sn72-final-w-ML-PM.parquet",
    ]

    flight_csv_dir = "C:/dev/Air Partners/Data Analysis/data/flights/raw/"

    processed_flight_dir = "C:/dev/Air Partners/Data Analysis/data/flights/processed/"

    final_flights = "C:/dev/Air Partners/Data Analysis/data/flights/final/combined_flights.parquet"