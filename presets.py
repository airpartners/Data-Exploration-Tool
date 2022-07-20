from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import datetime

class Presets():
    pandemic_start_date = {
            'all': datetime.date(2019, 9, 8),
            'pre-pandemic': datetime.date(2019, 9, 8),
            'during pandemic': datetime.date(2020, 3, 21),
            'post-pandemic': datetime.date(2020, 7, 1)
        }
    pandemic_end_date = {
        'all': datetime.date(2021, 3, 5),
        'pre-pandemic': datetime.date(2020, 3, 20),
        'during pandemic': datetime.date(2020, 6, 30),
        'post-pandemic': datetime.date(2021, 3, 5)
    }
    def __init__(self, app):
        self.app = app
        self.layout = self.get_html()
        self.add_callbacks()

    def get_html(self):
        pandemic_radioitem = dcc.RadioItems(
            options = ['all','pre-pandemic','during pandemic','post-pandemic'],
            value = 'all', 
            inline=True, 
            id='pandemic-radioitems'
        )
        return pandemic_radioitem

    def get_id(self, id_str, id_num):
        return id_str + "-" + str(id_num)

    def add_callbacks(self):
        graphs_to_update = [12, 18, 24]
        outputs = []
        for id in graphs_to_update:
            outputs.append(Output(self.get_id('date-picker-range', id), 'start_date'))
            outputs.append(Output(self.get_id('date-picker-range', id), 'end_date'))


        @self.app.callback(
            *outputs,
            Input('pandemic-radioitems', 'value'),
        )
        def update_datepickers(pandemic_period):
            return [self.pandemic_start_date[pandemic_period], self.pandemic_end_date[pandemic_period]]*3
