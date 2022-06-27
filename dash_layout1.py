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

    def create_button(self, chart_num, chart_type):
        id_num = self.chart_ids[chart_num][chart_type]
        print("Creating Button with button id", self.get_id('button', id_num))
        button = \
        html.Button(
            children = self.chart_names[chart_type],
            id = self.get_id('button', id_num),
            n_clicks = 0
        )
        self.add_button_callback(id_num)
        return button

    def add_button_callback(self, id_num):
        self.app.clientside_callback(
            """
            function(n_clicks) {
                console.log("HOwdy dandy, World! ... This is a Button!");
                console.log("n_clicks: " + n_clicks);
                if (n_clicks > 0) {
                    return {'display': 'block'};
                } else {
                    return {'display': 'none'};
                }
            }
            """,
            Output(self.get_id('frame', id_num), 'style'),
            Input(self.get_id('button', id_num), 'n_clicks'),
        )

    def create_button_set(self, chart_num):
        buttons = []
        for chart_type in range(self.n_chart_types):
            buttons.append(self.create_button(chart_num, chart_type))

        button_set = \
        html.Div(
            children = buttons,
            id = self.get_id('button-set', self.button_ids[chart_num]),
            style = {'display': 'block'}
        )
        self.add_button_set_callback(chart_num) # this is a list
        return button_set

    def add_button_set_callback(self, chart_num):
        self.app.clientside_callback(
            """
            function(...inputs) {
                console.log("HOwdy dandy, World! ...");
                console.log("n_clicks: " + inputs);
                sum = inputs.reduce(function(a, b) { return a + b; }, 0);
                if (sum > 0) {
                    return [{'display': 'none'}];
                } else {
                    return [{'display': 'block'}];
                }
            }
            """,
            Output(self.get_id('button-set', self.button_ids[chart_num]), 'style'),
            # make it so the next button set erases the current one
            *[Input(self.get_id('button-set', id_num), 'n_clicks') for id_num in self.chart_ids[chart_num + 1]]
        )

    def create_layout(self):
        for chart_num in range(self.n_charts):
            buttons = []

            for chart_type in range(self.n_chart_types):
                graph_frame = GraphFrame(self.app, self.chart_ids[chart_num][chart_type], chart_type)
                self.layout.children.append(graph_frame.frame)
                self.next_id_num += 1
                # buttons.append(self.create_button(chart_num, chart_type))
                # new_button_ids

            self.layout.children.append(self.create_button_set(chart_num))

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

if __name__ == '__main__':
    app = Dash(__name__) # initialize the app

    p = Page(app)
    app.layout = html.Div(p.layout)

    app.run_server(debug=True)