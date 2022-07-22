from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import datetime


from time_series import TimeSeries
from bar_chart_graph import BarChartGraph
from Polar import Polar
from Scatterplot_final import Scatter
from calendar_plot import CalendarPlot

chart_classes = {
    0: CalendarPlot,
    1: TimeSeries,
    2: Scatter,
    3: Polar,
    4: BarChartGraph,
}

class Presets():
    pandemic_chart_type = {
        'all': 0,
        'pre-pandemic': 0,
        'during pandemic': 0,
        'post-pandemic': 0,
        'example-1': 4,
    }

    pandemic_start_date = {
        'all': datetime.date(2019, 9, 8),
        'pre-pandemic': datetime.date(2019, 9, 8),
        'during pandemic': datetime.date(2020, 3, 21),
        'post-pandemic': datetime.date(2020, 7, 1),
        'example-1': datetime.date(2020, 8, 6)
    }
    pandemic_end_date = {
        'all': datetime.date(2021, 3, 5),
        'pre-pandemic': datetime.date(2020, 3, 20),
        'during pandemic': datetime.date(2020, 6, 30),
        'post-pandemic': datetime.date(2021, 3, 5),
        'example-1': datetime.date(2020, 8, 25)
    }
    pandemic_sensor_selection = {
        'all': 0,
        'pre-pandemic': 0,
        'during pandemic': 0,
        'post-pandemic': 0,
        'example-1': 2
    }
    pandemic_pollutant_selection = {
        'all': 'pm25.ML',
        'pre-pandemic': 'pm25.ML',
        'during pandemic': 'pm25.ML',
        'post-pandemic': 'pm25.ML',
        'example-1': 'no2.ML'
    }
    correlation_xaxis = {
        'all': 'temp_manifold',
        'pre-pandemic': 'temp_manifold',
        'during pandemic': 'temp_manifold',
        'post-pandemic': 'temp_manifold',
        'example-1': 'rh_manifold'
    }
    correlation_yaxis = {
        'all': 'pm25.ML',
        'pre-pandemic': 'pm25.ML',
        'during pandemic': 'pm25.ML',
        'post-pandemic': 'pm25.ML',
        'example-1': 'no2.ML'
    }

    pandemic_date_ranges = {
        "data_start": datetime.date(2019, 9, 8),
        "pandemic_start": datetime.date(2020, 3, 20),
        "pandemic_end": datetime.date(2020, 6, 30),
        "data_end": datetime.date(2021, 3, 5),
    }

    keys_to_ids = {
        "start_date": ["date-picker-range", "start_date"],
        "end_date": ["date-picker-range", "end_date"],
        "sensor_location": ["which-sensor", "value"],
        "pollutant": ["pollutant-dropdown", "value"],
        "x_axis": ["x-axis", "value"],
        "y_axis": ["y-axis", "value"],
    }

    preset_scenarios = {
        "Reset Graphs": [
            (
                0,
                {
                    "sensor_location": 0,
                    "pollutant": "PM1.ML",
                }
            ),
            (
                1,
                {
                    "sensor_location": 0,
                    "pollutant": "PM10.ML",
                }
            ),
            (
                2,
                {
                    "sensor_location": 0,
                    'x_axis': "temp_manifold",
                    'y_axis': "PM25.ML",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                }
            ),
            (
                3,
                {
                    "sensor_location": 0,
                    "pollutant": "PM1.ML",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                }
            ),
            (
                4,
                {
                    "sensor_location": 0,
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                }
            ),

        ],
        "Pre-vs. Post-Pandemic": [
            (
                4,
                {
                    "start_date": pandemic_date_ranges["data_start"],
                    "end_date": pandemic_date_ranges["pandemic_start"],
                    "sensor_location": 0
                }
            ),
            (
                4,
                {
                    "start_date": pandemic_date_ranges["pandemic_start"],
                    "end_date": pandemic_date_ranges["pandemic_end"],
                    "sensor_location": 0
                },
            ),
            (
                4,
                {
                    "start_date": pandemic_date_ranges["pandemic_end"],
                    "end_date": pandemic_date_ranges["data_end"],
                    "sensor_location": 0
                },
            ),
        ]
    }


    def __init__(self, app):
        self.app = app
        self.layout = self.get_html()
        for scenario_name, scenario in self.preset_scenarios.items():
            self.add_callbacks(scenario_name, scenario)

    def get_html(self):
        pandemic_radioitem = dcc.RadioItems(
            options = list(self.preset_scenarios.keys()),
            value = None,
            inline = False,
            id = 'preset-radioitems'
        )
        return pandemic_radioitem

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

    def get_id_num_from_chart_num(self, chart_num, chart_type):
        return chart_num * 5 + chart_type

    def add_callbacks(self, scenario_name, scenario):
        outputs = []
        for chart_num, (chart_type, graph_dict) in enumerate(scenario):
            print("chart_num:", chart_num)
            print("chart_type:", chart_type)
            print("graph_dict:", graph_dict)
            outputs.append(Output(self.get_id('new-chart-dropdown', chart_num), 'value'))
            for key in graph_dict.keys():
                outputs.append(Output(
                    self.get_id(self.keys_to_ids[key][0], self.get_id_num_from_chart_num(chart_num, chart_type)),
                    self.keys_to_ids[key][1])
                )

        # outputs = list(dict.fromkeys(outputs)) # remove duplicates, preserving order

        # generate callback based on outputs
        @self.app.callback(
            *outputs,
            Input('preset-radioitems', 'value'),
            prevent_initial_call = True
        )
        def execute_presets(radio_scenario_name):
            if radio_scenario_name != scenario_name:
                raise PreventUpdate
            return_list = []
            # for (chart_type, graph_dict) in self.preset_scenarios[scenario_id]:
            for (chart_type, graph_dict) in scenario:
                print("returning chart type:", chart_type)
                print("returning graph_dict:", graph_dict)
                return_list.append(chart_type)
                for val in graph_dict.values():
                    return_list.append(val)

            # return_list = list(dict.fromkeys(return_list)) # remove duplicates, preserving order

            return tuple(return_list)


            # return [
            #     *[ self.pandemic_chart_type[pandemic_period] ] * len(type_update),
            #     *[ self.pandemic_start_date[pandemic_period], self.pandemic_end_date[pandemic_period] ] * len(dates_update),
            #     *[ self.pandemic_sensor_selection[pandemic_period] ]*len(sensor_update)
            # #   , *[
            # #         self.pandemic_pollutant_selection[pandemic_period]
            # #     ]*len(pollutants_update), *[
            # #         self.correlation_xaxis[pandemic_period],
            # #         self.correlation_yaxis[pandemic_period]
            # #     ]*len(correlation_update),
            # ]