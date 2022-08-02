def my_data_directory():
    """
    Action items to look out for as you follow these instructions:
    * There is one line you need to edit at the very end of the file.
    * There is also a command that we highly recommend you run to avoid overwriting this file in the GitHub repo:
      (in your command prompt/terminal, navigate to the directory for this repo, then type):
      git update-index --skip-worktree my_data_directory.py

    Before you start, choose a location on your computer to store your raw and processed data, and create a file system that
    looks like this (you just need to create 9 folders on your computer, with this structure):

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

    Now download the raw data from the following sources:
    * East Boston sensor data: https://www.dropbox.com/sh/g2ius57olxnv47y/AADGkZNQtheD_qxbR17fsHPca?dl=0
    * Flight data set #1: https://drive.google.com/file/d/1Dpxr71i97ktTbSn2OxsrzduH2EAr5HeF/view
    * Flight data set #2: https://docs.google.com/spreadsheets/d/1WVQCzpq_QVtPJT4BSEq30PJzRrDLvqC5/edit#gid=1925802693
        (Yes, you will have to download each month separately)

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

    IMPORTANT:
    If you edit this file right now and then commit your changes to the repo, you will potentially mess up someone else's version
    by making their system look in a different place for their files. To avoid committing your changes to this file, use the
    following git command (in your command prompt/terminal, navigate to the directory for this repo, then type):
    git update-index --skip-worktree my_data_directory.py

    Good luck, and have fun!
    """

    # set the following line to return the topmost data directory
    # remember to use forward slashes (/) instead of backslashes (\) even if on a Windows system
    # return "C:/.../data"
    return "C:/dev/Air Partners/Data Analysis/data"