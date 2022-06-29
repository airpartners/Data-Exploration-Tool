from plotly.subplots import make_subplots
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from filter_graph import FilterGraph


class BarChart(FilterGraph):

    def update_figure(self,start_date, end_date, data_stats, percentage_error):
        '''
        Main plotting function
        '''
        df = self.data_importer.get_data_by_sensor(0, numeric_only = True)

        # filter by timestamp and wind direction
        df = self.filter_by_date(df, start_date, end_date)

        #mean of the filtered data
        data_mean = df.mean(axis=0)
        #median of the filtered data
        data_median = df.median(axis=0)

        fig = go.Figure()

        #make two separate lists of the means and medians of the entire dataset
        sn45_mean = self.stats['sn45_mean']
        sn45_median = self.stats['sn45_median']
        #calculate standard deviation of filtered data
        standdev = []
        for i in df.columns[1:]:
            # print(df[i].head(2))
            standdev.append(np.nanstd(df[i]) if not isinstance(df[i].iloc[0], str) else 0)

        stdev = df.std()[1:] # ignore the first value (stdev of the timestamp)
        # norm_mean =
        # maybe also make it into a list

        #mean standardization: divide filtered data mean by entire dataset mean
        quotients_mean = []
        #mean percentage error: divide standard deviation of filtered data mean by entire dataset mean
        error_by_mean = []
        #median standardization: divide filtered data median by entire dataset median
        quotients_median = []
        #median percentage error: divide standard deviation of filtered data median by entire dataset median
        error_by_median = []
        for mean, means, median, medians, i in zip (data_mean,sn45_mean, data_median, sn45_median, standdev):
            quotients_mean.append(mean/means) if means is not str and means!=0.000000 else quotients_mean.append(0)
            error_by_mean.append(abs((i-means)/means)) if means is not str and means!=0.000000 else error_by_mean.append(0)
            quotients_median.append(median/medians) if medians is not str and medians!=0.000000 else quotients_median.append(0)
            error_by_median.append(abs((i-medians)/medians)) if medians is not str and medians!=0.000000 else error_by_median.append(0)


        round_quotients_mean = [round(num,2) for num in quotients_mean]
        round_quotients_median = [round(num,2) for num in quotients_median]


        #create subplots
        fig = make_subplots(rows=1, cols=3, subplot_titles=('Meteorology Data','Gas Pollutants','Particle Pollutants'))

        #first subplot of meteorology data
        fig.add_trace(
            go.Bar(
                x=['Temperature','RH','Pressure','Noise'],
                y=quotients_mean[1:5] if data_stats == 'Mean' else  quotients_median[1:5],
                text=round_quotients_mean[1:5] if data_stats == 'Mean' else round_quotients_median[1:5],
                marker_color=px.colors.qualitative.T10[0],
                customdata=data_mean[1:5] if data_stats == 'Mean' else data_median[1:5],
                hovertext=sn45_mean[1:5] if data_stats == 'Mean' else sn45_median[1:5],
                hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                if data_stats == 'Mean' else
                '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name='meteorology data',
                showlegend=False,
                error_y =
                    dict(
                        type='data', # value of error bar given in data coordinates
                        array=error_by_mean[1:5] if data_stats == 'Mean' else error_by_median[1:7],
                        visible = True if percentage_error=='Show Percentage Error' else False
                    )
            ),
        row=1, col=1
        )

        #second subplot of pollutant gas concentration data
        fig.add_trace(
            go.Bar(
                x=['CO','NO','NO2','O3'],
                y=quotients_mean[7:11] if data_stats == 'Mean' else  quotients_median[7:11],
                text=round_quotients_mean[7:11] if data_stats == 'Mean' else round_quotients_median[7:11],
                marker_color=px.colors.qualitative.T10[2],
                customdata=data_mean[7:11] if data_stats == 'Mean' else data_median[7:11],
                hovertext=sn45_mean[7:11] if data_stats == 'Mean' else sn45_median[7:11],
                hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                if data_stats == 'Mean' else
                '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name='pollutant gas data',
                showlegend=False,
                error_y =
                    dict(
                        type='data', # value of error bar given in data coordinates
                        array=error_by_mean[7:11] if data_stats == 'Mean' else error_by_median[7:11],
                        visible = True if percentage_error=='Show Percentage Error' else False
                    )
            ),
        row=1, col=2
        )

        #third subplot of pollutant particle concentration data
        fig.add_trace(
            go.Bar(
                x=['PM1','PM2.5','PM10','0.3-0.5 Microns', '0.5-0.7 Microns','0.7-1 Microns',
                '1-2.5 Microns','2.5-10 Microns','10+ Microns'],
                y=quotients_mean[11:20] if data_stats == 'Mean' else  quotients_median[11:20],
                text=round_quotients_mean[11:20] if data_stats == 'Mean' else round_quotients_median[11:20],
                marker_color=px.colors.qualitative.T10[5],
                customdata=data_mean[11:20] if data_stats == 'Mean' else data_median[11:20],
                hovertext=sn45_mean[11:20] if data_stats == 'Mean' else sn45_median[11:20],
                hovertemplate='<br><b>%{x}</b><br>Filtered data mean:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of mean:%{y}'
                if data_stats == 'Mean' else
                '<br><b>%{x}</b><br>Filtered data median:%{customdata}<br>Entire data set median:%{hovertext}<br>Quotient of median:%{y}',
                name='pollutant particle data',
                showlegend=False,
                error_y =
                    dict(
                        type='data', # value of error bar given in data coordinates
                        array=error_by_mean[11:20] if data_stats == 'Mean' else error_by_median[11:20],
                        visible = True if percentage_error=='Show Percentage Error' else False
                    )
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
