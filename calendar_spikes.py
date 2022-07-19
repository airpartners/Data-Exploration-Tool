from asyncore import poll
from typing import final
from dash import html, dcc, Input, Output
from plotly_calplot import calplot # $pip install plotly-calplot
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from graph_frame import GraphFrame


class CalendarSpikePlot(GraphFrame):
    def get_explanation(self):
        return [
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
            # html.P("Text some text some text some text."),
        ]


    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At ",
                        self.sensor_picker(),
                        ", what was the level of ",
                        self.pollutant_picker(multi = False),
                        "?",
                    ],
                    style = self.text_style
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                # html.Div(
                    # chilfwidren = [
                dcc.Graph(id = self.get_id('calendar-plot')),
                    # ],
                    # style = {'display': 'flex'}
                # ),
            ]


    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('calendar-plot'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('pollutant-dropdown'), 'value')
            )

        def update_figure(which_sensor, pollutant):

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # if isinstance(pollutant, str):
            #     pollutant = [pollutant]

            start_date = df.index[0]
            end_date = df.index[-1]


            # limit = {
            #     'pm25.ML': 20,
            #     'pm10.ML': 35,
            #     'pm1.ML': 35,
            #     'correctedNO': 45,
            #     'co.ML': 9000,
            #     'no2.ML': 1000,
            #     'o3,ML': 1000
            # }

            # smooth = 24
            # conv = [1/smooth] * smooth
            # offload = smooth // 2
            # variable = np.array(df[pollutant].squeeze())
            # conv_list=np.convolve(conv,variable)
            # conv_results = []
            # for item in conv_list:
            #     conv_results.append(1) if item >= limit[str(pollutant)] else conv_results.append(0)
            
            # conv_results = conv_results[offload:-offload+1]
            # new_list = [conv_results[i:i + 24] for i in range(0, len(conv_results), 24)]

            # final_results = []
            # for list in new_list:
            #     final_results.append(1) if 1 in list else final_results.append(0.5)
            
            
            
            # extend_number = len(pd.date_range(start_date, end_date)) - len(final_results)
            # final_results.extend([0]*extend_number)
            
            
            
            # x1=range(len(list1))

            # offset = smooth // 2
            # x = range(-offset, len(new_list) - offset)

            # calculate daily average                
            df=df.resample('D').mean()

            # df.index = pd.date_range('01/01/2018',
            #                         periods=8,
            #                         freq='W')

            # print(df.index)
            # pollution_level = np.array(df[pollutant])
            # pollution_level = list(np.average(pollution_level.reshape(-1, 24), axis=1))
            

            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
                "value": df[pollutant]
            })

            color_scale = {
                'pm25.ML': [(0,"white"),(0.00000000000001,"green"),(0.5,"yellow"),(1,"red")],
                'pm10.ML': [(0,"white"),(0.00000000000001,"green"),(0.5,"yellow"),(1,"red")],
                'pm1.ML': [(0,"white"),(0.00000000000001,"green"),(0.5,"yellow"),(1,"red")],
                'correctedNO': [(0,"white"),(0.00000000000001,"green"),(0.9,"yellow"),(1,"red")],
                'co.ML': [(0,"white"),(0.00000000000001,"green"),(0.95,"yellow"),(1,"red")],
                'no2.ML': [(0,"white"),(0.00000000000001,"green"),(0.9,"yellow"),(1,"red")],
                'o3,ML': [(0,"white"),(0.00000000000001,"green"),(0.9,"yellow"),(1,"red")]
            }

            # creating the plot
            fig = calplot(dummy_df,
                    x='ds',
                    y='value',
                    # data=df[pollutant]
                    years_title=True,
                    # colorscale=[(0,"white"),(0.000000000001,"green"),(0.5,"yellow"),(0.8,"red"),(1,"purple")],
                    colorscale=color_scale[pollutant],
                    showscale=True,
                    # colorbar=True
            )

            return fig

