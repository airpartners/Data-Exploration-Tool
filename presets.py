from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
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


    def __init__(self, app):
        self.app = app
        self.layout = self.get_html()
        self.add_callbacks()

    def get_html(self):
        pandemic_radioitem = dcc.RadioItems(
            options = ['all','pre-pandemic','during pandemic','post-pandemic','example-1'],
            value = 'all', 
            inline=True, 
            id='pandemic-radioitems'
        )
        return pandemic_radioitem

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

    def add_callbacks(self):
        type_update = [0, 1, 2, 3, 4]
        type_outputs = []
        for id in type_update:
            type_outputs.append(Output(self.get_id('new-chart-dropdown', id), 'value'))


        dates_update = [12, 18, 24]
        dates_outputs = []
        for id in dates_update:
            dates_outputs.append(Output(self.get_id('date-picker-range', id), 'start_date'))
            dates_outputs.append(Output(self.get_id('date-picker-range', id), 'end_date'))

        sensor_update = [0, 6, 12, 18, 24]
        sensor_outputs = []
        for id in sensor_update:
            sensor_outputs.append(Output(self.get_id('which-sensor', id), 'value'))

        
        # pollutants_update = [0, 6, 18]
        # pollutants_outputs = []
        # for id in pollutants_update:
        #     pollutants_outputs.append(Output(self.get_id('pollutant-dropdown', id), 'value'))

        # correlation_update = [12]
        # correlation_outputs = []
        # for id in correlation_update:
        #     correlation_outputs.append(Output(self.get_id('x-axis', id), 'value'))
        #     correlation_outputs.append(Output(self.get_id('y-axis', id), 'value'))


        @self.app.callback(
            *type_outputs,
            *dates_outputs,
            *sensor_outputs,
            # *pollutants_outputs,
            # *correlation_outputs,
            Input('pandemic-radioitems', 'value'),
        )
        def update_sensors_dates(pandemic_period):
            return [
                *[self.pandemic_chart_type[pandemic_period]],
                *[
                    self.pandemic_start_date[pandemic_period], 
                    self.pandemic_end_date[pandemic_period]
                ]*len(dates_update), *[
                    self.pandemic_sensor_selection[pandemic_period]
                ]*len(sensor_update)
            #   , *[
            #         self.pandemic_pollutant_selection[pandemic_period]
            #     ]*len(pollutants_update), *[
            #         self.correlation_xaxis[pandemic_period],
            #         self.correlation_yaxis[pandemic_period]
            #     ]*len(correlation_update), 
            ]