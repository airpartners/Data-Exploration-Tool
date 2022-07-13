from asyncore import poll
import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from filter_graph import FilterGraph # import from supporting file (contained in this repo)
from graph_frame import GraphFrame


class Polar(GraphFrame):
    def get_html(self):
        # children = ...
        return \
            [
                html.Div(
                    [
                        "At",
                        self.sensor_picker(),
                        ", what were the concentrations of ",
                        self.pollutant_picker(multi = False),
                        " on the date range of ",
                        self.date_picker(),
                        "?"
                    ],
                ),
                # Placeholder for a graph to be created.
                # This graph will be updated in the @app.callback: update_figure function below
                dcc.Graph(id=self.get_id('polar'))
            ]

    def add_graph_callback(self):
        self.polar_class = PolarClass(self.data_importer)

        @self.app.callback(
            Output(self.get_id('polar'),'figure'),
            Input(self.get_id('which-sensor'), 'value'),
            Input( self.get_id('date-picker-range'), 'start_date'),
            Input( self.get_id('date-picker-range'), 'end_date'),
            Input(self.get_id('pollutant-dropdown'), 'value'),
        )
        def update_figure(which_sensor, start_date, end_date, pollutant):
            return self.polar_class.update_figure(which_sensor, start_date, end_date, pollutant)



    # if __name__ == '__main__':
    #     app.run_server(debug=True)



class PolarClass(FilterGraph):
    def update_figure(self, which_sensor, start_date, end_date, pollutant):
        df = self.data_importer.get_data_by_sensor(which_sensor)
        df = self.filter_by_date(df, start_date, end_date)
        # df['ws'] = [round (num,2) for num in df['ws']]
        # df['wd'] = [round (num,2) for num in df['wd']]
        # df[pollutant] = [round (num,2) for num in df[pollutant]]
        df = df.round(2)
        df.sort_values(pollutant, ascending = True, inplace = True)

        print("Filtering by pollutant: ", pollutant)

        limit={
            'co.ML': [0,9000],
            'correctedNO': [0,71000],
            'no2.ML': [0,71000],
            'o3.ML': [0,93000],
            'pm1.ML': [0,20],
            'pm25.ML': [0,20],
            'pm10.ML': [0,67]
        }

        fig = px.scatter_polar(df,
            r='ws',
            theta='wd',
            size=pollutant,
            opacity=0.4,
            color=pollutant,
            color_continuous_scale=[(0,"green"),(0.5,"yellow"),(0.75,"red"),(1,"purple")],
            range_color=limit[pollutant],
            hover_name=df.index,
            # template="plotly_dark",
        )

        # add another column which is hour converted to degrees
        fig.update_layout(
            polar={
                "angularaxis": {
                    "tickmode": "array",
                    "tickvals": list(range(0, 360, 360 // 8)),
                    "ticktext": ['N','NE','E','SE','S','SW','W','NW'],
                }
            }
        )
        fig.layout.annotations =[dict(showarrow=False,
                              text='Wind Speed (m/s)',
                              xanchor='left',
                              yanchor='bottom',
                              font=dict(size=12 ))]
        fig.update_layout(margin = {'t': 0, 'l': 360, 'r': 360})
        # fig.update_traces(go.Scatterpolar(
        #     text=df[pollutant],
        #     customdata=df.index,
        #     hovertemplate='interesting<br>%{text}<br><b>{customdata}</b>'
        # ))

        # Add images
        # fig.add_layout_image(
        #     dict(
        #         source="C:/dev/Air Partners/Data Analysis/data/east_boston/maps/sensor_sn11.png",
        #         x=0,
        #         y=0,
        #     )
        # )
        # fig.update_layout(template="plotly_white")

        return fig




