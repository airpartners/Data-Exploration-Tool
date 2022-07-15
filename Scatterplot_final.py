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
    def get_explanation(self):
        return [
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
            html.P("Text some text some text some text."),
        ]

    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At",
                        self.sensor_picker(),
                        ", what was the correlation between",
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
                        " for dates in the range of ",
                        self.date_picker('date-picker-range'),
                        "?"
                    ],
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id=self.get_id('scatterplot'))
            ]

    def add_graph_callback(self):

        @self.app.callback(
            Output(self.get_id('scatterplot'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('date-picker-range'), 'start_date'),
            Input(self.get_id('date-picker-range'), 'end_date'),
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


            fig.update_layout(
                transition_duration = 500,
                margin = {'t': 0}, # removes the awkward whitespace where the title used to be
            )

            # # set title and caption
            # string1 = "Scatter plot"
            # myTitle = '<b>'+string1+'</b>'

            # string2 = 'This is the caption'
            # myCaption = string2


            # fig.update_layout(title=go.layout.Title(
            #     text=myTitle, font=dict(
            #     family="Courier New, monospace",
            #     size=22,
            #     color="#000000"
            #     ))
            # )

            return fig
