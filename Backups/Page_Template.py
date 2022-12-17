import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_daq as daq

import utilities, utilitiespg3

from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output


# App Main
dash.register_page(__name__, name = 'Dritte Seite')


# # Load Dataset
# df = utilities.loadData()


# ######################################################################
# ######################### Style Section ##############################
# ######################################################################

# Create Slidebar
sidebar = html.Div(
    [
        html.H6('Activate Button to include multiple selection'),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-sensitivity-picker',
                    children = [ 
                        daq.BooleanSwitch(id = 'my-toggle-switch', on = False) #color="#9B51E0", label = 'My toggle switch', labelPosition='bottom'
                    ],
                ),
            ]
        ),
        html.Hr(),

        html.Div( 
            id = "my-toggle-switch-output"
        ),

        html.H6('Fast API'),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-date-picker',
                    children = [ 

                        html.P('Drücken Sie den Button um eine Prediction zu erhalten!', style = {'textAlign': 'justify'}),
                        # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
                        html.Div(id = "zeitraum_id"),
                        html.Div(id = "bundesland_id"),
                        # html.Br(),
                        dbc.Button(id = 'API_Button', children = 'Calculate with API'),
                        html.Hr(),
                        html.Div(id = "API_Call")
                    ],
                ),
            ]
        )
    ]
)

# Create Main Content Area
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Fälle_Zeitperiode', figure = {})
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Lost_records', figure = {})
                    ], width = 6
                )
            ]#, style = {"height": "10%"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_sector', figure = {})
                    ], width = 4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_methoden', figure = {})
                    ], width = 4
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_data_sensi', figure = {})
                    ], width = 4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_pro_Jahr', figure = {})
                    ], width = 12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_pro_Jahr_Sektor', figure = {})
                    ], width = 12
                )
                
            ]
        )
    ]
)

# Define the app
layout = html.Div([

    dbc.Row([

        dbc.Col(
                [
                    sidebar
                ], width = 2
            ),

        dbc.Col(
            [
                content
            ], width = 10
        )
    ])    
])


# ######################################################################
# #################### Dependencie Selection ###########################
# #### Eher nicht weil dann zu wenig flexibilität, was sektoren und ####
# #### methoden angeht##################################################
# ######################################################################
# # @callback(
# # Output('select-sector-dependend', 'options'),
# # Input('select-organisation', 'value'))
# # def set_cities_options(selected_country):
    
# #     print("ich bin hier")

# #     labels = df[df['organisation'] == selected_country]['sector_1'].unique()

# #     return labels






# ######################################################################
# #################### Function Plot Section ###########################
# ######################################################################
# # Callback for toggle switch button
# @callback(
#     Output('my-toggle-switch-output', 'children'),
#     Input('my-toggle-switch', 'on')
# )
# def update_output(value):

#     div = utilitiespg2.getStyleSection(df, value)

#     return div

# # KPI Anzahl unterschiedlicher Sektoren
# @callback( 
#     Output('KPI_Datensetgroeße_sector', 'figure'),
#     Input('select-year', 'value'),
#     Input('select-year2', 'value'),
#     Input('select-sector', 'value'),
#     Input('select-organisation', 'value'))
# def generateKPIDatensetgroeßeSector(start_year : int, end_year : int):

#     # df_temp = utilities.getMultipleSectors(df, sector)
#     fig = utilities.getKPIDatensetgroeße(df, start_year, end_year, 'sector_1', 'Sektoren')

#     return fig


# # # KPI Anzahl unterschiedlicher Methoden
# # @callback( 
# #     Output('KPI_Datensetgroeße_methoden', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateKPIDatensetgroeßeMethod(start_year : int, end_year : int):

# #     fig = utilities.getKPIDatensetgroeße(df, start_year, end_year, 'method', 'Methoden')

# #     return fig


# # # KPI Anzahl unterschiedlicher Data Senistivities
# # @callback( 
# #     Output('KPI_Datensetgroeße_data_sensi', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateKPIDatensetgroeßeDataSensitivity(start_year : int, end_year : int):

# #     fig = utilities.getKPIDatensetgroeße(df, start_year, end_year, 'data_sensitivity', 'Data Senistivity')

# #     return fig


# # # KPI Fälle Zeitperiode / Jahr
# # @callback( 
# #     Output('KPI_Fälle_Zeitperiode', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateKPIVorfälle(start_year : int, end_year : int):

# #     fig = utilities.getVorfälleYear(df, start_year, end_year)

# #     return fig

# # # KPI Lost records Zeitperiode / Jahr
# # @callback( 
# #     Output('KPI_Lost_records', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateKPIVorfälle(start_year : int, end_year : int):

# #     fig = utilities.getLostRecordsYear(df, start_year, end_year)

# #     return fig


# # # Fälle pro Jahr
# # @callback( 
# #     Output('Barchart_pro_Jahr', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateBarchartProJahr(start_year : int, end_year : int):

# #     fig = utilities.getBarchartProJahr(df, start_year, end_year)

# #     return fig

# # # Fälle pro Jahr und Sektor
# # @callback( 
# #     Output('Barchart_pro_Jahr_Sektor', 'figure'),
# #     Input('select-year', 'value'),
# #     Input('select-year2', 'value'))
# # def generateBarchartProJahrSektor(start_year : int, end_year : int):

# #     fig = utilities.getBarchartProJahrSektor(df, start_year, end_year)

# #     return fig



