import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import utilities

from dash import html
from dash import dcc

##############################################
################ Style Section ###############
##############################################
def getStyleSection(df, togglevalue):

    style = [html.H6('Choose organization.'),
            html.Div( 
                className ='div-user-controls',
                children= [
                    html.Div( 
                        className='div-for-land-dropdown',
                        children=[ 
                            dcc.Dropdown(
                                id = 'select-organisation',
                                options = utilities.generate_options(df, 'organisation'), value = 'Facebook', className = 'postselector', multi = togglevalue 
                            )
                        ],
                    ),
                ]
            ),
            html.Hr(),

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

            # define method filter layout
            html.H6('Choose method.'),
            html.Div( 
                className = 'div-user-controls',
                children= [
                    html.Div( 
                        className = 'div-for-method-picker',
                        children = [ 
                            dcc.Dropdown(
                                id = 'select-method-dependend', multi = togglevalue
                            )
                        ],
                    ),
                ]
            ),
            html.Hr(),

            # define data sensitivity filter layout
            html.H6('Choose data sensitivity type.'),
            html.Div( 
                className = 'div-user-controls',
                children= [
                    html.Div( 
                        className = 'div-for-sensitivity-picker',
                        children = [ 
                            dcc.Dropdown(
                                id = 'select-data-sensitivity-dependend', multi = togglevalue, optionHeight = 50
                            )
                        ],
                    ),
                ]
            ),
            html.Hr()]

    return style



###############################################################################
################# apply multi selection mode to data ##########################
###############################################################################


def getMultipleFilters(df, start_year : int, end_year : int, organisation, method, data_sensitivity, toggle_button):
    
    df = utilities.checkYear(df, start_year, end_year)

    if not toggle_button:
        
        df2 = df[df['organisation'] == organisation]
        
        if method != None:

            df2 = df2[df2['method'] == method]
        
            if data_sensitivity != None:

                df2 = df2[df2['data_sensitivity_text'] == data_sensitivity]

    else:

        if type(organisation) == str:

            organisation = organisation.split()

        df2 = df[df['organisation'].isin(organisation)]

        if method != None:

            if type(method) == list:
                df2 = df2[df2['method'].isin(method)]
            else:
                df2 = df2[df2['method'] == method]

            if data_sensitivity != None:

                if type(data_sensitivity) == list:
                    df2 = df2[df2['data_sensitivity_text'].isin(data_sensitivity)]
                else:
                    df2 = df2[df2['data_sensitivity_text'] == data_sensitivity]

    return df2



##############################################
############## KPI stolen data ###############
##############################################
def getKPIAnzahlLostRecords(df_temp, titlename):

    summe = df_temp.records_lost.sum()

    fig = go.Figure(go.Indicator(
                                    mode = "number",
                                    number = {"font": {"size": utilities.number_size}},
                                    value = summe,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                            )
                    )

    if type(titlename) == str:
        
        fig.update_layout(title = {'text' : "Sum of stolen data for {}".format(titlename)}, title_x = 0.5, height = utilities.kpi_height)

    else:

        fig.update_layout(title = {'text' : "Sum of stolen data for selected organizations"}, title_x = 0.5, height = utilities.kpi_height)

    return fig



##############################################
############## Pie stolen data ###############
##############################################
def getPieAnzahlLostRecords(df_temp, titlename):

    df = df_temp.groupby(['organisation'])['records_lost'].sum().reset_index(name = 'anzahl')
    fig = px.pie(df, values = df.anzahl, names = df.organisation, hole = .7)

    if type(titlename) == str:
        
        fig.update_layout(legend = dict(orientation = "h"), title_text = "Stolen data distribution for {}".format(titlename), title_x = 0.5, height = utilities.kpi_height)

    else:

        fig.update_layout(legend = dict(orientation = "h"), title_text = 'Stolen data distribution for selected organizations', title_x = 0.5, height = utilities.kpi_height)
    
    return fig


##############################################
####### Barchart stolen data over time #######
##############################################
def getBarLostRecordsTime(df_temp, titlename):

    fig = px.bar(df_temp, x = "records_lost", y = "year", color = 'organisation', text = df_temp.records_lost, orientation = 'h', height = utilities.chart_height_3)

    if type(titlename) == str:
        
        fig.update_layout(title = {'text' : "Sum of stolen data for {}".format(titlename)})

    else:

        fig.update_layout(title = {'text' : "Sum of stolen data for selected organizations"})

    fig.update_traces(texttemplate='%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0, width = 1)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)

    return fig