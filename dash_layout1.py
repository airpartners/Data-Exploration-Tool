from cv2 import add
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from graph_frame import GraphFrame

class Page():

    chart_names = {
        0: "Bar Chart",
        1: "Timeseries",
        2: "Correlation Plot",
        # 4: "Polar Plot",
    }

    def __init__(self, app, n_charts = 10, n_chart_types = 3) -> None:
        self.app = app
        self.n_charts = n_charts
        self.n_chart_types = n_chart_types
        self.chart_ids = [list(range(n_chart_types * i, n_chart_types * (i + 1))) for i in range(n_charts + 1)] # this works!
        # self.chart_ids = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], ..., [27, 28, 29], [30, 31, 32]]
        self.button_ids = list(range(n_charts + 1))
        # access this with self.chart_ids[chart_type][id_num]
        self.next_id_num = 0 # prepare for the next graph to be added
        self.layout = html.Div(children = [], id = 'main')
        self.create_layout()

    def create_dropdown(self, chart_num, add_callback = True):
        print("Creating Dropdown with id", self.get_id('new-chart-dropdown', chart_num))
        dropdown = \
        dcc.Dropdown(
            # children = "hh",
            options = [
                {'label': "Bar Chart", 'value': 0},
                {'label': "Timeseries", 'value': 1},
                {'label': "Correlation Plot", 'value': 2},
                {'label': "Polar Plot", 'value': 3},
            ],
            # note: in order to set the default value, you have to set value = {the VALUE you want}.
            # Do NOT try to set value = {the LABEL you want}, e.g. value = 'Sensor 1'
            value = None, # default value
            id = self.get_id('new-chart-dropdown', chart_num), # javascript id, used in @app.callback to reference this element, below
            style = {'display': 'none'}
        )
        if add_callback:
            self.add_dropdown_callback(chart_num)
        # print(dropdown)
        return dropdown

    def add_dropdown_callback(self, chart_num):
        @self.app.callback(
            *[Output(self.get_id('frame', id_num), 'style') for id_num in self.chart_ids[chart_num]],
            Output(self.get_id('new-chart-dropdown', chart_num + 1), 'style'),
            # Output(self.get_id('button', chart_num)) # maybe we don't need to hide the old buttons
            Input(self.get_id('new-chart-dropdown', chart_num), 'value'),
        )
        def make_graphs_visible(chart_type):
            print(f"Dropdown with id is being called back!")
            output = [{'display': 'none'}] * self.n_chart_types # create it as a list so it can be modified
            output.append({'display': 'none'})
            if chart_type is None:
                return tuple(output) # then convert to a tuple before returning
            # else:
            output[chart_type] = {'display': 'block'}
            output[-1] = {'display': 'block'}
            return tuple(output)

    def create_layout(self):
        for chart_num in range(self.n_charts):

            self.layout.children.append(self.create_dropdown(chart_num))
            if chart_num == 0:
                self.layout.children[-1].style = {'display': 'block'} # set the initial dropdown to visible
            # self.layout.children.append(self.create_button_set(chart_num))

            for chart_type in range(self.n_chart_types):
                graph_frame = GraphFrame(self.app, self.chart_ids[chart_num][chart_type], chart_type, initial_display_status = 'none')
                self.layout.children.append(graph_frame.frame)

        self.layout.children.append(self.create_dropdown(chart_num + 1, add_callback = False))

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

if __name__ == '__main__':
    app = Dash(__name__) # initialize the app

    p = Page(app)
    app.layout = html.Div(p.layout)

    app.run_server(debug=True)