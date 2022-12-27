import dash
from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash_bootstrap_templates import load_figure_template
import requests
import utilities, utilitiespg3

# page settings
dash.register_page(__name__, name = 'Organizations', external_stylesheets = [dbc.themes.LUX])

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
        # multi selection toggle
        html.H6('Enable multiple selection'),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    children = [ 
                        daq.BooleanSwitch(id = 'my-toggle-switch', on = False) 
                    ],
                ),
            ]
        ),
        html.Hr(),

        html.Div( 
            id = "my-toggle-switch-output"
        ),

        html.H6('Fast API regression model'),
        html.Div( 
            children= [
                html.Div( 
                    children = [ 

                        # prediction model year input 
                        html.P('Predict the count of breaches.', style = {'textAlign': 'justify'}),
                        html.H6('Enter year.', style = {'textAlign': 'justify'}),
                        dcc.Input(
                            id="input_number",
                            className="list-group-item",
                            type="number",
                            value='2025',
                            placeholder="input year",
                            style={'width': '100%', 'height': 25}
                        ),

                        # prediction model output
                        html.H6('Predicted count of breaches.', style = {'textAlign': 'justify', 'margin-top': 5}),
                        dcc.Input(
                            id='textarea',
                            className="list-group-item",
                            value='',
                            style={'width': '100%', 'height': 25},
                        ),
                    ],
                ),
            ]
        )
    ]
)

# define main content layout
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPIAnzahlLostRecords', figure = {})
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'PieAnzahlLostRecords', figure = {})
                    ], width = 6
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'BarLostRecordsTime', figure = {})
                    ], width = 12
                )
            ]
        )
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
####################### callback section #############################
######################################################################

# toggle multi selection switch
@callback(
    Output('my-toggle-switch-output', 'children'),
    Input('my-toggle-switch', 'on')
)
def update_output(value):

    div = utilitiespg3.getStyleSection(df, value)

    return div

# filter method based on organisation
@callback(
    Output('select-method-dependend', 'options'),
    Input('select-organisation', 'value'))
def getAuswahlMethod(selected_organization):
    
    if type(selected_organization) == str:
        
        labels = df[df['organisation'] == selected_organization]['method'].unique()

    else:

        labels = df[df['organisation'].isin(selected_organization)]['method'].unique()

    return labels

# filter data senistivity based on organization and method
@callback(
    Output('select-data-sensitivity-dependend', 'options'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'))
def getAuswahlDataSensitivity(selected_organization, selected_method):

    if type(selected_organization) == str:
        
        df2 = df[df['organisation'] == selected_organization]
        labels = df2[df2['method'] == selected_method]['data_sensitivity_text'].unique()

        return labels

    else:

        df2 = df[df['organisation'].isin(selected_organization)]
        if selected_method is None:
            labels = None
        else:
            labels = df2[df2['method'].isin(selected_method)]['data_sensitivity_text'].unique()
        return labels

######################################################################
#################### function plot section ###########################
######################################################################

# KPI stolen data
@callback( 
    Output('KPIAnzahlLostRecords', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generateKPIAnzahlLostRecords(start_year : int, end_year : int, organisation, method, data_sensitivity, togglebutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglebutton)
    fig = utilitiespg3.getKPIAnzahlLostRecords(df_temp, df_temp.organisation.unique())

    return fig

# pie stolen data
@callback( 
    Output('PieAnzahlLostRecords', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generatePieAnzahlLostRecords(start_year : int, end_year : int, organisation, method, data_sensitivity, togglebutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglebutton)
    fig = utilitiespg3.getPieAnzahlLostRecords(df_temp, df_temp.organisation.unique())

    return fig


# bar chart stolen data over time
@callback( 
    Output('BarLostRecordsTime', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generateBarLostRecordsTime(start_year : int, end_year : int, organisation, method, data_sensitivity, togglebutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglebutton)
    fig = utilitiespg3.getBarLostRecordsTime(df_temp, df_temp.organisation.unique())

    return fig


# fast api call 
@callback(
    Output('textarea', 'value'),
    Input('input_number', 'value'))
def useApi(number: int):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    params = {
        'year': number,
    }
    response = requests.post('http://0.0.0.0:8001/predict', params=params, headers=headers)
    data = response.json()
    return data['noOfBreaches']
