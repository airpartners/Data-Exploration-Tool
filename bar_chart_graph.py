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
from barchart_class import BarChart

class BarChartGraph(GraphFrame):
    def get_html(self):
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
                self.normalize_switch(my_id = 'normalize-height'),
                dcc.Graph(
                    id = self.get_id('select-time')
                ),
            ]

    def add_graph_callback(self):

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
            Main plotting function
            '''
            stat_type = stat_type.lower() # convert to lowercase characters
            # stat_type = "mean"

            df = self.data_importer.get_data_by_sensor(which_sensor, numeric_only = True)

            df_stats = self.data_importer.df_stats
            sensor_name = self.data_importer.get_all_sensor_names()[which_sensor]


            df = self.filter_by_date(df, start_date, end_date) # filter by timestamp and wind direction

            if stat_type == "mean":
                filtered_stat = df.mean(axis = 0)
                normalized_stat = filtered_stat / df_stats[sensor_name, "mean"]
            elif stat_type == "median":
                filtered_stat = df.median(axis=0)
                normalized_stat = filtered_stat / df_stats[sensor_name, "median"]
            else:
                raise KeyError("Unsupported aggregation function. Try 'mean' or 'median' instead.")

            # if normalize_height is unchecked, undo the division by df_stats
            if normalize_height:
                normalized_text = normalized_stat[self.gas_vars.keys()].apply(self.as_percent)
            else:
                normalized_stat = filtered_stat
                normalized_text = normalized_stat[self.gas_vars.keys()].apply(self.as_float)

            # remove infinite values
            # filtered_stat.replace([np.inf, -np.inf], np.nan, inplace=True)
            normalized_stat.replace([np.inf, -np.inf], np.nan, inplace=True)

            #create subplots
            fig = go.Figure()
            fig = make_subplots(rows = 1, cols = 3, subplot_titles = ('Meteorology Data', 'Gas Pollutants', 'Particle Pollutants'))

            def add_sub_barchart(vars, name):
                pass

            #first subplot of meteorology data
            fig.add_trace(
                go.Bar(
                    x = list(self.meteorology_vars.values()),
                    y = normalized_stat[self.meteorology_vars.keys()],
                    text = normalized_text,
                    marker_color = px.colors.qualitative.T10[0],
                    # customdata = data_mean[1:5] if data_stats == 'Mean' else data_median[1:5],
                    # hovertext = sn45_mean[1:5] if data_stats == 'Mean' else sn45_median[1:5],
                    # hovertemplate = '<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                    # if data_stats == 'Mean' else
                    # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                    # name = 'meteorology data',
                    showlegend = False,
                    # error_y =
                    #     dict(
                    #         type = 'data', # value of error bar given in data coordinates
                    #         array = error_by_mean[1:5] if data_stats == 'Mean' else error_by_median[1:7],
                    #         visible = True if percentage_error=='Show Percentage Error' else False
                    #     )
                ),
            row = 1, col = 1
            )

            #second subplot of pollutant gas concentration data
            fig.add_trace(
                go.Bar(
                    x = list(self.gas_vars.values()),
                    y = normalized_stat[self.gas_vars.keys()],
                    text = normalized_text,
                    marker_color=px.colors.qualitative.T10[2],
                    # customdata=data_mean[7:11] if data_stats == 'Mean' else data_median[7:11],
                    # hovertext=sn45_mean[7:11] if data_stats == 'Mean' else sn45_median[7:11],
                    # hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                    # if data_stats == 'Mean' else
                    # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                    # name='pollutant gas data',
                    showlegend=False,
                    # error_y =
                    #     dict(
                    #         type='data', # value of error bar given in data coordinates
                    #         array=error_by_mean[7:11] if data_stats == 'Mean' else error_by_median[7:11],
                    #         visible = True if percentage_error=='Show Percentage Error' else False
                    #     )
                ),
            row=1, col=2
            )

            #third subplot of pollutant particle concentration data
            fig.add_trace(
                go.Bar(
                    x = list(self.particles_vars.values()),
                    y = normalized_stat[self.particles_vars.keys()],
                    text = normalized_text,
                    marker_color = px.colors.qualitative.T10[5],
                    # customdata=data_mean[11:20] if data_stats == 'Mean' else data_median[11:20],
                    # hovertext=sn45_mean[11:20] if data_stats == 'Mean' else sn45_median[11:20],
                    # hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                    # if data_stats == 'Mean' else
                    # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                    # name='pollutant particle data',
                    showlegend=False,
                    # error_y =
                    #     dict(
                    #         type='data', # value of error bar given in data coordinates
                    #         array=error_by_mean[11:20] if data_stats == 'Mean' else error_by_median[11:20],
                    #         visible = True if percentage_error=='Show Percentage Error' else False
                    #     )
                ),
            row=1, col=3
            )

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