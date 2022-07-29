def my_data_directory():
    """
    After reading this document and following the instructions, there is one line you need to edit at the very end of the file.

    Before you start, choose a location on your computer to store your raw and processed data, and create a file system that
    looks like this:

        📦data
        ┣ 📂east_boston
        ┃ ┣ 📂processed
        ┃ ┣ 📂raw
        ┃ ┗ 📂stats
        ┗ 📂flights
        ┃ ┣ 📂final
        ┃ ┣ 📂processed
        ┃ ┗ 📂raw

    IMPORTANT: Set the last line in this file to return the file location of the topmost data directory.

    Now download the raw data from _____.
    Move the raw CSV files you downloaded into the respective `raw` folders for raw East Boston data and raw flight data.
    Your new file system should look like this:

        📦data
        ┣ 📂east_boston
        ┃ ┣ 📂processed
        ┃ ┣ 📂raw
        ┃ ┃ ┣ 📜sn45-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn46-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn49-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn62-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn67-final-w-ML-PM.csv
        ┃ ┃ ┗ 📜sn72-final-w-ML-PM.csv
        ┃ ┗ 📂stats
        ┗ 📂flights
        ┃ ┣ 📂final
        ┃ ┣ 📂processed
        ┃ ┗ 📂raw
        ┃ ┃ ┣ 📜finalflightdf.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - AUG 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - DEC 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JAN 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JULY 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JUNE 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAR 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAY 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - NOV 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - OCT 2020.csv
        ┃ ┃ ┗ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - SEP 2020.csv

    Once you run `dash_layout1.py`, it will populate the 📂processed, 📂final, and 📂stats folders with processed data, so that
    it looks like this:

        📦data
        ┣ 📂east_boston
        ┃ ┣ 📂processed
        ┃ ┃ ┣ 📜sn45-final-w-ML-PM.parquet
        ┃ ┃ ┣ 📜sn46-final-w-ML-PM.parquet
        ┃ ┃ ┣ 📜sn49-final-w-ML-PM.parquet
        ┃ ┃ ┣ 📜sn62-final-w-ML-PM.parquet
        ┃ ┃ ┣ 📜sn67-final-w-ML-PM.parquet
        ┃ ┃ ┗ 📜sn72-final-w-ML-PM.parquet
        ┃ ┣ 📂raw
        ┃ ┃ ┣ 📜sn45-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn46-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn49-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn62-final-w-ML-PM.csv
        ┃ ┃ ┣ 📜sn67-final-w-ML-PM.csv
        ┃ ┃ ┗ 📜sn72-final-w-ML-PM.csv
        ┃ ┗ 📂stats
        ┃ ┃ ┗ 📜east_boston_summary_stats.parquet
        ┗ 📂flights
        ┃ ┣ 📂final
        ┃ ┃ ┗ 📜combined_flights.parquet
        ┃ ┣ 📂processed
        ┃ ┃ ┣ 📜finalflightdf.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2021.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - AUG 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - DEC 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JAN 2021.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JULY 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JUNE 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAR 2021.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAY 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - NOV 2020.parquet
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - OCT 2020.parquet
        ┃ ┃ ┗ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - SEP 2020.parquet
        ┃ ┗ 📂raw
        ┃ ┃ ┣ 📜finalflightdf.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - APR 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - AUG 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - DEC 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JAN 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JULY 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - JUNE 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAR 2021.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - MAY 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - NOV 2020.csv
        ┃ ┃ ┣ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - OCT 2020.csv
        ┃ ┃ ┗ 📜Olin_April 2020-May 2021_Flight_Data_Set.xlsx - SEP 2020.csv

    After you have run `dash_layout1.py` successfully one time, you can delete the raw datasets if you want to.
    However although it is recommended that you keep the raw data in case you ever change the processing algorithm or want to
    add more data; in this case you will need to delete all the files inside of 📂processed, 📂final, and 📂stats and re-run
    `dash_layout1.py` to regenerate the processed files.

    One more thing:
    The file you are currently editing is included in the .gitignore in this GitHub repo. So you can modify this file and still
    commit your changes to other parts of the code base; you will not mess up anyone else's data loading process by modifying
    this file to match your personal data directory.

    Good luck, and have fun!
    """

    # set the following line to return the topmost data directory
    # remember to use forward slashes (/) instead of backslashes (\) even if on a Windows system
    return "C:/.../data/"