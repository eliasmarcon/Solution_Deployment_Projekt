import dash
import dash_bootstrap_components as dbc
import dash_daq as daq

import utilities

from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output


# App Main
dash.register_page(__name__, name = 'Machine Learning Tab')

# Create Main Content Area
content = html.Div(

)

# Define the app
layout = html.Div([

    dbc.Row([

        dbc.Col(
            [
                content
            ], width = 12
        )
    ])    
])

