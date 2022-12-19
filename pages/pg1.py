import dash
import dash_bootstrap_components as dbc
import utilities, utilitiespg1

from dash import html
from dash import dcc


# App Main
dash.register_page(__name__, path = '/', name = 'Home')


# Load Dataset
df = utilities.loadData()

# Create Main Content Area
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Datensetgröße', figure = utilitiespg1.getKPI(df, ''))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Unternehmen', figure = utilitiespg1.getKPI(df, 'organisation'))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Summe_Records', figure = utilitiespg1.getKPIRecords(df))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Year_High', figure = utilitiespg1.getKPIYear(df))
                    ], width = 3
                )
            ]#, style = {"height": "10%"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Sektoren', figure = utilitiespg1.getPie(df, 'sector_1', 'Sektoren'))
                    ], width = 12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Methoden', figure = utilitiespg1.getPie(df, 'method', 'Methoden'))
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Methoden_Summe', figure = utilitiespg1.getBarMethodeSensitive(df, 'method', 'Methoden'))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Data_Sensitivity', figure = utilitiespg1.getPie(df, 'data_sensitivity_text', 'Data Sensitivity'))
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Pie_Data_Sensitivity_Summe', figure = utilitiespg1.getBarMethodeSensitive(df, 'data_sensitivity_text', 'Data Sensitivity'))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Jahr', figure = utilitiespg1.getBarTime(df))
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Jahr', figure = utilitiespg1.getBarTime(df, True))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Unternehmen', figure = utilitiespg1.getBarUnternehmen(df))
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Unternehmen', figure = utilitiespg1.getBarUnternehmen(df, True))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Sektor', figure = utilitiespg1.getBarSektor(df))
                    ], width = 6
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Sektor', figure = utilitiespg1.getBarSektor(df, True))
                    ], width = 6
                )
            ]
        ),
    ]
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
