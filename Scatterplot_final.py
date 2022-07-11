import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from graph_frame import GraphFrame

class Scatter(GraphFrame):
    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At",
                        dcc.Dropdown(
                            options = [
                                {'label': 'SN45', 'value': 0},
                                {'label': 'SN46', 'value': 1},
                                {'label': 'SN49', 'value': 2},
                                {'label': 'SN62', 'value': 3},
                                {'label': 'SN67', 'value': 4},
                                {'label': 'SN72', 'value': 5},
                            ],
                            # note: in order to set the default value, you have to set value = {the VALUE you want}.
                            # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
                            value = 0, # default value
                            id = self.get_id("which-sensor"), # javascript id, used in @app.callback to reference this element, below
                            clearable = False, # prevent users from deselecting all sensors
                            style = self.dropdown_style
                        ),
                        ", what were the correlations between",
                        dcc.Dropdown(
                            id=self.get_id('x-axis'),
                            options = self.all_vars,
                            value='temp_manifold',
                            style = self.dropdown_style | {"width": "340px"}
                        ),
                        " and",
                        dcc.Dropdown(
                            id=self.get_id('y-axis'),
                            options = self.all_vars,
                            multi = True,                            
                            value='pm25.ML',
                            style = self.dropdown_style | {"width": "340px"}
                        ),
                        " when dates are between",
                        dcc.DatePickerSingle(
                            display_format='MM/DD/Y',
                            date = datetime.date(2019, 12, 1), # default value
                            id = self.get_id('start-date'),
                            style = self.date_picker_style
                        ),
                        "and",
                        dcc.DatePickerSingle(
                            date = datetime.date(2020, 1, 1), # default value
                            display_format='MM/DD/Y',
                            id = self.get_id('end-date'),
                            style = self.date_picker_style
                        ),
                        "?"
                    ],
                    style = self.text_style
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id=self.get_id('scatterplot'))
            ]

    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('scatterplot'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            Input(self.get_id('x-axis'), 'value'),
            Input(self.get_id('y-axis'), 'value'),
            )

        def update_figure(which_sensor, start_date, end_date, xaxis_column_name, yaxis_column_name):
            df = self.data_importer.get_data_by_sensor(which_sensor)
            df = self.filter_by_date(df, start_date, end_date)


            fig = px.scatter(df, x=xaxis_column_name, y=yaxis_column_name,
                    trendline="ols",
                    hover_name=df.index,
                    # log_x=True, size_max=15
                )


            # fig.update_xaxes(title=xaxis_column_name,
            #                 type='linear' if xaxis_type == 'Linear' else 'log')

            # fig.update_yaxes(title=str(yaxis_column_name),
            #                 type='linear' if yaxis_type == 'Linear' else 'log')
                            

            fig.update_layout(transition_duration=500)

            # set title and caption
            string1 = "Scatter plot"
            myTitle = '<b>'+string1+'</b>'

            string2 = 'This is the caption'
            myCaption = string2


            fig.update_layout(title=go.layout.Title(
                text=myTitle, font=dict(
                family="Courier New, monospace",
                size=22,
                color="#000000"
                ))
            )

            return fig
        