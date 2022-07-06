import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px

from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from graph_frame import GraphFrame


class Polar(GraphFrame):
    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        html.Div(
                            html.P("At "),
                            style = self.text_style
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    options = [
                                        {'label': 'SN45', 'value': '0'},
                                        {'label': 'SN46', 'value': '1'},
                                        {'label': 'SN49', 'value': '2'},
                                        {'label': 'SN62', 'value': '3'},
                                        {'label': 'SN67', 'value': '4'},
                                        {'label': 'SN72', 'value': '5'},
                                    ],
                                    # note: in order to set the default value, you have to set value = {the VALUE you want}.
                                    # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
                                    value = '0', # default value
                                    id = self.get_id("which-sensor"), # javascript id, used in @app.callback to reference this element, below
                                    clearable = False # prevent users from deselecting all sensors
                                ),
                            ],
                            style = self.dropdown_style
                        ),
                        html.Div(
                            html.P(", what were the concentrations of"),
                            style = self.text_style
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id='pollutant', 
                                    options=['co.ML', 'correctedNO', 'no2.ML', 'o3.ML', 'pm1.ML', 'pm25.ML', 'pm10.ML'], # ['CO', 'NO', 'NO2', 'O3', 'PM1', 'PM2.5', 'PM10']
                                    value='co.ML'
                                ),
                            ],
                            style = self.dropdown_style
                        ), 
                        html.Div(
                            html.P(" between"),
                            style = self.text_style
                        ),
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    display_format='MM/DD/Y',
                                    date = datetime.date(2019, 12, 1), # default value
                                    id = self.get_id('start-date'),
                                ),
                            ],
                            style = self.date_picker_style
                        ),
                        html.Div(
                            html.P(" and "),
                            style = self.text_style
                        ),
                        html.Div(
                            [
                                dcc.DatePickerSingle(
                                    date = datetime.date(2020, 1, 1), # default value
                                    display_format='MM/DD/Y',
                                    id = self.get_id('end-date'),
                                ),
                            ],
                            style = self.date_picker_style
                        ),
                        html.Div(
                            html.P("?"),
                        ),
                    ]
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id='polar')
            ]

    def add_graph_callback(self):
        self.polar_class = PolarClass(self.data_importer)

        @self.app.callback(
            Output(self.get_id('polar'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            Input(self.get_id('pollutant'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date, pollutant):
            print('whatever')
            return self.polar_class.update_figure(int(which_sensor), start_date, end_date, pollutant)

    

    # if __name__ == '__main__':
    #     app.run_server(debug=True)



class PolarClass(FilterGraph):
    def update_figure(self, which_sensor, start_date, end_date, pollutant):
        df = self.data_importer.get_data_by_sensor(which_sensor)
        df = self.filter_by_date(df, start_date, end_date)

        limit={
            'co.ML': [0,9000], 
            'correctedNO': [0,71000], 
            'no2.ML': [0,71000], 
            'o3.ML': [0,93000], 
            'pm1.ML': [0,20], 
            'pm25.ML': [0,20], 
            'pm10.ML': [0,67]
        }

        fig = px.scatter_polar(df,
            r='ws',
            theta='wd', 
            size=self.df_filtered[pollutant], 
            opacity=0.4,
            color=self.df_filtered[pollutant],
            color_continuous_scale=[(0,"green"),(0.5,"yellow"),(0.75,"red"),(1,"purple")],
            range_color=limit[pollutant],
            # template="plotly_dark",
        )

        # add another column which is hour converted to degrees
        fig.update_layout(
            polar={
                "angularaxis": {
                    "tickmode": "array",
                    "tickvals": list(range(0, 360, 360 // 8)),
                    "ticktext": ['N','NE','E','SE','S','SW','W','NW'],
                }
            }
        )
        fig.layout.annotations =[dict(showarrow=False, 
                              text='Wind Speed (m/s)', 
                              xanchor='left',   
                              yanchor='bottom',  
                              font=dict(size=12 ))]    

        return fig




