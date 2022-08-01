from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sigfig import round
from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from graph_frame import GraphFrame

class BarChartGraph(GraphFrame):
    def get_explanation(self):
        return [
            html.P([html.B("Bar Chart:"), " Shows a summary of the pollution levels of multiple fine particle categories. ",
            "Select a date range between September 2019 and April 2020. The bar chart shows the average toxic gas concentrations in parts per billion (ppb) and particle concentrations in micrograms per cubic meter (μg/m^3) over the date range that is selected. ",
            ]),
            html.P(["To compare the values to the average pollutant concentration for the entire deployment period of that sensor, use the ", html.B('"Ignore units"'), " button. ",
            "When ", html.B('"Ignore units"'), " is selected, the bar chart shows the standardized data that is calculated by dividing the mean particle concentration during the selected time slot by the 2-year mean concentration of the same particles measured from the same sensor. "
            ]),
        ]

    def get_html(self):
        """
        Defines the structure of barchart in html by calling the dropdown the functions in add_graph_callback()

        """

        # children = ...
        return \
            [
                "At ",
                self.sensor_picker(),
                "what were the average pollution levels over the period of ",
                self.date_picker(), #apply filter to select time range
                html.Div(
                    ", relative to the baseline average",
                    id = self.get_id('relative-text'),
                    style = self.text_style
                ),
                "?",
                # html.Div(
                #     [
                #         #choose to plot either mean or median datasets at one time
                #         dcc.Dropdown(
                #             options = ['Mean', 'Median'],
                #             value = 'Mean',
                #             id = self.get_id('data-stats'),
                #             style = self.dropdown_style,
                #         ),
                #         #choose to show or hide error bars
                #         # dcc.RadioItems(
                #             # options=[{'label': i, 'value': i} for i in ['Show Percentage Error', 'Hide Percentage Error']],
                #             # id = self.get_id('percentage-error'),
                #         # ),
                #     ],
                #     style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin-bottom': '50px'}
                # ),
                self.normalize_switch(id = 'normalize-height'),
                dcc.Graph(
                    id = self.get_id('select-time')
                ),
            ]

    def add_graph_callback(self):
        """
        Returns 
        
        """

        @self.app.callback(
            Output(self.get_id('select-time'), 'figure'),
            Output(self.get_id('relative-text'), 'style'),
            Input( self.get_id('which-sensor'), 'value'),
            Input( self.get_id('date-picker-range'), 'start_date'),
            Input( self.get_id('date-picker-range'), 'end_date'),
            Input( self.get_id('normalize-height'), 'on'),
            # Input( self.get_id('data-stats'          ), 'value'),
            # Input( self.get_id('percentage-error'    ), 'value')
        )
        def update_figure(which_sensor, start_date, end_date, normalize_height = True, stat_type = "mean", percentage_error = False):
            '''
            Main plotting function,
            '''
            stat_type = stat_type.lower() # convert to lowercase characters
            # stat_type = "mean"
            
            # calling dataset from data_importer and make it a pandas dataframe
            df = self.data_importer.get_data_by_sensor(which_sensor, numeric_only = True)

            # calling the statistic data that mainly includes the mean of the entire dataset
            df_stats = self.data_importer.df_stats

            # extract sensor name from the function input which_sensor returned from the sensor dropdown menu
            sensor_name = self.data_importer.get_all_sensor_names()[which_sensor]
            print(sensor_name)

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
                # normalized_text = normalized_stat[self.gas_vars].apply(self.as_float)

            # remove infinite values
            # filtered_stat.replace([np.inf, -np.inf], np.nan, inplace=True)
            normalized_stat.replace([np.inf, -np.inf], np.nan, inplace=True)

            # round the stats data to 2 decimal places
            normalized_stat = normalized_stat.round(2)

            #create subplots
            fig = go.Figure()
            titles = ['Meteorology Data', 'Gas Pollutants', 'Particle Pollutants']
            fig = make_subplots(rows = 1, cols = 3, subplot_titles = titles)

            def add_sub_barchart(vars, col, color):
                """
                Defines and returns the filter text style and specific features of the barchart graph

                """

                var_name = ["PM10", "PM2.5","PM1","CO","NO","NO2","O3","Temperature","Humidity",
                "Wind Speed","Adverse Takeoffs/Landings","Adverse Takeoffs/Landings"]

                # define the text shown on each bar and the x-axis variable according to the normalizing data option
                if normalize_height:
                    normalized_text = normalized_stat[vars].apply(self.as_percent)
                    normalized_xaxis = var_name
                else:
                    normalized_text = normalized_stat[vars].apply(self.as_float)
                    normalized_xaxis = list(vars)

                fig.add_trace(
                    go.Bar(
                        x = normalized_xaxis,
                        y = normalized_stat[vars],
                        text = normalized_text,
                        marker_color = px.colors.qualitative.T10[color],
                        hovertemplate = '<b>%{x}</b> %{text}',
                        name = titles[col-1] ,
                        showlegend = False,
                        # error_y =
                        #     dict(
                        #         type = 'data', # value of error bar given in data coordinates
                        #         array = error_by_mean[1:5] if data_stats == 'Mean' else error_by_median[1:7],
                        #         visible = True if percentage_error=='Show Percentage Error' else False
                        #     )
                    ),
                    row = 1,
                    col = col
                )

            add_sub_barchart(self.meteorology_vars + self.flight_vars, 1, color = 0)
            add_sub_barchart(self.gas_vars, 2, color = 2)
            add_sub_barchart(self.particles_vars, 3, color = 5)

            #add title
            # fig.update_layout(title_text="Bar Chart of Standardized Data", title_font_size=30)
            fig.update_layout(margin = {'t': 20})
            # removes the awkward whitespace where the title used to be

            #mark the line y=1 i.e. when filtered mean/median equals entire dataset mean/median
            if normalize_height:
                fig.add_hline(y=1, line_width=3, line_dash="dot", line_color="navy", annotation=dict(text='Average'))
            # fig.update_layout(
            #     go.layout(
            #         yaxis=dict(
            #             range=[0, max(error_by_mean[1:5]+quotients_mean[1:5]) if data_stats == 'Mean'
            #             else max(error_by_median[1:5]+quotients_median[1:5])]
            #         ),
            #         yaxis2 = dict(
            #             range=[0, max(error_by_mean[7:11]+quotients_mean[7:11]) if data_stats == 'Mean'
            #             else max(error_by_median[7:11]+quotients_median[7:11])]
            #         ),
            #         yaxis3 = dict(
            #             range=[0, max(error_by_mean[11:20]+quotients_mean[11:20]) if data_stats == 'Mean'
            #             else max(error_by_median[11:20]+quotients_median[11:20])]
            #         ),
            #     )
            # )

            if normalize_height:
                relative_text_style = self.text_style
            else:
                relative_text_style = self.text_style | {'display': 'none'}

            return fig, relative_text_style