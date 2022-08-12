from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sigfig import round
from graph_frame import GraphFrame
from css import CSS

class BarChartGraph(GraphFrame):

    def get_html(self):
        """
        Defines the structure of barchart in html

        The filter message and dropdown menus are defined as html.Div() arguments, and the graph will be updated in the
        add_graph_callback(): update_figure() function below

        """
        return \
            [
                "At ",
                self.sensor_picker(), # calling the sensor dropdown menu defined in graph_frame.py
                "what were the average pollution levels over the period of ",
                self.date_picker(), # calling the date range dropdown menu defined in graph_frame.py
                "when the wind was blowing from the ",
                self.wind_direction_picker(my_id = 'wind-direction-picker'),

                html.Div(
                    ", relative to the baseline average",
                    id = self.get_id('relative-text'),
                    style = CSS.text_style
                ),

                "? Filter by: ",
                self.filter_picker(),
                self.normalize_switch(my_id = 'normalize-height', is_barchart = True),

                dcc.Graph(
                    id = self.get_id('bar-chart-graph')
                ),
            ]

    def add_graph_callback(self):
        """
        Defines and returns all the text and calendar plot features

        This function consists of two sections:
        - @self.app.callback that contains all the input and output callback functions;
        - the main plotting function update_figure() that takes sensor and pollutant selections from the filter message dropdowns(defined above
         as html.Div() arguments in get_html() function) to choose the demanded dataset and/or select the demanded column of dataset to plot on the graph

        """

        @self.app.callback(
            # the id of the graph lines up with the id argument in dcc.Graph defined in get_html() function
            Output(self.get_id('bar-chart-graph'), 'figure'),
            Output(self.get_id('relative-text'), 'style'),
            Input( self.get_id('which-sensor'), 'value'),
            Input( self.get_id('date-picker-range'), 'start_date'),
            Input( self.get_id('date-picker-range'), 'end_date'),
            Input( self.get_id('normalize-height'), 'on'),
            Input(self.get_id('wind-direction-picker'), 'value'),
            Input(self.get_id('filter-callback-data'), 'data'),
        )
        def update_figure(which_sensor, start_date, end_date, normalize_height, wind_direction, var_ranges):
            """
            Main plotting function:
            - selects and processes the dataset
            - then makes the plot

            """
            # calling dataset from data_importer and make it a pandas dataframe
            # df = self.data_importer.get_data_by_sensor(which_sensor, numeric_only = True)
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # calling the statistic data that mainly includes the mean of the entire dataset
            df_stats = self.data_importer.df_stats

            # extract sensor name from the function input which_sensor returned from the sensor dropdown menu
            sensor_name = self.data_importer.get_all_sensor_names()[which_sensor]

            # rename the columns in df_stats to something more understandable
            df_stats = df_stats.rename(index={
                "pm10.ML": "PM10 (μg/m^3)",
                "pm25.ML": "PM2.5 (μg/m^3)",
                "pm1.ML": "PM1 (μg/m^3)",
                "co.ML": "CO (ppb)",
                "correctedNO": "NO (ppb)",
                "no2.ML": "NO2 (ppb)",
                "o3.ML": "O3 (ppb)",
                "temp_manifold": "Temperature (°C)",
                "rh_manifold": "Humidity (%)",
                "ws": "Wind Speed (m/s)",
                "adverse_flight_count": "Adverse Takeoffs/Landings",
                "count": "Total Takeoffs/Landings",
            })

            # filter by timestamp and wind direction
            df = self.filter_by_date(df, start_date, end_date)

            for var, var_range in var_ranges.items():
                df = self.filter_by_var(df, var, var_range[0], var_range[1])

            df = self.filter_by_wind_direction(df, wind_direction)

            # rename the columns in the dataset of the selected sensor
            df = df.rename(columns={
                "pm10.ML": "PM10 (μg/m^3)",
                "pm25.ML": "PM2.5 (μg/m^3)",
                "pm1.ML": "PM1 (μg/m^3)",
                "co.ML": "CO (ppb)",
                "correctedNO": "NO (ppb)",
                "no2.ML": "NO2 (ppb)",
                "o3.ML": "O3 (ppb)",
                "temp_manifold": "Temperature (°C)",
                "rh_manifold": "Humidity (%)",
                "ws": "Wind Speed (m/s)",
                "adverse_flight_count": "Adverse Takeoffs/Landings",
                "count": "Total Takeoffs/Landings",
            })

            # extract the stats data based on the sensor name
            stat_type = "mean"
            if stat_type == "mean":
                filtered_stat = df.mean(axis = 0)
                normalized_stat = filtered_stat / df_stats[sensor_name, "mean"]
            elif stat_type == "median":
                filtered_stat = df.median(axis=0)
                normalized_stat = filtered_stat / df_stats[sensor_name, "median"]
            else:
                raise KeyError("Unsupported aggregation function. Try 'mean' or 'median' instead.")

            # if normalize_height(ignore units button on the html page) is unchecked, undo the division by df_stats
            if normalize_height:
                normalized_text = normalized_stat[self.gas_vars].apply(self.as_percent)
            else:
                normalized_stat = filtered_stat
                normalized_text = normalized_stat[self.gas_vars].apply(self.as_float)

            # remove infinite values
            normalized_stat.replace([np.inf, -np.inf], np.nan, inplace=True)

            # round the stats data to 2 decimal places
            normalized_stat = normalized_stat.round(2)

            # create subplots
            fig = go.Figure()
            titles = ['Meteorology Data', 'Gas Pollutants', 'Particle Pollutants']
            fig = make_subplots(rows = 1, cols = 3, subplot_titles = titles)

            def add_sub_barchart(vars, col, color):
                """
                Defines and returns the filter text style and specific features of the barchart graph

                """
                # define the text shown on each bar and the x-axis variable according to the normalizing data option
                if normalize_height:
                    normalized_text = normalized_stat[vars].apply(self.as_percent)
                else:
                    normalized_text = normalized_stat[vars].apply(self.as_float)

                # define the format of each individual barchart subplot
                fig.add_trace(
                    go.Bar(
                        x = list(vars),
                        y = normalized_stat[vars],
                        text = normalized_text,
                        marker_color = px.colors.qualitative.T10[color],
                        hovertemplate = '<b>%{x}</b> %{text}',
                        name = titles[col-1] ,
                        showlegend = False
                    ),
                    row = 1,
                    col = col
                )

            # make 3 subplots in the same format defined above with different input arguments
            add_sub_barchart(self.meteorology_vars + self.flight_vars, 1, color = 0)
            add_sub_barchart(self.gas_vars, 2, color = 2)
            add_sub_barchart(self.particles_vars, 3, color = 5)


            # remove the awkward whitespace where the title used to be
            fig.update_layout(margin = {'t': 20})
            self.update_background_colors(fig)


            # mark the line y=1 i.e. when filtered mean/median equals entire dataset mean/median
            if normalize_height:
                fig.add_hline(y=1, line_width=3, line_dash="dot", line_color="navy", annotation=dict(text='Average'))

            if normalize_height:
                relative_text_style = CSS.text_style
            else:
                relative_text_style = CSS.text_style | {'display': 'none'}

            return fig, relative_text_style