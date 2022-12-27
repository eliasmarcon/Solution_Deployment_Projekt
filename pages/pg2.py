import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import utilities, utilitiespg2

from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output

# page settings
dash.register_page(__name__, name = 'Sectors')

# load bootstrap figure template
load_figure_template("LUX")

# load dataset
df = utilities.loadData()

######################################################################
######################### layout section #############################
######################################################################

# define sidebar content
sidebar = html.Div(
    [
        html.H6('Choose period.'),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-year-picker',
                    children = [ 
                         dcc.Dropdown(
                            id = 'select-year',
                            options = utilities.generate_options(df, 'year'), value = '2004', className = 'postselector'
                        )
                    ],
                    style = {'width': '49%', 'display': 'inline-block'}
                ),
                html.Div( 
                    className = 'div-for-year2-picker',
                    children = [ 
                         dcc.Dropdown(
                            id = 'select-year2',
                            options = utilities.generate_options(df, 'year'), value = '2022', className = 'postselector'
                        )
                    ],
                    style = {'width': '49%', 'display': 'inline-block'}
                )
            ]
        ),
        html.Hr(),

        html.H6('Choose sector(s).'),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-sector-picker',
                    children = [ 
                         dcc.Dropdown(
                            id = 'select-sector',
                            options = utilities.generate_options(df, 'sector_1'), value = 'web', className = 'postselector', multi = True
                        )
                    ],
                    style = {'width': '100%', 'display': 'inline-block'}
                )
            ]
        ),

    ]
)

# define main content area
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Fälle_Zeitperiode', figure = {})
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Lost_records', figure = {})
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_organisationen', figure = {})
                    ], width = 2
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_methoden', figure = {})
                    ], width = 2
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgroeße_data_sensi', figure = {})
                    ], width = 2
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_pro_Jahr_Sektor', figure = {})
                    ], width = 8
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Methoden', figure = {})
                    ], width = 2
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Data_Sensitivity', figure = {})
                    ], width = 2
                )
                
            ]
        ),
    ]
)

# define page layout
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

######################################################################
#################### function plot section ###########################
######################################################################

# KPI unique organizations
@callback( 
    Output('KPI_Datensetgroeße_organisationen', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeOrganisation(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'organisation', 'organizations')

    return fig

# KPI unique methods
@callback( 
    Output('KPI_Datensetgroeße_methoden', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeMethod(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'method', 'methods')

    return fig

# KPI unique data sensitivities
@callback( 
    Output('KPI_Datensetgroeße_data_sensi', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeDataSensitivity(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'data_sensitivity', 'data sensitivity types')

    return fig

# KPI count of breaches in period
@callback( 
    Output('KPI_Fälle_Zeitperiode', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIVorfälle(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getVorfälleYear(df_temp, start_year, end_year)

    return fig

# KPI stolen data in period
@callback( 
    Output('KPI_Lost_records', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIVorfälle(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getLostRecordsYear(df_temp, start_year, end_year)

    return fig

# Barchart count of breaches by year and sector
@callback( 
    Output('Barchart_pro_Jahr_Sektor', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateBarchartProJahrSektor(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getBarchartProJahrSektor(df_temp, start_year, end_year)

    return fig

# Piechart method distribution
@callback(
    Output('Pie_Methoden', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generatePieMethoden(start_year : int, end_year : int, sector):
    
    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getPieChart(df_temp, start_year, end_year, 'method', 'Method')
    
    return fig

# Piechart data sensitivity distribution
@callback(
    Output('Pie_Data_Sensitivity', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generatePieMethoden(start_year : int, end_year : int, sector):
    
    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getPieChart(df_temp, start_year, end_year, 'data_sensitivity_text', 'Data sensitivity')

    return fig