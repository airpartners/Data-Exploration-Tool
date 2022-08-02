from asyncore import poll
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

from graph_frame import GraphFrame
import css

class TimeSeries(GraphFrame):

    def get_explanation(self):
        return [
            html.P([html.B("Timeseries:"), " Shows the pollution levels at a certain sensor over time. ",
            "Select a date range between September 2019 and April 2020, and select one or more pollutants to show at once. ",
            "To compare variables with different magnitudes, use the ", html.B('"Ignore units"'), " button ",
            "to scale the values to fit the whole range."]
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
                        self.sensor_picker(),
                        # "in the date range of ",
                        # self.date_picker(),
                        ", what was the value of ",
                        self.pollutant_picker(),
                        "?",
                        self.normalize_switch(),
                    ],
                    style = self.text_style
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                # html.Div(
                    # chilfwidren = [
                dcc.Graph(id = self.get_id('graph-to-update')),
                    # ],
                    # style = {'display': 'flex'}
                # ),
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
            Output(self.get_id('graph-to-update'), 'figure'),

            # the values of the two inputs below are called from the filter message dropdowns above in get_html() function
            Input(self.get_id('which-sensor'), 'value'),
            Input(self.get_id('pollutant-dropdown'), 'value'),
            Input(self.get_id('normalize-height'), 'on'),
        )
        # def update_figure(which_sensor, start_date, end_date, pollutant, normalize_height):
        def update_figure(which_sensor, pollutant, normalize_height):
            print(f"Graph with id {self.id_num} being called back!")

            # turn the input argument pollutamt into a list, since time series graph accepts multiple variables on the y-axis
            if isinstance(pollutant, str):
                pollutant = [pollutant]

            # select which sensor data to draw from
            df = self.data_importer.get_data_by_sensor(which_sensor)

            if normalize_height:
                df = self.normalize_height(df)

            # round the dataset to display 2 decimal places
            df = df.round(2)
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

            # plot line
            fig = px.line(df, x=df.index, y = pollutant, render_mode='webg1')

            # fig = go.Figure([
            #     go.Line(
            #         name = 'Average',
            #         x = df.index,
            #         y = df,
            #         fill = pollutant,
            #         # mode = 'lines',
            #         # line = dict(color = 'rgb(31, 119, 180)'),
            #     ),
                # go.Scatter(
                #     name = '95th Percentile',
                #     x = df.index,
                #     y = df["pm25.ML"],
                #     mode = 'lines',
                #     marker = dict(color = "#444"),
                #     line = dict(width = 0),
                #     showlegend = False
                # ),
                # go.Scatter(
                #     name = '5th Percentile',
                #     x = df.index,
                #     y = df["pm25.ML"],
                #     marker = dict(color = "#444"),
                #     line = dict(width = 0),
                #     mode = 'lines',
                #     fillcolor = 'rgba(68, 68, 68, 0.3)',
                #     fill = 'tonexty',
                #     showlegend = False
                # )
            # ])

            # set the time range to be the entire dataset
            start_date = df.index[0]
            end_date = df.index[-1]
            if len(pollutant) == 1:
                y_label = pollutant[0]
            else:
                y_label = 'Pollutant (refer to legend)'

            # add time division tabs
            fig.update_layout(
                xaxis_title = 'Timestamp',
                yaxis_title = y_label,
                margin = {'t': 0}, # removes the awkward whitespace where the title used to be
                xaxis = dict(
                    rangeselector = dict(
                        buttons = list([
                            dict(count=1,
                                label="1d",
                                step="day",
                                stepmode="backward"),
                            dict(count=7,
                                label="1w",
                                step="day",
                                stepmode="backward"),
                            dict(count=1,
                                label="1m",
                                step="month",
                                stepmode="backward"),
                            dict(count=3,
                                label="3m",
                                step="month",
                                stepmode="todate"),
                            dict(count=6,
                                label="6m",
                                step="month",
                                stepmode="backward"),
                            dict(count=1,
                                label="1y",
                                step="year",
                                stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider = dict(
                        autorange = True,
                        range = [start_date, end_date],
                        visible = True,
                    ),
                    type="date"
                ),
                yaxis = dict(
                    autorange = True,
                    fixedrange = False
                )

            )

            # when y=100%, filtered mean equals entire dataset mean
            if normalize_height:
                fig.layout.yaxis.tickformat = ',.0%'

            fig.update_traces(
                hovertemplate='%{y}'
            )

            fig.update_layout(uirevision = "Static Literal String")
            fig.update_layout(
                modebar_add=[
                    'zoom',
                    # 'drawline',
                    # 'drawopenpath',
                    # 'drawclosedpath',
                    # 'drawcircle',
                    # 'drawrect',
                    # 'eraseshape'
                ],
                hovermode = 'x'
            )
            fig.update_layout(
                paper_bgcolor="rgb(0,0,0,0)",
                legend = dict(bgcolor = css.color_scheme["main_background"]),
                plot_bgcolor = "#FFFFFF",
            )
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E3E3E3')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E3E3E3')

            return fig