from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
import math
import numpy as np
from sigfig import round
import datetime
# from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from data_importer import DataImporter


# Parent class for TimeSeries, BarChart, CorrelationPlot, and PolarPlot
class GraphFrame():

    # define HTML styles for text and dropdown menus. Use this to change font size, alignment, etc.
    text_style = {
        # "display": "inline-block", # if you take this out, all successive elements will be displayed on separate lines
        # "display": "flex",
        "display": "inline-block",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",
        "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-right": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "font-size" : "24px",
        "font-family": "Arial",
        # "line-height": "0%", # helps reduce the line spacing
    }

    text_style_explanation = {
        "display": "inline-block",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",
        "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-right": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "font-size" : "18px",
        "font-family": "Times New Roman, Serif",
        "background-color": "#F2F2F2"
    }

    # text_style_bold = text_style_explanation |

    dropdown_style = {
        # "display": "inline-block",
        # "display": "flex",
        "display": "inline-block",
        "width": "400px",
        # "height": "30px",
        "margin-left": "5px",
        "margin-right": "15px",
        "font-size": "20px",
        "font-family": "Arial",
        # "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style_2 = {
        # "display": "block",
        # "display": "flex",
        "display": "inline-block",
        "width": "400px",
        # "height": "30px",
        # "margin-right": "10px",
        # "margin-left": "10px",
        "font-size": "20px",
        "font-family": "Arial",
        # "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style_header = dropdown_style_2 | {"font-size": "20px", "font-weight": "bold"}
    # dropdown_style_header["font-size"] = "20px"
    # dropdown_style_header["font-weight"] = "bold"

    date_picker_style = {
        # "display": "inline-block",
        # "display": "flex",
        "display": "inline-block",
        # "width": "200px", # not used or doesn't work
        # "height": "40px",
        "margin-left": "10px",
        # "font-family": "Arial", # not used or doesn't work
        # "line-height": "0%", # helps reduce the line spacing
    }

## //////////////////////////////////////////////////////// ##
##  Reused HTML components

    def date_picker(self, id = 'date-picker-range'):
        return \
            dcc.DatePickerRange(
                display_format = 'MM/DD/Y',
                min_date_allowed = datetime.date(2019, 9, 8),
                max_date_allowed = datetime.date(2021, 3, 5),
                start_date = datetime.date(2019, 12, 1), # default value
                end_date = datetime.date(2019, 12, 31), # default value
                id = self.get_id(id),
            )

    def sensor_picker(self, id = 'which-sensor'):
        return \
            dcc.Dropdown(
                options = [{'label': self.sensor_locations[name], 'value': i} for i, name in enumerate(self.sensor_names)],
                # note: in order to set the default value, you have to set value = {the VALUE you want}.
                # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
                value = 0, # default value
                id = self.get_id(id), # javascript id, used in @app.callback to reference this element, below
                clearable = False, # prevent users from deselecting all sensors
                style = self.dropdown_style | {"width": "350px"}
            )


    def pollutant_picker(self, my_id = 'pollutant-dropdown', multi = True):
        return \
            dcc.Dropdown(
                options = [{'label': var_name, 'value': var} for var, var_name in
                    list(self.particles_vars.items()) + list(self.gas_vars.items()) + list(self.flight_vars.items())],
                value='pm25.ML',

                multi = multi,
                id = self.get_id(my_id),

                style = self.dropdown_style_2 | {"width": ("800px" if multi else "350px")}
            )

    def normalize_switch(self, id = 'normalize-height'):
        return \
            daq.BooleanSwitch(
                id = self.get_id(id),
                on = False,
                style = {'display': 'block'},
                label = "Ignore units",
                labelPosition = "top"
            )

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
        # "bin0": "0.3-0.5μm particles (bin 0)",
        # "bin1": "0.5-0.7μm particles (bin 1)",
        # "bin2": "0.7-1.0μm particles (bin 2)",
        # "bin3": "1.0-2.5μm particles (bin 3)",
        # "bin4": "2.5-10μm particles (bin 4)",
        # "bin5": "10+ μm particles (bin 5)",
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

## //////////////////////////////////////////////////////// ##
##  Sensor locations and names
    sensor_locations_long = {
        "sn45": "Orient Heights (West end); 65 St Andrew Road, East Boston",
        "sn46": "Jeffries Point (Maverick end); 198 Everett Street, East Boston",
        "sn49": "Winthrop (Maze); 3 Elmer Ave, Winthrop",
        "sn62": "Jeffries Point (Airport end); 551 Sumner EB",
        "sn67": "Point Shirley; 86 bay View Ave, Winthrop",
        "sn72": "Orient Heights (East end); 21 Anna Voy, EB",
    }

    sensor_locations = {
        "sn45": "Orient Heights (West end)",
        "sn46": "Jeffries Point (Maverick end)",
        "sn49": "Winthrop",
        "sn62": "Jeffries Point (Airport end)",
        "sn67": "Point Shirley",
        "sn72": "Orient Heights (East end)",
    }

    def __init__(self, app, data_importer: DataImporter, id_num, chart_type = 0, initial_display_status = 'block') -> None:
        self.app = app
        self.data_importer = data_importer
        self.sensor_names = self.data_importer.get_all_sensor_names()
        self.id_num = id_num
        self.frame = self.get_layout(initial_display_status)
        self.add_graph_callback()

    def get_id(self, id_str):
        return id_str + "-" + str(self.id_num)

    def get_layout(self, initial_display_status):
        children = []

        children.append(
                html.Details(
                    children = self.get_explanation(),
                    open = True,
                    id = self.get_id("explanation"),
                    style = self.text_style_explanation,
                )
        )

        children.append(
            html.Div(
                self.get_html(),
                style = self.text_style,
            )
        )

        children.append(
            html.Hr(style = {'border': '8px solid black'})
        )

        return_div = \
        html.Div(
            children = children,
            style = self.text_style | {'display': initial_display_status},
            id = self.get_id('frame')
        )

        return return_div

    def get_explanation(self):
        print("This GraphFrame method should be overwritten by the child class.")
        return None

    def get_html(self):
        print("This GraphFrame method must be overwritten by the child class.")
        # assert(False)

    def add_graph_callback(self):
        print("This GraphFrame method must be overwritten by the child class.")
        # assert(False)

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

    def as_float(self, x):
        # handle non-numeric data
        if not isinstance(x, (int, float)) or math.isinf(x) or math.isnan(x):
            return np.nan

        # format the number with +/- sign ('+'), commas in the thousands place (','), no sig figs ('.0'), and as a percentage ('%')
        return format(x, '.1f')
