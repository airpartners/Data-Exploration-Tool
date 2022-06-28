import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from map_class import Map
map_class = Map()


us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# https://raw.githubusercontent.com/plotly/datasets/master/Nuclear%20Waste%20Sites%20on%20American%20Campuses.csv
# https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv

#locate time slot
# df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
# df = df_major.copy()
# df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
# df["date"] = df["timestamp_local"].dt.date

app = dash.Dash()

df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df = df_major.copy()
df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df["date"] = df["timestamp_local"].dt.date


app.layout = html.Div([
    dcc.DatePickerRange(
        clearable = True,
        with_portal = True,
        start_date = (sd := df['date'].min()).strftime("%Y-%m-%d"),
        end_date = (sd + pd.Timedelta(2, "days")).strftime("%Y-%m-%d"),
        # end_date = df_minor['date'].max().strftime("%Y-%m-%d"),
        id='my-date-picker-range'
    ),
    # html.H4('Interactive Plotly Express color scale selection'),
    # html.P("Color Scale"),
    dcc.Dropdown(
        id='dropdown',
        options=['CO', 'NO', 'NO2', 'O3', 'PM1', 'PM2.5', 'PM10'],
        value='CO'
    ),
    dcc.Graph(id='map'),
])


@app.callback(
    Output('map','figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("dropdown", "value")
)
def update_figure(start_date, end_date, variable_name):
    return map_class.update_figure(start_date, end_date, variable_name)

if __name__ == '__main__':
    app.run_server(debug=True)