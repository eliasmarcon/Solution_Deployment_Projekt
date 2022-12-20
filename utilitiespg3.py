import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import utilities

from dash import html
from dash import dcc

##############################################
############### Style Sectiopn ###############
##############################################
def getStyleSection(df, togglevalue):

    style = [html.H6('Select organisation of your choice.'),
            html.Div( 
                className ='div-user-controls',
                children= [
                    html.Div( 
                        className='div-for-land-dropdown',
                        children=[ 
                            dcc.Dropdown(
                                id = 'select-organisation',
                                options = utilities.generate_options(df, 'organisation'), value = 'Twitter', className = 'postselector', multi = togglevalue 
                            )
                        ],
                    ),
                ]
            ),
            html.Hr(),

            html.H6('Select Year of your choice.'),
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

            # html.H6('Select Sector of your choice.'),
            # html.Div( 
            #     className = 'div-user-controls',
            #     children= [
            #         html.Div( 
            #             className = 'div-for-sector-picker',
            #             children = [ 
            #                 dcc.Dropdown(
            #                     id = 'select-sector',
            #                     options = utilities.generate_options(df, 'sector_1'), value = 'web', className = 'postselector', multi = togglevalue 
            #                 )
            #             ],
            #             style = {'width': '100%', 'display': 'inline-block'}
            #         )
            #     ]
            # ),
            # html.Hr(),

            # Selector Dependencie für Organisation
            # html.H6('Select Sector of your choice.'),
            # html.Div( 
            #     className = 'div-user-controls',
            #     children= [
            #         html.Div( 
            #             className = 'div-for-sector-picker',
            #             children = [ 
            #                 dcc.Dropdown(
            #                     id = 'select-sector-dependend',
            #                     options = utilities.generate_options(df, 'sector_1'), value = 'web', className = 'postselector', multi = True 
            #                 )
            #             ],
            #             style = {'width': '100%', 'display': 'inline-block'}
            #         )
            #     ]
            # ),
            # html.Hr(),

            html.H6('Select Method of your choice.'),
            html.Div( 
                className = 'div-user-controls',
                children= [
                    html.Div( 
                        className = 'div-for-method-picker',
                        children = [ 
                            dcc.Dropdown(
                                id = 'select-method-dependend', multi = togglevalue
                                #options = utilities.generate_options(df, 'method'), value = 'hacked', className = 'postselector'
                            )
                        ],
                    ),
                ]
            ),
            html.Hr(),

            html.H6('Select Data Sensitivity of your choice.'),
            html.Div( 
                className = 'div-user-controls',
                children= [
                    html.Div( 
                        className = 'div-for-sensitivity-picker',
                        children = [ 
                            dcc.Dropdown(
                                id = 'select-data-sensitivity-dependend', multi = togglevalue, optionHeight = 50
                                #options = utilities.generate_options(df, 'data_sensitivity_text'), className = 'postselector', value = 'Full details', optionHeight = 50, multi = togglevalue 
                            )
                        ],
                    ),
                ]
            ),
            html.Hr()]

    return style



########################################################################################################################################################################################
########################################################################################################################################################################################
########################################################################################################################################################################################


def getMultipleFilters(df, start_year : int, end_year : int, organisation, method, data_sensitivity, toggl_button):
    
    df = utilities.checkYear(df, start_year, end_year)

    if not toggl_button:
        
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

            df2 = df2[df2['method'].isin(method)]

            if data_sensitivity != None:

                df2 = df2[df2['data_sensitivity_text'].isin(data_sensitivity)]

    return df2



##############################################
########## KPI Anzahl Lost Records ###########
##############################################
def getKPIAnzahlLostRecords(df_temp, titlename):

    summe = df_temp.records_lost.sum()

    fig = go.Figure(go.Indicator(
                                    mode = "number",
                                    value = summe,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                            )
                    )

    if len(titlename) > 1:
        
        fig.update_layout(title = {'text' : "Summe der Lost Records für {} !".format(titlename)})

    else:

        fig.update_layout(title = {'text' : "Summe der Lost Records für " + str(titlename[0]) + "!"})

    return fig



##############################################
########## Pie Anzahl Lost Records ###########
##############################################
def getPieAnzahlLostRecords(df_temp, titlename):

    df = df_temp.groupby(['organisation'])['records_lost'].sum().reset_index(name = 'anzahl')
    fig = px.pie(df, values = df.anzahl, names = df.organisation, hole = .7)

    if len(titlename) > 1:
        
        fig.update_layout(legend = dict(orientation = "h"), title_text = "Summe der Lost Records für {} !".format(titlename), title_x = 0.5)

    else:

        fig.update_layout(legend = dict(orientation = "h"), title_text = 'Verteilung von ' + str(titlename[0]) + "!", title_x = 0.5)
    
    return fig



##############################################
### Barchart Anzahl Lost Records over time ###
##############################################
def getBarLostRecordsTime(df_temp, titlename):

    fig = px.bar(df_temp, x = "records_lost", y = "year", color = 'organisation', text = df_temp.records_lost, orientation = 'h')

    if len(titlename) > 1:
        
        fig.update_layout(title = {'text' : "Summe der Lost Records für {} !".format(titlename)})

    else:

        fig.update_layout(title = {'text' : "Summe der Lost Records für " + str(titlename[0]) + "!"})

    fig.update_traces(texttemplate='%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0, width = 1)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)


    return fig







