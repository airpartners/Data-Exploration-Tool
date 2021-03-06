from dash import Dash, dcc, html, Input, Output
import pandas as pd
from data_importer import DataImporter

#call BarChart class defined in barchart_class.py which should be in the same repo
from barchart_class import BarChart
barchart_class = BarChart()

#locate time slot
# df_major = pd.read_csv('C:/Users/zxiong/Desktop/Olin/Air Partners/Code/sn45-final-w-ML-PM.csv')
# df = df_major.copy()
# df["timestamp_local"] = pd.to_datetime(df_major["timestamp_local"], format = "%Y-%m-%dT%H:%M:%SZ")
# df["date"] = df["timestamp_local"].dt.date

data_importer = DataImporter()
df = data_importer.get_data_by_sensor(0)
df["date"] = df["timestamp_local"].dt.date

app = Dash(__name__)


app.layout = html.Div([
    #apply filter to select time range
    dcc.DatePickerRange(
        clearable = True,
        with_portal = True,
        start_date = (sd := df['date'].min()).strftime("%Y-%m-%d"),
        end_date = (sd + pd.Timedelta(2, "days")).strftime("%Y-%m-%d"),
        # end_date = df_minor['date'].max().strftime("%Y-%m-%d"),
        id='my-date-picker-range'
    ),
    html.Div(
        [
            #choose to plot either mean or median datasets at one time
            dcc.Dropdown(
                options = [
                    {'label': 'Mean', 'value': 'mean'},
                    {'label': 'Median', 'value': 'median'},
                ],
                value = 'mean',
                id='stat-type'
            ),
            #choose to show or hide error bars
            dcc.RadioItems(
                options=[{'label': i, 'value': i} for i in ['Show Percentage Error', 'Hide Percentage Error']],
                id='percentage-error',
            ),
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    dcc.Graph(id='select-time'),
])


@app.callback(
    Output('select-time', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('stat-type', 'value'),
    Input('percentage-error','value')
)
def update_figure(start_date, end_date, data_stats, percentage_error):
    return barchart_class.update_figure(start_date, end_date, data_stats, percentage_error)

if __name__ == '__main__':
    app.run_server(debug=True)