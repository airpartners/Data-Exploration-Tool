from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import datetime

from bar_chart_graph import BarChartGraph
from Scatterplot_final import Scatter
from calendar_plot import CalendarPlot
from time_series import TimeSeries
from polar_plot_v2 import Polar

from css import CSS

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
        "explanation": ["explanation", "children"],
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
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 1                      // #
        # ///////////////////////////////////////////////////////////// #

        (
            "Default",
            "To get back to the default settings: Explore the calendar, timeline, correlations, wind direction, and average pollutant charts."): [
            (
                chart_type_ids["calendar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM1 (μg/m^3)",
                    "show_details": True,
                    "explanation": CalendarPlot.get_explanation("self-placeholder"),
                },
            ),
            (
                chart_type_ids["timeseries"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM10 (μg/m^3)",
                    "show_details": True,
                    "ignore_units": False,
                    "explanation": TimeSeries.get_explanation("self-placeholder"),
                },
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
                    "explanation": Scatter.get_explanation("self-placeholder"),
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM1 (μg/m^3)",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_details": True,
                    "explanation": Polar.get_explanation("self-placeholder"),
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_details": True,
                    "ignore_units": False,
                    "explanation": BarChartGraph.get_explanation("self-placeholder"),
                },
            ),

        ],
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 2                      // #
        # ///////////////////////////////////////////////////////////// #
        (
            "Pre-vs. Post-Pandemic",
            "During the Covid-19 pandemic, airport activity dropped dramatically. So did particulate and gas pollution."
        ): [
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["pandemic_start"],
                    "show_details": True,
                    "ignore_units": True,
                    "explanation": [
                        html.H4("Pre-Pandemic"),
                        "This bar chart shows the averages of all the variables over the pre-Pandemic date range of September 2019 to March 2020. During this period, ",
                        "activity at Logan Airport was at typical levels, and pollution from particulate matter (PM1-10) as well as gas phase pollutants (CO, NOx) ",
                        "was at or above average."
                    ]
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["pandemic_start"],
                    "end_date": preset_date_ranges["pandemic_end"],
                    "show_details": True,
                    "ignore_units": True,
                    "explanation": [
                        html.H4("Peak Pandemic"),
                        "This chart shows the same variables for the date range of March through June 2020. See how the number of flights arriving or departing from Logan ",
                        "are about half of the average value. Accordingly, gas phase and particulate matter pollution levels were substantially lower (healthier) during ",
                        "this period."
                    ],
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["pandemic_end"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "ignore_units": True,
                    "explanation": "Hellow Worlds!!! #0",
                },
            ),
        ],
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 3                      // #
        # ///////////////////////////////////////////////////////////// #
        ("Sources by Wind Direction", "At each sensor, see where the pollution was coming from based on wind direction and speed. Hint: pollution was highest when the wind was blowing in from the airport."): [
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "explanation": "Hellow Worlds!!! #1",
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 1,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "explanation": "Hellow Worlds!!! #2",
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 2,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "explanation": "Hellow Worlds!!! #3",
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 3,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "explanation": "Hellow Worlds!!! #4",
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 4,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_details": True,
                    "explanation": "Hellow Worlds!!! #5",
                },
            ),
            # (
            #     chart_type_ids["polar_plot"],
            #     {
            #         "sensor_location": 5,
            #         "start_date": preset_date_ranges["data_start"],
            #         "end_date": preset_date_ranges["data_end"],
            #         "show_details": True,
            #     }
            # ),
        ],
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 4                      // #
        # ///////////////////////////////////////////////////////////// #
        ("Pollutant/Flights Correlation", "Under certain meteorological conditions, CO and NO2 are highly correlated with airport activity on runways near the sensor."): [
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
                    "explanation": "Hellow Worlds!!! #6",
                },
            )
        ]
    }


    def __init__(self, app):
        self.app = app
        self.layout = self.get_html()
        for (scenario_name, scenario_description), scenario in self.preset_scenarios.items():
            self.add_callbacks(scenario_name, scenario)

    def get_html(self):
        pandemic_radioitem = dcc.RadioItems(
            options = [scenario_item[0] for scenario_item in self.preset_scenarios.keys()],
            value = None,
            inline = False,
            style = {'display': 'block'},
            id = 'preset-radioitems',
        )
        return pandemic_radioitem

    def get_cards(self):
        cards = []
        for scenario_item in self.preset_scenarios.keys():
            scenario_name = scenario_item[0]
            scenario_desc = scenario_item[1]
            card = \
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(html.B(scenario_name)),
                                html.P(scenario_desc),
                                html.Button(
                                    children = html.A('See it yourself', href = '#graphs'),
                                    n_clicks = 0,
                                    style = {
                                        "border-color": CSS.color_scheme["presets"],
                                        "border-radius": "4px",
                                        # "border-style": "solid",
                                        "background-color": "white",
                                        "color": CSS.color_scheme["presets"]
                                    },
                                    id = self.get_str_id('preset-button', scenario_name)
                                ),
                            ],
                        ),
                        style = {"display": "inline-flex", "color": "white", "margin-top": "8px"},
                        color = CSS.color_scheme["presets"],
                    )
                )
            cards.append(card)
        return html.Div(dbc.Row(children = cards))

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

    def get_str_id(self, id_str, id_suffix):
        return id_str + ''.join(filter(str.isalnum, id_suffix))

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
            Input(self.get_str_id('preset-button', scenario_name), 'n_clicks'),
            prevent_initial_call = False if scenario_name == "Default" else True # perform the callback on the Default preset
        )
        def execute_presets(radio_scenario_name):
            # if radio_scenario_name != scenario_name:
            #     raise PreventUpdate # https://community.plotly.com/t/how-to-leave-callback-output-unchanged/7276/13

            return_list = []
            # for (chart_type, graph_dict) in self.preset_scenarios[scenario_id]:
            for (chart_type, graph_dict) in scenario:
                print("returning chart type:", chart_type)
                print("returning graph_dict:", graph_dict)
                return_list.append(chart_type)
                for val in graph_dict.values():
                    return_list.append(val)

            return tuple(return_list)