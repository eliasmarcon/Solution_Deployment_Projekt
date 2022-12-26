import dash
from dash import html
from dash import dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash_bootstrap_templates import load_figure_template
import requests
import utilities, utilitiespg3

# App Main
dash.register_page(__name__, name = 'Organizations', external_stylesheets = [dbc.themes.LUX])
load_figure_template("LUX")

# Load Dataset
df = utilities.loadData()

######################################################################
######################### Style Section ##############################
######################################################################

# Create Slidebar
sidebar = html.Div(
    [
        html.H6('Enable multiple selection'),
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

                        html.P('Predict the count of breaches for specific year.', style = {'textAlign': 'justify'}),
                        # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
                        html.Div(id = "zeitraum_id"),
                        html.Div(id = "bundesland_id"),
                        # html.Br(),
                        dcc.Input(
                            id="input_number",
                            type="number",
                            value='2025',
                            placeholder="input type number",
                            style={'width': '100%', 'height': 25}
                        ),
                        dcc.Input(
                            id='textarea',
                            value='',
                            style={'width': '100%', 'height': 25},
                        ),
                        dbc.Button(id = 'API_Button', children = 'Calculate with API', style={'width': '100%'}),
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
                        dcc.Graph(id = 'KPIAnzahlLostRecords', figure = {})
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'PieAnzahlLostRecords', figure = {})
                    ], width = 6
                )
            ]#, style = {"height": "10%"}
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
#################### Dependencie Selection ###########################
######################################################################
# Callback for toggle switch button
@callback(
    Output('my-toggle-switch-output', 'children'),
    Input('my-toggle-switch', 'on')
)
def update_output(value):

    div = utilitiespg3.getStyleSection(df, value)

    return div

# Auswahl für Method based on Organisation
@callback(
    Output('select-method-dependend', 'options'),
    Input('select-organisation', 'value'), prevent_initial_call = True)
def getAuswahlMethod(selected_country):
    
    if type(selected_country) == str:
        
        labels = df[df['organisation'] == selected_country]['method'].unique()

    else:

        labels = df[df['organisation'].isin(selected_country)]['method'].unique()

    return labels

# Auswahl für Data Senistivity based on Organisation und Method
@callback(
    Output('select-data-sensitivity-dependend', 'options'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'), prevent_initial_call = True)
def getAuswahlDataSensitivity(selected_country, selected_method):

    if type(selected_country) == str:
        
        df2 = df[df['organisation'] == selected_country]
        labels = df2[df2['method'] == selected_method]['data_sensitivity_text'].unique()

        return labels

    else:

        df2 = df[df['organisation'].isin(selected_country)]
        labels = df2[df2['method'].isin(selected_method)]['data_sensitivity_text'].unique()

        return labels


######################################################################
#################### Function Plot Section ###########################
######################################################################

# KPI an Lost Records
@callback( 
    Output('KPIAnzahlLostRecords', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generateKPIAnzahlLostRecords(start_year : int, end_year : int, organisation, method, data_sensitivity, togglbutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglbutton)
    fig = utilitiespg3.getKPIAnzahlLostRecords(df_temp, df_temp.organisation.unique())

    return fig

# Pie an Lost Records
@callback( 
    Output('PieAnzahlLostRecords', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generatePieAnzahlLostRecords(start_year : int, end_year : int, organisation, method, data_sensitivity, togglbutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglbutton)
    fig = utilitiespg3.getPieAnzahlLostRecords(df_temp, df_temp.organisation.unique())

    return fig


# Bar an Lost Records over time
@callback( 
    Output('BarLostRecordsTime', 'figure'),
    Input('select-year', 'value'),
    Input('select-year2', 'value'),
    Input('select-organisation', 'value'),
    Input('select-method-dependend', 'value'),
    Input('select-data-sensitivity-dependend', 'value'),
    Input('my-toggle-switch', 'on'), prevent_initial_call = True)
def generateBarLostRecordsTime(start_year : int, end_year : int, organisation, method, data_sensitivity, togglbutton):

    df_temp = utilitiespg3.getMultipleFilters(df, start_year, end_year, organisation, method, data_sensitivity, togglbutton)
    fig = utilitiespg3.getBarLostRecordsTime(df_temp, df_temp.organisation.unique())

    return fig


@callback(
    Output('textarea', 'value'),
    Input('input_number', 'value'), prevent_initial_call = True)
def useApi(number: int):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }
    params = {
        'number': number,
    }
    response = requests.post('http://0.0.0.0:8001/predict', params=params, headers=headers)
    return response.text
