from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

'''
RUN THIS FILE TO DISPLAY THE GRAPHS
'''

#call BarChart class defined in barchart_class.py which should be in the same repo
from scatterplot_class import ScatterPlot
scatterplot_class = ScatterPlot()

#locate time slot
df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
df = df_major.copy()
df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
df["date"] = df["timestamp_local"].dt.date


app = Dash(__name__)



app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    dcc.DatePickerRange(
        clearable = True,
        with_portal = True,
        start_date = (sd := df['date'].min()).strftime("%Y-%m-%d"),
        end_date = (sd + pd.Timedelta(2, "days")).strftime("%Y-%m-%d"),
        # end_date = df_minor['date'].max().strftime("%Y-%m-%d"),
        id='my-date-picker-range'
    ),
    html.Div([
        html.Div([
            dcc.Dropdown(
                ['wind_dir', 'temp_box', 'pm10', 'pm25', 'no2'],
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                ['wind_dir', 'temp_box', 'pm10', 'pm25', 'no2'],
                multi=True,
                id='yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
 ])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    # prevent_initial_call=True
)



def update_figure(start_date, end_date, xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
    return scatterplot_class.update_figure(start_date, end_date, xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type)


if __name__ == '__main__':
    app.run_server(debug=True)
