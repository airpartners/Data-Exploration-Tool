from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.dash import no_update
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import math
import numpy as np
from sigfig import round
import datetime
# from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from data_importer import DataImporter
import css


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
        "font-size" : "18px",
        "font-family": "Arial",
        "padding-right": "15px",
        "line-height": "2", # line spacing
    }

    text_style_explanation = {
        "display": "inline-block",
        # "transform": "translateY(0%)", # vertical alignment
        # "position": "relative",

        # 'margin' affects the size of the bounding box
        "margin-left": "7px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-right": "40px", # adds a horizontal space between dropdowns menus and next chunk of text
        "margin-top": "20px",
        "margin-bottom": "20px",
        "border-radius": "5px", # rounded corners!

        # 'padding' affects the positioning of the text withing the bounding box
        "padding-left": "30px",
        "padding-right": "30px",
        "padding-top": "0px",
        "padding-bottom": "0px",

        # font size and color
        "font-size" : "16px",
        "font-family": "Arial",
        "color": css.color_scheme["explanation_text"],
        "background-color": css.color_scheme["explanation_background"],

        "line-height": "1.6", # line spacing
    }

    filter_picker_style = text_style | {"display": "inline"}

    # text_style_bold = text_style_explanation |

    dropdown_style = {
        "display": "inline-block",
        "width": "50%",
        "height": "32px",
        "margin-left": "5px",
        "margin-right": "15px",
        "font-size": "17px",
        "font-family": "Arial",
        "vertical-align": "middle",
        # "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style_2 = dropdown_style | {
        "width": "50%",
        # "margin-right": "10px",
        # "margin-left": "10px",
        "overflow-y": "visible",
        "max-height": "100%",
    }

    dropdown_style_header = dropdown_style_2 | {
        "font-size": "20px",
        "font-weight": "bold",
        }

    date_picker_style = {
        # "display": "inline-block",
        # "display": "flex",
        "display": "inline-block",
        # "width": "200px", # not used or doesn't work
        "height": "32px",
        "margin-left": "10px",
        "font-size": "18px",
        "vertical-align": "middle",
        "overflow-y": "visible",
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
                start_date = datetime.date(2019, 9, 8), # default value
                end_date = datetime.date(2021, 3, 5), # default value
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
                style = self.dropdown_style | {"width": "220px"}
            )

    def wind_direction_picker(self, my_id = 'wind-direction-picker'):
        return \
            dcc.Dropdown(
                options = [
                    {'label': 'North',     'value': 'N'},
                    {'label': 'Northeast', 'value': 'NE'},
                    {'label': 'East',      'value': 'E'},
                    {'label': 'Southeast', 'value': 'SE'},
                    {'label': 'South',     'value': 'S'},
                    {'label': 'Southwest', 'value': 'SW'},
                    {'label': 'West',      'value': 'W'},
                    {'label': 'Northwest', 'value': 'NW'},
                ],
                clearable = True,
                value = None,
                multi = True,
                id = self.get_id(my_id),
                style = self.dropdown_style_2
            )

    def pollutant_picker(self, my_id = 'pollutant-dropdown', multi = True, show_flights = True):
        vars = self.particles_vars + self.gas_vars
        if show_flights:
            vars.extend(self.flight_vars)

        return \
            dcc.Dropdown(
                options = vars,
                value="PM2.5 (μg/m^3)",

                multi = multi,
                id = self.get_id(my_id),

                style = (self.dropdown_style_2 | {"width": "500px"}) if multi else (self.dropdown_style | {"width": "200px"})
            )

    def correlation_xvar(self, id = 'x-axis'):
        return \
            dcc.Dropdown(
                options = self.all_vars,
                value='Humidity (%)',

                id=self.get_id(id),
                style = self.dropdown_style | {"width": "340px"}
            )

    def correlation_yvar(self, id = 'y-axis'):
        return \
            dcc.Dropdown(
                options = self.all_vars,
                value='O3 (ppb)',
                multi = True,

                id=self.get_id(id),
                style = self.dropdown_style | {"width": "340px"}
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

    def filter_picker(self, my_id = 'filter-set'):
        vars = self.meteorology_vars + self.flight_vars

        filter_sliders = []
        graph_inputs = []
        graph_inputs_state = []
        dropdown_targets = []
        sensor_picker_callback_targets = []

        for var in vars:
            var_name = var

            filter_id = self.get_id('filter-by-' + var)
            filter_display_id = self.get_id('show-filter-by-' + var)

            filter_sliders.append(
                html.Div(
                    children = [
                        var_name + ":",
                        html.Div(
                            dcc.RangeSlider(
                                min = 0,
                                max = 100,
                                step = 1,
                                marks = None,
                                value = [0, 100],
                                id = filter_id,
                                tooltip = {"placement": "bottom", "always_visible": True},
                            ),
                            style = {'display': 'inline', 'width': '50%'},
                        )
                    ],
                    style = self.filter_picker_style | {'display': 'none'},
                    id = filter_display_id
                )
            )
            print(f"I am a RangeSlider, and I have an id of {filter_id}")

            graph_inputs.append(Input(filter_id, "value"))
            graph_inputs_state.append(State(filter_id, "value"))

            dropdown_targets.append(Output(filter_display_id, "style"))
            dropdown_targets.append(Output(filter_id, "value"))
            dropdown_targets.append(Output(filter_id, "min"))
            dropdown_targets.append(Output(filter_id, "max"))

            sensor_picker_callback_targets.append(Output(filter_id, "value"))
            sensor_picker_callback_targets.append(Output(filter_id, "min"))
            sensor_picker_callback_targets.append(Output(filter_id, "max"))

        return_var = \
            html.Div(
                children = [
                    dcc.Store(
                        data = {},
                        id = self.get_id('filter-callback-data')
                    ), # used for storing data; not displayed
                    dcc.Dropdown(
                        options = [{'label': var, 'value': var} for var in vars],
                        value = 'blankenship',

                        multi = True,
                        id = self.get_id(my_id),

                        style = (self.dropdown_style_2 | {"width": "100%"})
                    ),
                    *filter_sliders,
                ]
            )

        @self.app.callback(
            *dropdown_targets,
            Input(self.get_id(my_id), 'value'),
            Input(self.get_id('which-sensor'), 'value'),
            prevent_initial_call = True
        )
        def dropdown_callback(vars_to_show, sensor):
            if not vars_to_show:
                vars_to_show = []

            outputs_list = []
            for var in vars:
                var_min = int(self.data_importer.df_stats[self.sensor_names[sensor]]["min"][self.var_col_names[var]])
                var_max = int(self.data_importer.df_stats[self.sensor_names[sensor]]["max"][self.var_col_names[var]])
                if var in vars_to_show:
                    outputs_list.append(self.filter_picker_style | {'display': 'inline'})
                    outputs_list.append(no_update)
                else:
                    outputs_list.append(self.filter_picker_style | {'display': 'none'})
                    outputs_list.append([var_min, var_max])
                # also:
                outputs_list.append(var_min)
                outputs_list.append(var_max)

            return tuple(outputs_list)

        @self.app.callback(
            Output(self.get_id('filter-callback-data'), "data"),
            *graph_inputs,
            prevent_initial_call = True
        )
        def slider_callback(*var_ranges):
            return {var: range for var, range in zip(vars, var_ranges)}

        # now have filter_picker() return the div with all the RangeSliders after all the callbacks have been added
        return return_var

## /////////////////////////////////////////////////// ##
## Graph Styling Functions
    def update_background_colors(self, fig, is_polar = False):
        if not is_polar:
            fig.update_layout(
                paper_bgcolor="rgb(0,0,0,0)",
                legend = dict(bgcolor = css.color_scheme["main_background"]),
                plot_bgcolor = "#FFFFFF",
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E3E3E3')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E3E3E3')
        else:
            fig.update_polars(
                bgcolor = "#FFFFFF",
                angularaxis_gridcolor = "#E3E3E3",
                radialaxis_gridcolor = "#E3E3E3",
                )

## /////////////////////////////////////////////////// ##
## Variables

    meteorology_vars = [
        "Temperature (°C)",
        "Humidity (%)",
        # "pressure": "Pressure (Pa)",
        # "noise": "Noise (dB)",
        "Wind Speed (m/s)",
        # 'South-West': "Takeoffs/Landings per hour (SouthWest Operation)",
        # 'North-West': "Takeoffs/Landings per hour (NorthWest Operation)",
        # 'North-East': "Takeoffs/Landings per hour (NorthEast Operation)",
    ]
    gas_vars = [
        "CO (ppb)",
        "NO (ppb)",
        "NO2 (ppb)",
        "O3 (ppb)",
    ]
    particles_vars = [
        # "bin0": "0.3-0.5μm particles (bin 0)",
        # "bin1": "0.5-0.7μm particles (bin 1)",
        # "bin2": "0.7-1.0μm particles (bin 2)",
        # "bin3": "1.0-2.5μm particles (bin 3)",
        # "bin4": "2.5-10μm particles (bin 4)",
        # "bin5": "10+ μm particles (bin 5)",
        "PM1 (μg/m^3)",
        "PM2.5 (μg/m^3)",
        "PM10 (μg/m^3)",
    ]
    flight_vars = [
        # 'Opr': "Arrival/Departure",
        # 'RW_group': "Runway Operation",
        # 'count': "Flights",
        # 'A': "Arrivals",
        # 'D': "Departures",
        # # #
        # 'South-West': "Takeoffs/Landings per hour (SouthWest Operation)",
        # 'North-West': "Takeoffs/Landings per hour (NorthWest Operation)",
        # 'North-East': "Takeoffs/Landings per hour (NorthEast Operation)",
        # # #
        "Adverse Takeoffs/Landings",
        "Total Takeoffs/Landings",
    ]

    all_vars = meteorology_vars + gas_vars + particles_vars + flight_vars

    var_col_names = {
        "Temperature (°C)": "temp_manifold",
        "Humidity (%)": "rh_manifold",
        "Wind Speed (m/s)": "ws",
        "CO (ppb)": "co.ML",
        "NO (ppb)": "correctedNO",
        "NO2 (ppb)": "no2.ML",
        "O3 (ppb)": "o3.ML",
        "PM1 (μg/m^3)": "pm1.ML",
        "PM2.5 (μg/m^3)": "pm25.ML",
        "PM10 (μg/m^3)": "pm10.ML",
        "Adverse Takeoffs/Landings": "adverse_flight_count",
        "Total Takeoffs/Landings": "count",
        "wind_direction_cardinal": "wind_direction_cardinal",
    }


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

    def filter_by_var(self, df, var, var_min, var_max):
        if not self.var_col_names[var] in df.columns:
            raise ValueError(f"Variable {var} is not in the dataframe. Try one of {df.columns} instead.")
        if var_min is not None and var_max is not None:
            return \
                df[
                    (df[self.var_col_names[var]] >= var_min) &
                    (df[self.var_col_names[var]] <= var_max)
                ]
        # else:
        return df

    def filter_by_wind_direction(self, df, wind_direction):
        if wind_direction is None or wind_direction == []:
            return df
        if not isinstance(wind_direction, list):
            wind_direction = [wind_direction]
        return df[ df[self.var_col_names["wind_direction_cardinal"]].isin(wind_direction) ]

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
