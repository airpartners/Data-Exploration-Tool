import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from polar_class import Polar
bar_polar=Polar()
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
    dcc.Dropdown(
        id='dropdown', 
        options=['co.ML', 'correctedNO', 'no2.ML', 'o3.ML', 'pm1.ML', 'pm25.ML', 'pm10.ML'], # ['CO', 'NO', 'NO2', 'O3', 'PM1', 'PM2.5', 'PM10']
        value='co.ML'
    ),
    dcc.Graph(id='polar')
    ])

@app.callback(
    Output('polar','figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('dropdown','value')
)
def update_figure(start_date, end_date, variable_name):
    return bar_polar.update_figure(start_date, end_date, variable_name)

if __name__ == '__main__':
    app.run_server(debug=True)

