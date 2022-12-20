import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests

from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


# App Main
app = dash.Dash(__name__)

# Style Components
# Fix sidebar to the left side
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "20rem", "padding": "2rem 1rem", "background-color": "#f8f9fa",
}

# Place main content on the right
CONTENT_STYLE = {
    "display": "inline-block", "margin-left": "21rem", "margin-right": "2rem", "padding": "2rem 1rem"
}

# Load Data and Transform Date
def load_data():
    
    # scrape covid data
    ds_url = 'https://www.data.gv.at/katalog/dataset/846448a5-a26e-4297-ac08-ad7040af20f1'
    page = requests.get(ds_url).text
    soup = BeautifulSoup(page, 'html.parser')
    file_url = soup.find('a', class_='resource-url-analytics').get('href')
    
    df = pd.read_csv(file_url, sep = ";")
    df['Meldedatum'] = pd.to_datetime(df['Meldedatum'], format = '%d.%m.%Y %H:%M:%S')
    # df['Meldedatum'] = pd.to_datetime(df['Meldedatum'], format = '%d.%m.%Y %H:%M:%S').dt.date
    
    return df

df = load_data()
# df = pd.read_csv(r"C:\Users\elias\Downloads\Hospitalisierung.csv", delimiter=";")

# Generate Filter Options Bundesland
def generate_options(dataframe):

    list_bundeslaender = list(dataframe['Bundesland'].unique())
    
    options = []

    for sym in list_bundeslaender:

        options.append({'label': sym, 'value': sym})

    return options

# Get Filtered Dataframe based on User Input
def getFilteredDataframe(bundesland : str = "Österreich", start_Date : 'datetime' = df.Meldedatum.min() - timedelta(days = 7), end_Date : 'datetime' = df.Meldedatum.max()):

    df_temp = df[(df['Meldedatum'].between(start_Date, end_Date)) & (df['Bundesland'] == bundesland)].sort_values(by = ['Meldedatum'])
    
    return df_temp

# Without Bundesland
def getFilteredDataframe2(bundesland :str, start_Date : 'datetime' = df.Meldedatum.min() - timedelta(days = 7), end_Date : 'datetime' = df.Meldedatum.max()):

    df_temp = df.copy()

    # calculating the daily tests
    df_temp['help_table'] = df_temp['TestGesamt'] - df_temp['TestGesamt'].shift(10)
    df_temp['help_table'] = df_temp['help_table'].fillna(0)

    # calculating the first 10 columns
    df_temp['help_table_2'] = df_temp['TestGesamt'][:10]
    df_temp['help_table_2'] = df_temp['help_table_2'].fillna(0)

    # combing both columns into the Tests_daily
    df_temp['Tests_daily'] = df_temp['help_table'] + df_temp['help_table_2']

    # deleting the unnecessary columns
    df_temp = df_temp.drop(['TestGesamt', 'help_table', 'help_table_2'], axis = 1)

    # transforming the float column into an int
    df_temp['Tests_daily'] = pd.to_numeric(df_temp['Tests_daily'], downcast = 'integer')
    
    if bundesland == "":

        df_temp2 = df_temp[df_temp['Meldedatum'].between(start_Date, end_Date)].sort_values(by = ['Meldedatum'])

    else:

        df_temp2 = df_temp[(df_temp['Meldedatum'].between(start_Date, end_Date)) & (df_temp['Bundesland'] == bundesland)].sort_values(by = ['Meldedatum'])
    
    return df_temp2


