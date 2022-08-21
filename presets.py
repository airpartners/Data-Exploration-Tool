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
        "show_explanation": ["explanation-container", "open"],
        "explanation": ["explanation", "children"],
        "explanation_title": ["explanation-title", "children"],
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
                    "show_explanation": True,
                    "explanation_title": "Calendar Plot",
                    "explanation": [
                        html.P([
                            "Shows the pollution levels at a certain sensor over the entire data collection period. ",
                            "Select a sensor location and a pollutant to show."
                        ]),
                        html.P([
                            "Each horizontal strip represents 365 days of data. Each square represents the average concentration levels for one day. ",
                            "If ",html.B("\"Adverse Takeoffs/Landings\""), " or ",html.B("\"Total Takeoffs/Landings\"")," are selected, the square represents the average  takeoffs and landings per hour on that day",
                            "Each column represents one week (the top row is all Mondays, etc.)"]
                        )
                    ],
                },
            ),
            (
                chart_type_ids["timeseries"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM10 (μg/m^3)",
                    "show_explanation": True,
                    "ignore_units": False,
                    "show_explanation": True,
                    "explanation_title": "Timeseries Plot",
                    "explanation": [
                        html.P([
                            "Shows the pollution levels at a certain sensor over time. ",
                            "Select a date range between September 2019 and April 2020, and select one or more pollutants to show at once. ",
                            "To compare variables with different magnitudes, use the ", html.B('"Ignore units"'), " button ",
                            "to scale the values to fit the whole range."
                        ]),
                    ],
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
                    "show_explanation": True,
                    "explanation_title": "Correlation Plot",
                    "explanation": [
                        html.P(["Shows relationships between different variables at the same time. ",
                            "Select a sensor location and a date range between September 2019 and April 2020. You can choose what to display on the x-axis and y-axis respectively, and a correlation line is going to display in the graph to show the correlation between your y-axis variable and your x-axis variable. ",
                        ]),
                        html.P(["For example, if you choose “temperature” on the x-axis and “PM2.5” on the axis, the coefficient m of the displayed equation “PM2.5 = m * temperature + c” indicates how much PM2.5 concentration is correlated to the temperature. ",
                            "The R squared value shows how scattered the data points are, and the range goes from 0 to1. A higher R squared value (generally equals or exceeds 0.4) means a more convincing x-axis variable coefficient (m)."
                        ])
                    ]
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "PM1 (μg/m^3)",
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "show_explanation": True,
                    "explanation_title": "Polar Plot",
                    "explanation": [
                        html.P([
                            "Shows the pollution levels at a certain location based on wind speed and direction. ",
                            "Select a sensor location, select a date range between September 2019 and April 2020, and select one pollutant at a time. ",
                        ]),
                        html.P([
                            "The directions shown on the polar plot represent the direction the wind was blowing ", html.B("from"), ". ",
                            "This type of graph can help with locating pollution sources, particularly if a large number of pollutants are ",
                            "blowing in from a certain direction."
                        ]),
                    ],
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": datetime.date(2019, 12, 1),
                    "end_date": datetime.date(2019, 12, 31),
                    "ignore_units": False,
                    "show_explanation": True,
                    "explanation_title": "Bar Chart",
                    "explanation": [
                        html.P(["Shows a summary of the pollution levels of multiple fine particle categories. ",
                            "Select a date range between September 2019 and April 2020. The bar chart shows the average toxic gas concentrations in parts per billion (ppb) and particle concentrations in micrograms per cubic meter (μg/m^3) over the date range that is selected. ",
                        ]),
                        html.P(["To compare the values to the average pollutant concentration for the entire deployment period of that sensor, use the ", html.B('"Ignore units"'), " button. ",
                            "When ", html.B('"Ignore units"'), " is selected, the bar chart shows the standardized data that is calculated by dividing the mean particle concentration during the selected time slot by the 2-year mean concentration of the same particles measured from the same sensor. "
                        ]),
                    ],
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
                    "show_explanation": True,
                    "ignore_units": True,
                    "explanation_title": "Pre-Pandemic",
                    "explanation": [
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
                    "ignore_units": True,
                    "show_explanation": True,
                    "explanation_title": "Peak Pandemic",
                    "explanation": [
                        html.P([
                            "This chart shows the same variables for the date range of March through June 2020. See how the number of flights arriving or departing from Logan ",
                            "are about half of the average value. Accordingly, gas phase and particulate matter pollution levels were substantially lower (healthier) during ",
                            "this period."
                        ]),
                    ],
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["pandemic_end"],
                    "end_date": preset_date_ranges["data_end"],
                    "ignore_units": True,
                    "show_explanation": True,
                    "explanation_title": "Post Pandemic",
                    "explanation": [
                        html.P([
                            "Same thing but for the date range of July 2020 through April 2021. During this period, the number of flights increased slightly to about 30% below ",
                            "pre-pandemic levels. Even so, the pollutant levels have increased almost back to their pre-pandemic average. ",
                        ]),
                        html.P([
                            "These graphs were made for the sensor at Orient Heights. Try exploring the effects at different sensors."
                        ])
                    ],
                },
            ),
            (
                chart_type_ids["calendar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "NO2 (ppb)",
                    "show_explanation": True,
                    "explanation_title": "Calendar Plot",
                    "explanation": "You can use a calendar plot to look at higher time resolution for a particular pollutant, in this case NO2.",
                },
            ),
            (
                chart_type_ids["calendar_plot"],
                {
                    "sensor_location": 0,
                    "pollutant": "NO2 (ppb)",
                    "show_explanation": True,
                    "explanation_title": "Calendar Plot",
                    "explanation": "This last graph shows the same thing but for a particulate matter pollutant, in this case PM2.5. How do they compare?",
                },
            ),

        ],
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 3                      // #
        # ///////////////////////////////////////////////////////////// #
        (
            "Sources by Wind Direction",
            "At each sensor, see where the pollution was coming from based on wind direction and speed. Hint: pollution was highest when the wind was blowing in from the airport."
        ): [
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": True,
                    "explanation_title": "Polar Plot for Orient Heights",
                    "explanation": [
                        html.P(["Shows the pollution levels at a the Orient Heights sensor based on wind speed and direction. "]),
                        html.P([
                            "Locate the Orient Heights sensor on the map at right. You can also select another location to show using the dropdown menus below. ",
                            "You can also select a date range and pollutant type to show data for."]),
                        html.P([
                        "The directions shown on the polar plot represent the direction the wind was blowing ", html.B("from"), ". ",
                        "This type of graph can help with locating pollution sources, particularly if a large number of pollutants are ",
                        "blowing in from a certain direction."
                        ]),
                        html.P(["See if you can identify plumes of high pollutant concentrations for wind blowing from the direction of the airport."]),
                    ],
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 1,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": True,
                    "explanation_title": "Jeffries Point (Maverick end)",
                    "explanation": [
                        html.P(["Shows the pollution levels at a the Jeffries Point sensor (Maverick end) based on wind speed and direction."]),
                        html.P(["See if you can identify plumes of high pollutant concentrations for wind blowing from the direction of the airport."]),
                    ],
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 2,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": False,
                    "explanation_title": "Winthrop",
                    "explanation": [
                        html.P(["Shows the pollution levels at a the Winthrop sensor based on wind speed and direction."]),
                        html.P(["See if you can identify plumes of high pollutant concentrations for wind blowing from the direction of the airport."]),
                    ],
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 3,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": False,
                    "explanation_title": "Jeffries Point (Airport end)",
                    "explanation": [
                        html.P(["Shows the pollution levels at a the Jeffries Point sensor (Airport end) based on wind speed and direction."]),
                        html.P(["See if you can identify plumes of high pollutant concentrations for wind blowing from the direction of the airport."]),
                    ],
                },
            ),
            (
                chart_type_ids["polar_plot"],
                {
                    "sensor_location": 4,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": False,
                    "explanation_title": "Point Shirley",
                    "explanation": [
                        html.P(["Shows the pollution levels at a the Point Shirley sensor based on wind speed and direction."]),
                        html.P(["See if you can identify plumes of high pollutant concentrations for wind blowing from the direction of the airport."]),
                    ],
                },
            ),
            # (
            #     chart_type_ids["polar_plot"],
            #     {
            #         "sensor_location": 5,
            #         "start_date": preset_date_ranges["data_start"],
            #         "end_date": preset_date_ranges["data_end"],
            #         "show_explanation": True,
            #     }
            # ),
        ],
        # ///////////////////////////////////////////////////////////// #
        # //                    Preset Number 4                      // #
        # ///////////////////////////////////////////////////////////// #
        (
            "Pollutant/Flights Correlation",
            "Under certain meteorological conditions, CO and NO2 are highly correlated with airport activity on runways near the Orient Heights sensor."
        ): [
            (
                chart_type_ids["correlation_plot"],
                {
                    "sensor_location": 0,
                    'x_axis': "Adverse Takeoffs/Landings",
                    'pollutant': "CO (ppb)",
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "show_explanation": True,
                    "wind_selector": ["NW", "SE"],
                    "filter_selector": ["Wind Speed (m/s)", "Temperature (°C)"],
                    "wind_speed_filter": [6, 100],
                    "temp_filter": [10, 100],
                    "explanation_title": "Carbon Monoxide (CO) - Flight correlation",
                    "explanation": [
                        html.P([ html.I([
                            "This graph shows the correlation between carbon monoxide (CO) concentrations and adverse takeoffs and landings ",
                            "for the Orient Heights sensor under certain meteorological condictions. This graph shows a pattern that East Boston ",
                            "residents know well, but it comes with several caveats."
                        ]) ]),
                        html.P([
                            html.B("Results:"), " Adverse flight takeoffs and landings are operations that happened on a runway where the plumes from the airplanes ",
                            "are expected to blow directly towards the sensor. For Orient Heights, this means takeoffs and landings on the north-south runways, ",
                            "especially southward departures, because planes taxi up to the northern end of the runway, turn around, and thrust full force with the ",
                            "engines pointing at the Orient Heights sensor. The x-axis on this graph shows the number of takeoffs and landings on 'adverse' runways ",
                            "per hour for every hour where we have data."
                        ]),
                        html.P([
                            "Carbon monoxide is a gas phase pollutant that is emitted during combustion, including from large vehicles like aircraft. The y-axis shows ",
                            "carbon monoxide concentrations in units of parts per billion (ppb). "
                        ]),
                        html.P([
                            "The trendline on the scatterplot shows that at times when there were larger numbers of adverse flights, the carbon monoxide concentrations ",
                            "tended to be higher. The trendline has an R² value of 0.37, which is high for atmospheric chemistry data. (Different fields ",
                            "have different thresholds for R² values that indicate a significant trend—in carefully controlled physics experiments, for example, ",
                            "values upwards of 0.9 are expected. For atmospheric data science, even values below 0.5 can be considered significant and worthy of ",
                            "investigation). So, this graph seems to show plainly that airport activity on certain runways is correlated with higher CO pollution."
                        ]),
                        html.P([
                            html.B("Caveats:"), " The correlation is only strong for a specific set of meteorolocical conditions, namely wind speeds greater than ",
                            "6 meters per second and temperatures above 10°C. These conditions are somewhat sensible—the correlation can be expected to be stronger ",
                            "when the wind is not stagnant, for exmple. But they were mostly chosen for this example", html.B("because"), " they yielded a high ",
                            "R² value. You are welcome to play around with the filters to see what effect different variables have on the scatterplot, ",
                            "but it will be difficult to find a better correlation coefficient between airport activity and pollution using this data set."
                        ]),
                        html.P([
                            "Perhaps needless to say, it's not good data science practice to mess around with variables and filters until you reach the desired ",
                            "conclusion, in this case a high R² value. Please use caution when interpreting the results of these graphs. The data set is a lot ",
                            "more messy than you might expect, and it is difficult to pin down cause and effect using this tool. There are other avenues for "
                            "making concrete cases against the airport using more robust science. That being said, this is an exploration tool, so test out your "
                            "hypotheses and see what other interesting patterns you can find. Exploration is the first step towards evidence—just not the final step."
                        ]),
                    ],
                },
            ),
            (
                chart_type_ids["timeseries"],
                {
                    "sensor_location": 0,
                    "pollutant": ["Adverse Takeoffs/Landings", "PM10 (μg/m^3)", "NO2 (ppb)"],
                    "start_date": datetime.date(2020, 10, 14),
                    "end_date": datetime.date(2020, 10, 17),
                    "ignore_units": True,
                    "show_explanation": True,
                    "explanation_title": "Runway Activity Over Time",
                    "explanation": "Hellow Worlds!!! #7",
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "ignore_units": True,
                    "filter_selector": ["Adverse Takeoffs/Landings"],
                    "adverse_flight_filter": [0, 33],
                    "show_explanation": True,
                    "explanation_title": "Bar Chart",
                    "explanation": [
                        html.P(["Shows a summary of the pollution levels of multiple fine particle categories. ",
                            "Select a date range between September 2019 and April 2020. The bar chart shows the average toxic gas concentrations in parts per billion (ppb) and particle concentrations in micrograms per cubic meter (μg/m^3) over the date range that is selected. ",
                        ]),
                        html.P(["To compare the values to the average pollutant concentration for the entire deployment period of that sensor, use the ", html.B('"Ignore units"'), " button. ",
                            "When ", html.B('"Ignore units"'), " is selected, the bar chart shows the standardized data that is calculated by dividing the mean particle concentration during the selected time slot by the 2-year mean concentration of the same particles measured from the same sensor. "
                        ]),
                    ],
                },
            ),
            (
                chart_type_ids["bar_chart"],
                {
                    "sensor_location": 0,
                    "start_date": preset_date_ranges["data_start"],
                    "end_date": preset_date_ranges["data_end"],
                    "ignore_units": True,
                    "filter_selector": ["Adverse Takeoffs/Landings"],
                    "adverse_flight_filter": [33, 100],
                    "show_explanation": True,
                    "explanation_title": "Bar Chart",
                    "explanation": [
                        html.P(["Shows a summary of the pollution levels of multiple fine particle categories. ",
                            "Select a date range between September 2019 and April 2020. The bar chart shows the average toxic gas concentrations in parts per billion (ppb) and particle concentrations in micrograms per cubic meter (μg/m^3) over the date range that is selected. ",
                        ]),
                        html.P(["To compare the values to the average pollutant concentration for the entire deployment period of that sensor, use the ", html.B('"Ignore units"'), " button. ",
                            "When ", html.B('"Ignore units"'), " is selected, the bar chart shows the standardized data that is calculated by dividing the mean particle concentration during the selected time slot by the 2-year mean concentration of the same particles measured from the same sensor. "
                        ]),
                    ],
                },
            ),
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
                                    children = html.A('See it yourself', href = '#graphs', style = {"color": CSS.color_scheme["presets"]}),
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