import os
from my_data_directory import my_data_directory

root = my_data_directory()

# raw_csv_paths = [
#     os.path.join(root, "east_boston/raw/sn45-final-w-ML-PM.csv"),
#     os.path.join(root, "east_boston/raw/sn46-final-w-ML-PM.csv"),
#     os.path.join(root, "east_boston/raw/sn49-final-w-ML-PM.csv"),
#     os.path.join(root, "east_boston/raw/sn62-final-w-ML-PM.csv"),
#     os.path.join(root, "east_boston/raw/sn67-final-w-ML-PM.csv"),
#     os.path.join(root, "east_boston/raw/sn72-final-w-ML-PM.csv"),
# ]

raw_sensor_dir = os.path.join(root, "east_boston/raw/")
processed_sensor_dir = os.path.join(root, "east_boston/processed/")

# processed_csv_paths = [
#     os.path.join(root, "east_boston/processed/sn45-final-w-ML-PM.parquet"),
#     os.path.join(root, "east_boston/processed/sn46-final-w-ML-PM.parquet"),
#     os.path.join(root, "east_boston/processed/sn49-final-w-ML-PM.parquet"),
#     os.path.join(root, "east_boston/processed/sn62-final-w-ML-PM.parquet"),
#     os.path.join(root, "east_boston/processed/sn67-final-w-ML-PM.parquet"),
#     os.path.join(root, "east_boston/processed/sn72-final-w-ML-PM.parquet"),
# ]

stats_file = os.path.join(root, "east_boston/stats/east_boston_summary_stats.parquet")

flight_csv_dir = os.path.join(root, "flights/raw/")

processed_flight_dir = os.path.join(root, "flights/processed/")

final_flights = os.path.join(root, "flights/final/combined_flights.parquet")