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

    preset_date_ranges = {
        "data_start": datetime.date(2019, 9, 8),
        "pandemic_start": datetime.date(2020, 3, 20),
        "pandemic_end": datetime.date(2020, 6, 30),
        "data_end": datetime.date(2021, 3, 5),
    }

    chart_type_ids = {
        "calendar_plot": 0,
        "timeseries": 1,
        "correlation_plot": 2,
        "polar_plot": 3,
        "bar_chart": 4,
    }

    keys_to_ids = {
        "start_date": ["date-picker-range", "start_date"],
        "end_date": ["date-picker-range", "end_date"],
        "sensor_location": ["which-sensor", "value"],
        "pollutant": ["pollutant-dropdown", "value"],
        "x_axis": ["x-axis", "value"],
        # "y_axis": ["y-axis", "value"],
        "show_details": ["explanation", "open"],
        "ignore_units": ["normalize-height", "on"],
        "filter_selector": ["filter-set", "value"],
        "hum_filter": ["filter-by-Humidity (%)", "value"], # "value" is a list of [min, max]
        "temp_filter": ["filter-by-Temperature (°C)", "value"], # "value" is a list of [min, max]
        "wind_speed_filter": ["filter-by-Wind Speed (m/s)", "value"], # "value" is a list of [min, max]
        "total_flight_filter": ["filter-by-Total Takeoffs/Landings", "value"], # "value" is a list of [min, max]
        "adverse_flight_filter": ["filter-by-Adverse Takeoffs/Landings", "value"], # "value" is a list of [min, max]
        "wind_selector": ["wind-direction-picker", "value"], # "value" is a list of wind directions, e.g. ["NW", "SE"]
    }

    preset_scenarios = {
        "Reset Graphs": [
            (
                chart_type_ids["calendar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM1 (μg/m^3)",
                    "show_details": True,
                }
            ),
            (
                chart_type_ids["timeseries"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM10 (μg/m^3)",
                    "show_details": True,
                    "ignore_units": False,
                }
            ),
            (
                chart_type_ids["correlation_plot"],
                {
                    "sensor_location": 0,
                    'x_axis': "Temperature (°C)",
                    # 'y_axis': "pm25.ML",
                    'pollutant': "PM2.5 (μg/m^3)",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_details": True,
                }
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM1 (μg/m^3)",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_details": True,
                }
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_details": True,
                    "ignore_units": False,
                }
            ),

        ],
        "Pre-vs. Post-Pandemic": [
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["pandemic_start"],
                    "show_details": False,
                    "ignore_units": True,
                }
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["pandemic_start"],
                    "end_date": preset_date_ranges["pandemic_end"],
                    "show_details": False,
                    "ignore_units": True,
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["pandemic_end"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": False,
                    "ignore_units": True,
                },
            ),
        ],
        "Source Direction": [
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                }
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 1,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": False,
                }
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 2,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": False,
                }
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 3,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": False,
                }
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 4,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": False,
                }
            ),
            # (
            #     chart_type_ids["polar_plot"],
            #     {
            #         "sensor_location": 5,
            #         "start_date": preset_date_ranges["data_start"],
            #         "end_date": preset_date_ranges["data_end"],
            #         "show_details": False,
            #     }
            # ),
        ],
        "Pollutant/Flights Correlation": [
            (
                chart_type_ids["correlation_plot"],
                {
                    "sensor_location": 0,
                    'x_axis': "Adverse Takeoffs/Landings",
                    'pollutant': "CO (ppb)",
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "wind_selector": ["NW", "SE"],
                    "filter_selector": ["Wind Speed (m/s)", "Temperature (°C)"],
                    "wind_speed_filter": [6, 100],
                    "temp_filter": [10, 100],
                }
            )
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
            style = {'display': 'block'},
            id = 'preset-radioitems',
        )
        return pandemic_radioitem

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

    def get_id_num_from_chart_num(self, chart_num, chart_type):
        return chart_num * len(self.chart_type_ids) + chart_type

    def add_callbacks(self, scenario_name, scenario):
        outputs = []
        for chart_num, (chart_type, graph_dict) in enumerate(scenario):
            outputs.append(Output(self.get_id('new-chart-dropdown', chart_num), 'value'))
            for key in graph_dict.keys():
                outputs.append(Output(
                    self.get_id(self.keys_to_ids[key][0], self.get_id_num_from_chart_num(chart_num, chart_type)),
                    self.keys_to_ids[key][1])
                )

        # generate callback based on outputs
        @self.app.callback(
            *outputs,
            Input('preset-radioitems', 'value'),
            prevent_initial_call = True
        )
        def execute_presets(radio_scenario_name):
            if radio_scenario_name != scenario_name:
                raise PreventUpdate # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/13

            return_list = []
            # for (chart_type, graph_dict) in self.preset_scenarios[scenario_id]:
            for (chart_type, graph_dict) in scenario:
                print("returning chart type:", chart_type)
                print("returning graph_dict:", graph_dict)
                return_list.append(chart_type)
                for val in graph_dict.values():
                    return_list.append(val)

            return tuple(return_list)