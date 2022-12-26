import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import utilities, utilitiespg2

from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output


# App Main
dash.register_page(__name__, name = 'Sectors')
load_figure_template("LUX")


# Load Dataset
df = utilities.loadData()


######################################################################
######################### Style Section ##############################
######################################################################

# Create Slidebar
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

# Create Main Content Area
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
    # children = [
    #                 html.Div(
    #                     children = [dcc.Graph(id = 'KPI_Fälle_Zeitperiode')],
                        
    #                 ),
    #                 html.Div(
    #                     children = [dcc.Graph(id = 'KPI_Lost_records')],
    #                     style = {'width': '50%', 'display': 'inline-block'}
    #                 )
    #             ]
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


######################################################################
#################### Function Plot Section ###########################
######################################################################

# KPI Anzahl unterschiedlicher Organisationen
@callback( 
    Output('KPI_Datensetgroeße_organisationen', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeOrganisation(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'organisation', 'organizations')

    return fig


# KPI Anzahl unterschiedlicher Methoden
@callback( 
    Output('KPI_Datensetgroeße_methoden', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeMethod(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'method', 'methods')

    return fig


# KPI Anzahl unterschiedlicher Data Senistivities
@callback( 
    Output('KPI_Datensetgroeße_data_sensi', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIDatensetgroeßeDataSensitivity(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getKPIDatensetgroeße(df_temp, start_year, end_year, 'data_sensitivity', 'data sensitivity types')

    return fig


# KPI Fälle Zeitperiode / Jahr
@callback( 
    Output('KPI_Fälle_Zeitperiode', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIVorfälle(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getVorfälleYear(df_temp, start_year, end_year)

    return fig

# KPI Lost records Zeitperiode / Jahr
@callback( 
    Output('KPI_Lost_records', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateKPIVorfälle(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getLostRecordsYear(df_temp, start_year, end_year)

    return fig


# Barchart Fälle pro Jahr
@callback( 
    Output('Barchart_pro_Jahr', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateBarchartProJahr(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getBarchartProJahr(df_temp, start_year, end_year)

    return fig


# Barchart Fälle pro Jahr und Sektor
@callback( 
    Output('Barchart_pro_Jahr_Sektor', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generateBarchartProJahrSektor(start_year : int, end_year : int, sector):

    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getBarchartProJahrSektor(df_temp, start_year, end_year)

    return fig


# Barchart Unternehmen mit meisten Leaks
@callback( 
    Output('Barchart_meisten_Leaks', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'))
def generateBarchartLeaksUnternehmen(start_year : int, end_year : int):

    fig = utilitiespg2.getBarchartLeaksUnternehmen(df, start_year, end_year)

    return fig


# Piechart Verteilung Methoden 
@callback(
    Output('Pie_Methoden', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generatePieMethoden(start_year : int, end_year : int, sector):
    
    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getPieChart(df_temp, start_year, end_year, 'method', 'Method')
    
    return fig


# Piechart Verteilung Data_Sensitivity 
@callback(
    Output('Pie_Data_Sensitivity', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-sector', 'value'))
def generatePieMethoden(start_year : int, end_year : int, sector):
    
    df_temp = utilitiespg2.getMultipleSectors(df, sector)
    fig = utilitiespg2.getPieChart(df_temp, start_year, end_year, 'data_sensitivity_text', 'Data sensitivity')

    return fig
