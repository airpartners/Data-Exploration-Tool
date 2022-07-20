import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc

def get_sensor_map():
    print("Starting getting sensor map...")
    latitude = [42.38436682275741, 42.366293100928964, 42.372108131433066, 42.36425867647669, 42.361552197618515, 42.38273398676193]
    longitude = [-71.00224008848411, -71.03119524615705, -70.99516411546733,  -71.02899217300163, -70.97258190197628, -70.99861095950514]
    # sensor_name = ['SN45', 'SN46', 'SN49', 'SN62', 'SN67', 'SN72']
    sensor_name = [
        "Orient Heights (West end)",
        "Jeffries Point (Maverick end)",
        "Winthrop",
        "Jeffries Point (Airport end)",
        "Point Shirley",
        "Orient Heights (East end)"
    ]
    # latitude = [42.38436682275741]
    # longitude = [-71.00224008848411]
    # sensor_name = ['SN45']
    fig = px.scatter_mapbox(
        lat=latitude,
        lon=longitude,
        hover_name=sensor_name,
        color_discrete_sequence=['#FF0000'],
        size = [1, 1, 1, 1, 1, 1],
        size_max=9,
        opacity=0.9,
        zoom=11.35,
        height=450,
        # customdata=sensor_name
        # hoverinfo="name",
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(customdata = sensor_name, hovertemplate = "%{customdata}")
    # fig.update_traces(hoverinfo = "name")

    print("Finished getting sensor map!")

    return dcc.Graph(id = 'sidebar-map', figure = fig)