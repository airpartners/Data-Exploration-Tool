from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import math
import plotly.express as px
from filter_graph import FilterGraph
from sigfig import round


class BarChart(FilterGraph):

    meteorology_vars = {
        "temp_manifold": "Temperature (°C)",
        "rh_manifold": "Humidity (%)",
        "pressure": "Pressure (Pa)",
        "noise": "Noise (dB)",
        "ws": "Wind Speed (m/s)",
    }
    gas_vars = {
        "co.ML": "CO",
        "correctedNO": "NO",
        "no2.ML": "NO2",
        "o3.ML": "O3",
    }
    particles_vars = {
        "bin0": "0.3-0.5 μm",
        "bin1": "0.5-0.7 μm",
        "bin2": "0.7-1.0 μm",
        "bin3": "1.0-2.5 μm",
        "bin4": "2.5-10 μm",
        "bin5": "10+ μm",
        "pm1.ML": "PM1",
        "pm25.ML": "PM2.5",
        "pm10.ML": "PM10",
    }

    def as_percent(self, x):
        # handle non-numeric data
        if not isinstance(x, (int, float)) or math.isinf(x) or math.isnan(x):
            return np.nan

        return format(round(x - 1, sigfigs = 2), '+,.0%')

    def update_figure(self,start_date, end_date, stat_type, show_percentage_error):
        '''
        Main plotting function
        '''
        which_sensor = 0
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

        # remove infinite values
        filtered_stat.replace([np.inf, -np.inf], np.nan, inplace=True)
        normalized_stat.replace([np.inf, -np.inf], np.nan, inplace=True)

        #create subplots
        fig = go.Figure()
        fig = make_subplots(rows = 1, cols = 3, subplot_titles = ('Meteorology Data', 'Gas Pollutants', 'Particle Pollutants'))

        #first subplot of meteorology data
        fig.add_trace(
            go.Bar(
                x = list(self.meteorology_vars.values()),
                y = normalized_stat[self.meteorology_vars.keys()],
                text = normalized_stat[self.meteorology_vars.keys()].apply(self.as_percent),
                marker_color = px.colors.qualitative.T10[0],
                # customdata = data_mean[1:5] if data_stats == 'Mean' else data_median[1:5],
                # hovertext = sn45_mean[1:5] if data_stats == 'Mean' else sn45_median[1:5],
                # hovertemplate = '<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                # if data_stats == 'Mean' else
                # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name = 'meteorology data',
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
                text = normalized_stat[self.gas_vars.keys()].apply(self.as_percent),
                marker_color=px.colors.qualitative.T10[2],
                # customdata=data_mean[7:11] if data_stats == 'Mean' else data_median[7:11],
                # hovertext=sn45_mean[7:11] if data_stats == 'Mean' else sn45_median[7:11],
                # hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                # if data_stats == 'Mean' else
                # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name='pollutant gas data',
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
                text = normalized_stat[self.particles_vars.keys()].apply(self.as_percent),
                marker_color=px.colors.qualitative.T10[5],
                # customdata=data_mean[11:20] if data_stats == 'Mean' else data_median[11:20],
                # hovertext=sn45_mean[11:20] if data_stats == 'Mean' else sn45_median[11:20],
                # hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                # if data_stats == 'Mean' else
                # '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name='pollutant particle data',
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
        fig.update_layout(title_text="Bar Chart of Standardized Data", title_font_size=30)
        #mark the line y=1 i.e. when filtered mean/median equals entire dataset mean/median
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
        return fig