# get KPIs
def getKPIDashboard(dataframe, column):
    
    mean = int(dataframe[column].mean())
    max = dataframe["IntensivBettenKapGes"].max()

    #prozent = (mean / max) * 100

    fig = go.Figure(
            go.Indicator(
                mode = "gauge+number",
                value = mean,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {'axis': {'range': [0, max]},
                         'bar': {'color': '#2a3f5f'},
                         'steps' : [
                                    {'range': [0, max // 2], 'color': px.colors.qualitative.Light24[19]},
                                    {'range': [max // 2, max - max // 4], 'color': px.colors.qualitative.Light24[7]},
                                    {'range': [max - max // 4, max], 'color': px.colors.qualitative.Light24[0]}
                                   ]
                        }))

    return fig


# Create Slidebar
sidebar = html.Div(
    [
        html.H2('Select Bundesland of your choice.'),
        html.Hr(),
        html.Div( 
            className ='div-user-controls',
            children= [
                html.Div( 
                    className='div-for-land-dropdown',
                    children=[ 
                        dcc.Dropdown(
                            id = 'select-bundesland',
                            options = generate_options(df), value = 'Österreich', className = 'postselector'
                        )
                    ],
                ),
            ]
        ),
        html.H2('Select Date of your choice.'),
        html.Hr(),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-date-picker',
                    children = [ 
                        dcc.DatePickerRange(
                            id = 'date-picker-range',
                            min_date_allowed = df.Meldedatum.min(),
                            max_date_allowed = df.Meldedatum.max(),
                            start_date = df.Meldedatum.max() - timedelta(days = 7),
                            end_date = df.Meldedatum.max(),
                            calendar_orientation = 'vertical'
                        )
                    ],
                ),
            ]
        ),
        html.H2('Fast API'),
        html.Hr(),
        html.Div( 
            className = 'div-user-controls',
            children= [
                html.Div( 
                    className = 'div-for-date-picker',
                    children = [ 

                        html.P('Drücken Sie den Button um die Prozentwerte der Gauge Grafiken zu erhalten!', style = {'textAlign': 'justify'}),
                        # html.P('Ausgewählte Zeitperiode in Tagen: ' + str(len(df))),
                        html.Div(id = "zeitraum_id"),
                        html.Div(id = "bundesland_id"),
                        html.Br(),
                        dbc.Button(id = 'API_Button', children = 'Calculate with API'),
                        html.Hr(),
                        html.Div(id = "API_Call")
                    ],
                ),
            ]
        )
    ],

    style = SIDEBAR_STYLE # Include style to fix position
)


# Create Main Content Area
content = html.Div(
    id = "page-content", 
    children = [
                    html.Div(
                        className='div-for-text',
                        children=[
                            html.H1('COVID 19 Hospitalisierungen'), 
                            html.P('''A basic Dashboard with Dash and Plotly, showing the Hospitalisierungen of Austria.''')
                        ]
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'KPI_Intensibettenbelegung_Gesamt')],
                        style={'width': '49%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'KPI_Intensibettenbelegung_Frei')],
                        style={'width': '49%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'KPI_Intensibettenbelegung_Nicht_Covid')],
                        style={'width': '49%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'KPI_Intensibettenbelegung_Covid')],
                        style={'width': '49%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'Tests_Zeitraum')],
                        style = {'width': '100%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'Tests_Zeitraum_Bundesland')],
                        style = {'width': '100%', 'display': 'inline-block'}
                    ),
                    html.Div(
                        children = [dcc.Graph(id = 'Verlauf_Intensivbettenbelegung')],
                        style = {'width': '100%', 'display': 'inline-block'}
                    )
                ],

    style = CONTENT_STYLE # Include style to fix position
)


# Define the app
app.layout = html.Div([sidebar, content])



# Create Plots
# Tests_Zeitraum
@app.callback( 
    Output('Tests_Zeitraum', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateTestsGesamt(start_date : 'datetime', end_date : 'datetime'):
    
    df_Tests = getFilteredDataframe2("", start_date, end_date)

    df_Tests = df_Tests.groupby(['Bundesland']).sum().reset_index().sort_values(by = ['Tests_daily'])

    fig = px.bar(df_Tests, x = 'Bundesland', y = 'Tests_daily', color = 'Bundesland', text = 'Tests_daily')
    fig.update_traces(texttemplate = '%{text:.3s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Durchgeführte Tests im ausgewählten Zeitraum!"})

    return fig


# Tests_Zeitraum_Bundesland
@app.callback( 
    Output('Tests_Zeitraum_Bundesland', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateTestsGesamtBundesland(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
    
    df_Tests = getFilteredDataframe2(bundesland, start_date, end_date)
    fig = px.line(df_Tests, x = 'Meldedatum', y = 'Tests_daily', markers = True)
    fig.update_layout(title = {'text' : "Durchgeführte Tests in " + bundesland + " im ausgewählten Zeitraum!"})

    return fig


# Verlauf_Intensivbettenbelegung
@app.callback( 
    Output('Verlauf_Intensivbettenbelegung', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateVerlaufIntensivbettenbelegung(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
     
    df_Verlauf = getFilteredDataframe(bundesland, start_date, end_date)
    df_Verlauf = df_Verlauf[['Meldedatum', 'IntensivBettenBelNichtCovid19', 'IntensivBettenFrei', 'IntensivBettenBelCovid19']]
    df_Verlauf = pd.melt(df_Verlauf, id_vars = ['Meldedatum'], var_name = 'Belegungsart', value_name = 'Belegung')
    df_Verlauf = df_Verlauf.sort_values(by = ['Meldedatum']).sort_values(by = ['Belegung'], ascending = False)

    fig = px.bar(df_Verlauf, x = "Meldedatum", y = 'Belegung', color = "Belegungsart", text = 'Belegung')
    fig.update_traces(texttemplate = '%{text:.3s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(title = {'text' : "Belegung der Intensivbetten in " + bundesland + " und im ausgewählten Zeitraum!"})

    return fig


# KPI_Intensibettenbelegung_Gesamt
@app.callback( 
    Output('KPI_Intensibettenbelegung_Gesamt', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateKPIIntensivBettenKapGes(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
    
    df_KPIGesamt = getFilteredDataframe(bundesland, start_date, end_date)
    fig = getKPIDashboard(df_KPIGesamt, "IntensivBettenKapGes")
    fig.update_layout(title = {'text' : "Ø Intensivbettenkapazität in " + bundesland + "!"})

    return fig


# KPI_Intensibettenbelegung_Frei
@app.callback( 
    Output('KPI_Intensibettenbelegung_Frei', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateKPIIntensivBettenFrei(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
    
    df_KPIFrei = getFilteredDataframe(bundesland, start_date, end_date)
    fig = getKPIDashboard(df_KPIFrei, "IntensivBettenFrei")
    fig.update_layout(title = {'text' : "Ø freie Intensivbetten in " + bundesland + "!"})

    return fig
    

# KPI_Intensibettenbelegung_Nicht_Covid
@app.callback( 
    Output('KPI_Intensibettenbelegung_Nicht_Covid', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateKPIIntensivBettenBelNichtCovid19(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
    
    df_KPINichtCov = getFilteredDataframe(bundesland, start_date, end_date)
    fig = getKPIDashboard(df_KPINichtCov, "IntensivBettenBelNichtCovid19")
    fig.update_layout(title = {'text' : "Ø Intensivbettenbelegung in " + bundesland + "!"})

    return fig


# KPI_Intensibettenbelegung_Covid
@app.callback( 
    Output('KPI_Intensibettenbelegung_Covid', 'figure'),
    Input('select-bundesland', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def generateKPIIntensivBettenBelCovid19(bundesland : str, start_date : 'datetime', end_date : 'datetime'):
    
    df_KPICov = getFilteredDataframe(bundesland, start_date, end_date)
    fig = getKPIDashboard(df_KPICov, "IntensivBettenBelCovid19")
    fig.update_layout(title = {'text' : "Ø Intensivbettenbelegung mit COVID-19 in " + bundesland + "!"})

    return fig

# Zeitperiode
@app.callback( 
    Output('zeitraum_id', component_property = 'children'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def getDateDiff(start_date, end_date):

    delta = pd.to_datetime(end_date, format = "%Y-%m-%d %H:%M:%S") - pd.to_datetime(start_date, format = "%Y-%m-%d %H:%M:%S")
    return f'Ausgewählte Zeitperiode in Tagen: {delta.days + 1}'

# Bundesland Auswahl
@app.callback( 
    Output('bundesland_id', component_property = 'children'),
    Input('select-bundesland', 'value'))
def getBundesland(bundesland):

    return f'Ausgewähltes Bundesland: {bundesland}'


@app.callback(
    Output("API_Call", component_property = 'children'), 
    [Input('API_Button', 'n_clicks')],
    #  Input('select-bundesland', 'value'),
    #  Input('date-picker-range', 'start_date'),
    #  Input('date-picker-range', 'end_date')],
    [State(component_id = 'select-bundesland', component_property = 'value'),
     State(component_id = 'date-picker-range', component_property = 'start_date'),
     State(component_id = 'date-picker-range', component_property = 'end_date')],
    prevent_initial_call = True)
    # old Version
    # Output("API_Call", component_property = 'children'), 
    # Input('API_Button', 'n_clicks'),
    # Input('select-bundesland', 'value'),
    # Input('date-picker-range', 'start_date'),
    # Input('date-picker-range', 'end_date'),
    # prevent_initial_call = True)
def calculatePercent(_, bundesland : str, start_date : datetime, end_date : datetime):
    
    df_filtered = getFilteredDataframe(bundesland, start_date, end_date)

    maxGesamtkapazität = int(df_filtered["IntensivBettenKapGes"].sum())
    sumFrei = int(df_filtered["IntensivBettenFrei"].sum())
    sumOCovid = int(df_filtered["IntensivBettenBelNichtCovid19"].sum())
    sumCovid = int(df_filtered["IntensivBettenBelCovid19"].sum())

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    inputs = {
                'maxGesamtkapazität' : maxGesamtkapazität,
                'sumFrei' : sumFrei,
                'sumOCovid' : sumOCovid,
                'sumCovid' : sumCovid,
            }

    response = requests.post(url = "http://localhost:8000/calculatePercantage", params = inputs, headers = headers)

    percentage_frei = response.json()['percentageFrei']
    percentageOCovid = response.json()['percentageOCovid']
    percentageCovid = response.json()['percentageCovid']

    return html.Div(
                        children=[
                                    # html.P(f"In {bundesland} hat es folgende Prozentverteilungen gegeben!", style = {'textAlign': 'justify'}),
                                    html.P(f"Prozentsatz an freien Instensivbetten: {percentage_frei} Prozent!", style = {'textAlign': 'justify'}),
                                    html.P(f"Prozentsatz an belegten Intensivbetten ohne Covid Erkrankung: {percentageOCovid} Prozent!", style = {'textAlign': 'justify'}),
                                    html.P(f"Prozentsatz an belegten Intensivbetten mit Covid Erkrankung: {percentageCovid} Prozent!", style = {'textAlign': 'justify'})
                        ]
                    )


# Run the app
def start():    
    app.run_server(host='0.0.0.0', port=80)

if __name__ == '__main__':
    start()