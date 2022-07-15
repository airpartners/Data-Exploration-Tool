import pandas as pd
import plotly.graph_objects as go

us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv
# https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv

import plotly.express as px

# latitude = [42.38436682275741, 42.366293100928964, 42.372108131433066, 42.36425867647669, 42.361552197618515, 42.38730430752273]
# longitude = [-71.00224008848411, -71.03119524615705, -70.99516411546733,  -71.02899217300163, -70.97258190197628, -71.00479111744103]
# sensor_name = ['SN45', 'SN46', 'SN49', 'SN62', 'SN67', 'SN72']
latitude = [42.38436682275741]
longitude = [-71.00224008848411]
sensor_name = ['SN45']
fig = px.scatter_mapbox(
    lat=latitude,
    lon=longitude,
    hover_name=sensor_name,
    color_discrete_sequence=['#FF0000'],
    # size = [1, 1, 1, 1, 1, 1],
    size = [0],
    zoom=12,
    height=600)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
pass