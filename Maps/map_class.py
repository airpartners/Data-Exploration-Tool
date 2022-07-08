import pandas as pd
import plotly.graph_objects as go  
import plotly.express as px
from calculate_quotients import CalculateQuotients
from csv_file_paths import processed_csv_paths
results=CalculateQuotients()
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
correctedNO: 12
co.ML: 13
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
    
        quotient_results=[]
        for file in processed_csv_paths:
            quotient_results.append(results.calculate(start_date,end_date,file))
        quotient_results = pd.DataFrame(quotient_results)
        quotient_results_mean=quotient_results[0]

        pollutants = pd.DataFrame([[0]*6]*7)
        for i in pollutants.columns:
            pollutants[i][0:7]=quotient_results_mean[i][12:19]
        pollutants['idx']=['NO', 'CO', 'NO2', 'O3', 'PM1', 'PM2.5', 'PM10']
        pollutants=pollutants.set_index('idx')
        percentage=pollutants*100
        percentage=percentage.round(3)

        latitude = [42.38436682275741, 42.366293100928964, 42.372108131433066, 42.36425867647669, 42.361552197618515, 42.38273398676193]
        longitude = [-71.00224008848411, -71.03119524615705, -70.99516411546733,  -71.02899217300163, -70.97258190197628, -70.99861095950514]
        sensor_name = ['SN45', 'SN46', 'SN49', 'SN62', 'SN67', 'SN72']

        
        fig = px.scatter_mapbox(
            lat=latitude, 
            lon=longitude, 
            color=pollutants.loc[variable_name],
            color_continuous_scale=[(0,"green"),(0.5,"yellow"),(0.75,"red"),(1,"purple")],
            range_color=[0,3],
            # text = percentage.loc[variable_name],
            size = [10,10,10,10,10,10],
            zoom=12.7,
            opacity=0.9,
            height=500)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_traces(go.Scattermapbox(
            customdata=percentage.loc[variable_name],
            hovertext=sensor_name, 
            hovertemplate='<br>%{hovertext}<b><br>%{customdata}<span>&#37;</span></b> of 2-year mean'
        ))
        # fig.update_traces(go.Scattermapbox(
        #     lat=latitude,
        #     lon=longitude,
        #     mode='text+markers',
        #     marker = {'size': 20},
        #     text = [1,1,1,1,1,1],#percentage.loc[variable_name],
        #     textposition = "bottom right"
        # ))

        return fig

