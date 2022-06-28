from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
from filter_graph import FilterGraph # import from supporting file (contained in this repo)

# Parent class for TimeSeries, BarChart, CorrelationPlot, and PolarPlot
class GraphFrame():

    # define HTML styles for text and dropdown menus. Use this to change font size, alignment, etc.
    text_style = {
        "display": "inline-block", # if you take this out, all successive elements will be displayed on separate lines
        "transform": "translateY(0%)", # vertical alignment
        "position": "relative",
        "margin-left": "10px", # adds a horizontal space between dropdowns menus and next chunk of text
        "font-size" : "30px",
        "font-family": "Arial",
        "line-height": "0%", # helps reduce the line spacing
    }

    dropdown_style = {
        "display": "inline-block",
        "width": "200px",
        "height": "30px",
        "margin-left": "10px",
        "font-size": "20px",
        "font-family": "Arial",
        "line-height": "0%", # helps reduce the line spacing
    }

    date_picker_style = {
        "display": "inline-block",
        # "width": "200px", # not used or doesn't work
        "height": "40px",
        "margin-left": "10px",
        # "font-family": "Arial", # not used or doesn't work
        "line-height": "0%", # helps reduce the line spacing
    }

    def __init__(self, app, id_num, chart_type = 0, initial_display_status = 'block') -> None:
        self.app = app
        self.id_num = id_num
        self.frame = self.get_layout(initial_display_status)
        self.add_graph_callback()

    def get_id(self, id_str):
        return id_str + "-" + str(self.id_num)

    def get_html(self):
        return "Placeholder for GraphFrame child class"

    def get_layout(self, initial_display_status):
        return \
        html.Div(
            children = self.get_html(),
            style = {'display': initial_display_status},
            id = self.get_id('frame')
        )

    def add_graph_callback(self):
        self.filter_graph = FilterGraph()

        @self.app.callback(
            Output(self.get_id('graph-to-update'), 'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('start-date'), 'date'),
            Input(self.get_id('end-date'), 'date'),
            Input(self.get_id('wind-direction'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date, wind_direction):
            print(f"Graph with id {self.id_num} being called back!")
            return self.filter_graph.update_figure(int(which_sensor), start_date, end_date, wind_direction)