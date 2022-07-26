from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State


def filter_picker(self, my_id = 'filter-set'):
    vars = list(self.meteorology_vars.items()) + list(self.flight_vars.items())


    filters = []
    for var_name, var in vars.items():
        filters.append(
            html.Div(
                children = [
                    var_name + ":",
                    dcc.RangeSlider(min = 0, max = 100, step = 1, value = [0, 100], id = self.get_id('filter-by-' + var)),
                ],
                style = {'display': 'inline'}
            )
        )

    return_var = \
        html.Div(
            children = [
                dcc.Dropdown(
                    options = [{'label': var_name, 'value': var} for var, var_name in vars],
                    value = 'blankenship',

                    multi = True,
                    id = self.get_id(my_id),

                    style = (self.dropdown_style_2 | {"width": "800px"})
                ),
                *filters
            ]
        )





    return return_var