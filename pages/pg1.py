import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import utilities, utilitiespg1

# App Main
dash.register_page(__name__, path = '/', name = 'Home', external_stylesheets = [dbc.themes.LUX])
load_figure_template("LUX")

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
                        dcc.Graph(id = 'KPI_Summe_Records', figure = utilitiespg1.getKPIRecords(df))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Unternehmen', figure = utilitiespg1.getKPI(df, 'organisation'))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'KPI_Year_High', figure = utilitiespg1.getKPIYear(df))
                    ], width = 3
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Sektor', figure = utilitiespg1.getBarSektor(df))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Sektor', figure = utilitiespg1.getBarSektor(df, True))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Bar_Sektoren_2', figure = utilitiespg1.getBar(df, 'sector_1', 'Sector', True))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Method', figure = utilitiespg1.getBarMethod(df))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Method', figure = utilitiespg1.getBarMethod(df, True))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Bar_Method_2', figure = utilitiespg1.getBar(df, 'method', 'Method', True))
                    ], width = 6
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Anzahl_Sensitivity', figure = utilitiespg1.getBarDataSensitivity(df))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Barchart_Summe_Sensitivity', figure = utilitiespg1.getBarDataSensitivity(df, True))
                    ], width = 3
                ),
                dbc.Col(
                    [
                        dcc.Graph(id = 'Bar_sensitivity_2', figure = utilitiespg1.getBar(df, 'data_sensitivity_text', 'Data sensivity', True))
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
                        dcc.Graph(id = 'Linechart_Summe_Jahr', figure = utilitiespg1.getLineTime(df, True))
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
