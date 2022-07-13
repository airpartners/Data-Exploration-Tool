from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from graph_frame import GraphFrame
from time_series import TimeSeries
from bar_chart_graph import BarChartGraph
from data_importer import DataImporter
from Polar import Polar
from Scatterplot_final import Scatter
from calendar_plot import CalendarPlot

class Page():

    chart_names = {
        0: "Timeseries",
        1: "Correlation Plot",
        2: "Polar Plot",
        3: "Bar Chart",
        4: "Calendar Plot"
    }

    chart_classes = {
        0: TimeSeries,
        1: Scatter,
        2: Polar,
        3: BarChartGraph,
        4: CalendarPlot
    }

    def __init__(self, app, n_charts = 10) -> None:
        self.app = app
        self.n_charts = n_charts
        self.n_chart_types = len(self.chart_classes.keys())
        self.chart_ids = [list(range(self.n_chart_types * i, self.n_chart_types * (i + 1))) for i in range(n_charts + 1)] # this works!
        # self.chart_ids = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], ..., [27, 28, 29], [30, 31, 32]]
        self.button_ids = list(range(n_charts + 1))
        # access this with self.chart_ids[chart_type][id_num]
        self.next_id_num = 0 # prepare for the next graph to be added
        self.layout = html.Div(children = [], id = 'main')

        self.data_importer = DataImporter()

        self.create_layout()

    def create_dropdown(self, chart_num, initial_display_status, placeholder_text = None, add_callback = True):
        print("Creating Dropdown with id", self.get_id('new-chart-dropdown', chart_num))
        if not add_callback:
            return html.Div(
                children = f"Cannot add more than {self.n_charts} charts.",
                id = self.get_id('new-chart-dropdown', chart_num),
                style = GraphFrame.text_style | {'display': initial_display_status},
            )
        # else:

        # `options` is formatted in this way, because this is the format that dcc.Dropdown requires
        options = [
            {'label': "Timeseries", 'value': 0},
            {'label': "Correlation Plot", 'value': 1},
            {'label': "Polar Plot", 'value': 2},
            {'label': "Bar Chart", 'value': 3},
            {'label': "Calendar Plot", 'value': 4},
        ]

        if placeholder_text in range(4):
            placeholder = options[placeholder_text]["label"]
        else:
            placeholder = "Create another graph..."

        dropdown = \
        dcc.Dropdown(
            options = options,
            # note: in order to set the default value, you have to set value = {the VALUE you want}, e.g. value = 0.
            # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
            value = None, # default value
            id = self.get_id('new-chart-dropdown', chart_num), # javascript id, used in @app.callback to reference this element
            placeholder = placeholder,
            style = GraphFrame.dropdown_style_header | {'display': initial_display_status} # right-most dictionary xwins ties for keys
        )
        if add_callback:
            self.add_dropdown_callback(chart_num)
        # print(dropdown)
        return dropdown

    def add_dropdown_callback(self, chart_num):
        @self.app.callback(
            *[Output(self.get_id('frame', id_num), 'style') for id_num in self.chart_ids[chart_num]],
            Output(self.get_id('new-chart-dropdown', chart_num + 1), 'style'),
            Input(self.get_id('new-chart-dropdown', chart_num), 'value'),
            prevent_initial_call = True
        )
        def make_graphs_visible(chart_type):
            print(f"Dropdown with id is being called back!")
            output = [{'display': 'none'}] * self.n_chart_types # create it as a list so it can be modified
            output.append(GraphFrame.dropdown_style_header | {'display': 'none'})
            if chart_type is None:
                return tuple(output) # then convert to a tuple before returning
            # else:
            output[chart_type] = GraphFrame.text_style | {'display': 'block'}
            output[-1] = GraphFrame.dropdown_style_header | {'display': 'block'}
            return tuple(output)

    def create_layout(self):
        for chart_num in range(self.n_charts):

            # add dropdown
            initial_display_status = 'block' if chart_num in [0, 1, 2, 3, 4] else 'none'
            add_callback = chart_num < self.n_charts - 1 # not the last element
            self.layout.children.append(self.create_dropdown(chart_num, initial_display_status, placeholder_text = chart_num, add_callback = add_callback))

            # add graph frame
            for chart_type in range(self.n_chart_types):
                chart_class = self.chart_classes[chart_type]

                initial_display_status = 'block' if chart_num in [0, 1, 2, 3] and chart_type == chart_num else 'none'
                graph_frame = chart_class(self.app, self.data_importer, self.chart_ids[chart_num][chart_type], chart_type, initial_display_status)

                self.layout.children.append(graph_frame.frame)

        # self.layout.children.append(self.create_dropdown(chart_num + 1, add_callback = False))

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

if __name__ == '__main__':
    app = Dash(__name__) # initialize the app

    p = Page(app, n_charts = 10)
    app.layout = html.Div(p.layout)

    app.run_server(debug=True)