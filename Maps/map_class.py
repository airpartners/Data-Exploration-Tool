import pandas as pd
import plotly.graph_objects as go  
import plotly.express as px
from load import Load
results=Load()
'''
QUOTIENT INDEX LIST
temp_manifold: 0
rh_manifold: 1
pressure: 2
noise: 3
bin0: 4
bin1: 5
bin2: 6
bin3: 7
bin4: 8
bin5: 9
wd: 10
ws: 11
co.ML: 12
no.ML: 13
no2.ML: 14
o3.ML: 15
pm1.ML: 16
pm25.ML: 17
pm10.ML: 18
'''

class Map():
    def __init__(self):
        self.fig = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
        # https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv
        # https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv


    def update_figure(self,start_date,end_date,variable_name):
        
        quotient_sn45=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
        quotient_sn46=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn46-final-w-ML-PM.csv')
        quotient_sn49=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn49-final-w-ML-PM.csv')
        quotient_sn62=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn62-final-w-ML-PM.csv')
        quotient_sn67=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn67-final-w-ML-PM.csv')
        quotient_sn72=results.calculate(start_date,end_date,'C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn72-final-w-ML-PM.csv')

        
        co = [quotient_sn45[0][12],quotient_sn46[0][12],quotient_sn49[0][12],quotient_sn62[0][12],quotient_sn67[0][12],quotient_sn72[0][12]]
        no = [quotient_sn45[0][13],quotient_sn46[0][13],quotient_sn49[0][13],quotient_sn62[0][13],quotient_sn67[0][13],quotient_sn72[0][13]]
        no2 = [quotient_sn45[0][14],quotient_sn46[0][14],quotient_sn49[0][14],quotient_sn62[0][14],quotient_sn67[0][14],quotient_sn72[0][14]]
        o3 = [quotient_sn45[0][15],quotient_sn46[0][15],quotient_sn49[0][15],quotient_sn62[0][15],quotient_sn67[0][15],quotient_sn72[0][15]]
        pm1 = [quotient_sn45[0][16],quotient_sn46[0][16],quotient_sn49[0][16],quotient_sn62[0][16],quotient_sn67[0][16],quotient_sn72[0][16]]
        pm25 = [quotient_sn45[0][17],quotient_sn46[0][17],quotient_sn49[0][17],quotient_sn62[0][17],quotient_sn67[0][17],quotient_sn72[0][17]]
        pm10 = [quotient_sn45[0][18],quotient_sn46[0][18],quotient_sn49[0][18],quotient_sn62[0][18],quotient_sn67[0][18],quotient_sn72[0][18]]

        if variable_name == 'CO':
            variable = co
        elif variable_name == 'NO':
            variable = no
        elif variable_name == 'NO2':
            variable = no2
        elif variable_name == 'O3':
            variable = o3
        elif variable_name == 'PM1':
            variable = pm1
        elif variable_name == 'PM2.5':
            variable = pm25
        else:
            variable = pm10


        latitude = [42.38436682275741, 42.366293100928964, 42.372108131433066, 42.36425867647669, 42.361552197618515, 42.38730430752273]
        longitude = [-71.00224008848411, -71.03119524615705, -70.99516411546733,  -71.02899217300163, -70.97258190197628, -71.00479111744103]
        sensor_name = ['SN45', 'SN46', 'SN49', 'SN62', 'SN67', 'SN72']
        fig = px.scatter_mapbox(
            lat=latitude, 
            lon=longitude, 
            hover_name=sensor_name, 
            color=variable,
            color_continuous_scale=[(0, "green"), (0.5, "yellow"), (1, "red")],
            size = [1, 1, 1, 1, 1, 1],
            zoom=11, 
            height=500)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig

