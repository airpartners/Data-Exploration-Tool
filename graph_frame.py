from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import math
import numpy as np
from sigfig import round
# import datetime
# from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from data_importer import DataImporter


# Parent class for TimeSeries, BarChart, CorrelationPlot, and PolarPlot
class GraphFrame():

    # define HTML styles for text and dropdown menus. Use this to change font size, alignment, etc.
    text_style = {
        # "display": "inline-block", # if you take this out, all successive elements will be displayed on separate lines
        "display": "flex",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",
        "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "font-size" : "30px",
        "font-family": "Arial",
        # "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style = {
        # "display": "inline-block",
        "display": "flex",
        "width": "200px",
        # "height": "30px",
        "margin-left": "10px",
        "font-size": "20px",
        "font-family": "Arial",
        # "line-height": "0%", # helps reduce the line spacing
    }

    date_picker_style = {
        # "display": "inline-block",
        "display": "flex",
        # "width": "200px", # not used or doesn't work
        # "height": "40px",
        "margin-left": "10px",
        # "font-family": "Arial", # not used or doesn't work
        # "line-height": "0%", # helps reduce the line spacing
    }

## /////////////////////////////////////////////////// ##
## Variables

    meteorology_vars = {
        "temp_manifold": "Temperature (°C)",
        "rh_manifold": "Humidity (%)",
        # "pressure": "Pressure (Pa)",
        # "noise": "Noise (dB)",
        "ws": "Wind Speed (m/s)",
        'South-West': "Takeoffs/Landings per hour (SouthWest Operation)",
        'North-West': "Takeoffs/Landings per hour (NorthWest Operation)",
        'North-East': "Takeoffs/Landings per hour (NorthEast Operation)",
    }
    gas_vars = {
        "co.ML": "CO (ppb)",
        "correctedNO": "NO (ppb)",
        "no2.ML": "NO2 (ppb)",
        "o3.ML": "O3 (ppb)",
    }
    particles_vars = {
        "bin0": "0.3-0.5μm particles (bin 0)",
        "bin1": "0.5-0.7μm particles (bin 1)",
        "bin2": "0.7-1.0μm particles (bin 2)",
        "bin3": "1.0-2.5μm particles (bin 3)",
        "bin4": "2.5-10μm particles (bin 4)",
        "bin5": "10+ μm particles (bin 5)",
        "pm1.ML": "PM1 (μg/m^3)",
        "pm25.ML": "PM2.5 (μg/m^3)",
        "pm10.ML": "PM10 (μg/m^3)",
    }
    flight_vars = {
        # 'Opr': "Arrival/Departure",
        # 'RW_group': "Runway Operation",
        # 'count': "Flights",
        # 'A': "Arrivals",
        # 'D': "Departures",
        'South-West': "Takeoffs/Landings per hour (SouthWest Operation)",
        'North-West': "Takeoffs/Landings per hour (NorthWest Operation)",
        'North-East': "Takeoffs/Landings per hour (NorthEast Operation)",
    }

    # | is the python syntax for adding or "merging" two dictionaries
    all_vars = meteorology_vars | gas_vars | particles_vars | flight_vars

    def __init__(self, app, data_importer: DataImporter, id_num, chart_type = 0, initial_display_status = 'block') -> None:
        self.app = app
        self.data_importer = data_importer
        self.id_num = id_num
        self.frame = self.get_layout(initial_display_status)
        self.add_graph_callback()

    def get_id(self, id_str):
        return id_str + "-" + str(self.id_num)

    def get_layout(self, initial_display_status):
        return \
        html.Div(
            children = self.get_html() + [html.Hr(style = {'border': '3px solid black'})],
            style = {'display': initial_display_status},
            id = self.get_id('frame')
        )

    def get_html(self):
        print("This GraphFrame method must be overwritten by the child class.")
        assert(False)

    def add_graph_callback(self):
        print("This GraphFrame method must be overwritten by the child class.")
        assert(False)

    # methods for filtering and post-processing data for graphing
    def filter_by_date(self, df, start_date, end_date):
        if start_date and end_date:
            return \
                df[
                    (df.index.date >= pd.Timestamp(start_date).date()) &
                    (df.index.date <= pd.Timestamp(end_date).date()  )
                    # (df["timestamp_local"].dt.date >= pd.Timestamp(start_date).date()) &
                    # (df["timestamp_local"].dt.date <= pd.Timestamp(end_date).date()  )
                ]
        # else:
        return df

    def filter_by_wind_direction(self, df, wind_direction):
        if wind_direction is not None:
            return df[ df["wind_direction_cardinal"] == wind_direction ]
            # return df[ df["wind_direction_cardinal", "my_mode"] == wind_direction ]
        # else:
        return df

    def normalize_height(self, df, max_val = 1, do_it = True):
        if not do_it:
            return df
        return df / df.select_dtypes('number').max() * max_val

    def as_percent(self, x):
        # handle non-numeric data
        if not isinstance(x, (int, float)) or math.isinf(x) or math.isnan(x):
            return np.nan

        # format the number with +/- sign ('+'), commas in the thousands place (','), no sig figs ('.0'), and as a percentage ('%')
        return format(round(x - 1, sigfigs = 2), '+,.0%')
