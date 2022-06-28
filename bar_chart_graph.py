from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
from filter_graph import FilterGraph # import from supporting file (contained in this repo)

from graph_frame import GraphFrame
from barchart_class import BarChart

class BarChartGraph(GraphFrame):
    def get_html(self):
        # children = ...
        return \
            [
                #apply filter to select time range
                dcc.Graph(
                    id = self.get_id('select-time')
                ),
                dcc.DatePickerRange(
                    clearable = True,
                    with_portal = True,
                    start_date = "2020-01-01",
                    end_date = "2020-01-03",
                    id = self.get_id('my-date-picker-range')
                ),
                html.Div(
                    [
                        #choose to plot either mean or median datasets at one time
                        dcc.Dropdown(
                            ['Mean', 'Median'],
                            'Mean',
                            id = self.get_id('data-stats')
                        ),
                        #choose to show or hide error bars
                        dcc.RadioItems(
                            options=[{'label': i, 'value': i} for i in ['Show Percentage Error', 'Hide Percentage Error']],
                            id = self.get_id('percentage-error'),
                        ),
                    ],
                    style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
                )
            ]

    def add_graph_callback(self):
        self.filter_graph = FilterGraph()
        self.barchart = BarChart()

        @self.app.callback(
            Output(self.get_id('select-time'         ), 'figure'),
            Input( self.get_id('my-date-picker-range'), 'start_date'),
            Input( self.get_id('my-date-picker-range'), 'end_date'),
            Input( self.get_id('data-stats'          ), 'value'),
            Input( self.get_id('percentage-error'    ), 'value')
        )
        def update_figure(start_date, end_date, data_stats, percentage_error):
            return self.barchart.update_figure(start_date, end_date, data_stats, percentage_error)
