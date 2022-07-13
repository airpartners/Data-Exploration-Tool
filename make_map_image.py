import pandas as pd
import plotly.graph_objects as go

# us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv
# https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv

import plotly.express as px

def make_map_image(self, sensor_name, lat_long, zoom = 13):

    fig = px.scatter_mapbox(
        lat=[lat_long[0]],
        lon=[lat_long[1]],
        color_discrete_sequence=['#FF0000'],
        # size = [1, 1, 1, 1, 1, 1],
        size = [1],
        zoom=zoom,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.show()
    fig.write_image(file = f"C:/dev/Air Partners/Data Analysis/data/east_boston/maps/sensor_{sensor_name}.png")
    pass

make_map_image('a', 'sn11', (42.38436682275741, -71.00224008848411))
pass