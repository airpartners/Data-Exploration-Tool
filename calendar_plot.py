from dash import html, dcc, Input, Output
from plotly_calplot import calplot # pip install plotly-calplot
import pandas as pd
from graph_frame import GraphFrame
from css import CSS


class CalendarPlot(GraphFrame):
    def get_explanation(self):
        return [
            html.P([html.B("Calendar Plot:"), " Shows the pollution levels at a certain sensor over the entire data collection period. ",
            "Select a sensor location and a pollutant to show. ",
            "Each horizontal strip represents 365 days of data. Each square represents the average concentration levels for one day. ",
            "If ",html.B("\"Adverse Takeoffs/Landings\""), " or ",html.B("\"Total Takeoffs/Landings\"")," are selected, the square represents the average  takeoffs and landings per hour on that day",
            "Each column represents one week (the top row is all Mondays, etc.)"]
            )
        ]


    def get_html(self):
        """
        Defines the structure of barchart in html

        The filter message and dropdown menus are defined as html.Div() arguments, and the graph will be updated in the
        add_graph_callback(): update_figure() function below

        """
        return \
            [
                html.Div(
                    [
                        "At ",
                        self.sensor_picker(), # calling the sensor dropdown menu defined in graph_frame.py
                        ", what was the level of ",
                        self.pollutant_picker(multi = False, show_flights = True), # calling the pollutant dropdown menu defined in graph_frame.py
                        " over the entire date range for that sensor?",
                    ],
                    style = CSS.text_style # defining text styles
                ),
                dcc.Graph(id = self.get_id('calendar-plot'))
            ]


    def add_graph_callback(self):
        """
        Defines and returns all the text and calendar plot features

        This function consists of two sections:
        - @self.app.callback that contains all the input and output callback functions;
        - the main plotting function update_figure() that takes sensor and pollutant selections from the filter message dropdowns(defined above
         as html.Div() arguments in get_html() function) to choose the demanded dataset and/or select the demanded column of dataset to plot on the graph

        """

        @self.app.callback(
            # the id of the graph lines up with the id argument in dcc.Graph defined in get_html() function
            Output(self.get_id('calendar-plot'),'figure'),

            # the values of the two inputs below are called from the filter message dropdowns above in get_html() function
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('pollutant-dropdown'), 'value')
            )

        def update_figure(which_sensor, pollutant):
            """
            Main plotting function:
            - selects and processes the dataset
            - then makes the plot
            """

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            # calculate daily average and save the results
            df=df.resample('D').mean()

            # rename the columns in df_stats to something more understandable
            df = df.rename(columns={
                "pm10.ML": "PM10 (μg/m^3)",
                "pm25.ML": "PM2.5 (μg/m^3)",
                "pm1.ML": "PM1 (μg/m^3)",
                "co.ML": "CO (ppb)",
                "correctedNO": "NO (ppb)",
                "no2.ML": "NO2 (ppb)",
                "o3.ML": "O3 (ppb)",
                "temp_manifold": "Temperature (°C)",
                "rh_manifold": "Humidity (%)",
                "ws": "Wind Speed (m/s)",
                "adverse_flight_count": "Adverse Takeoffs/Landings",
                "count": "Total Takeoffs/Landings",
            })

            # define start date and end date of the calendar plot based on local_timestamp (the index) of datasets
            start_date = df.index[0]
            end_date = df.index[-1]
            dummy_df = pd.DataFrame({
                "ds": pd.date_range(start_date, end_date),
                "value": df[pollutant].squeeze()
            })

            # define colorscales based on EPA standards
            color_scale = {
                'PM2.5 (μg/m^3)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.5,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'PM10 (μg/m^3)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.5,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'PM1 (μg/m^3)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.5,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'NO (ppb)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.9,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'CO (ppb)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.9,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'NO2 (ppb)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.9,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'O3 (ppb)': [(0,"#eeeeee"),(0.00000000000001,"white"),(0.9,"#ffc300"),(0.95,"#ff5733"),(1,"#900c3f")],
                'Adverse Takeoffs/Landings': [(0, "#eeeeee"),(0.00001,"white"),(1,"#c70039")],
                'Total Takeoffs/Landings': [(0,"#eeeeee"),(0.00001,"white"),(1,"#c70039")]
            }

            # creating the plot
            fig = calplot(dummy_df,
                    x='ds',
                    y='value',
                    years_title=True,
                    colorscale=color_scale[pollutant],
                    month_lines_color="black",
                    month_lines_width=1,
                    showscale=True
            )

            self.update_background_colors(fig)

            return fig

