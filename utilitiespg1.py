import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import utilities

##############################################
############# KPI Anzahl Column ##############
##############################################
def getKPI(df, column):

    if column == "":
        
        df_anzahl = len(df)

    else:

        df_anzahl = len(df[column].unique())

    fig = go.Figure(go.Indicator(
                                    mode = "number",
                                    value = df_anzahl,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                                )
                    )

    if column == "":

        fig.update_layout(title = {'text' : "Anzahl an Vorfällen!"})

    else:

        fig.update_layout(title = {'text' : "Anzahl an Organisationen!"})


    return fig



##############################################
############# KPI Records Summe ##############
##############################################
def getKPIRecords(df):

    summe = df['records_lost'].sum()

    fig = go.Figure(go.Indicator(
                                    mode = "number",
                                    value = summe,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                                )
                    )

    fig.update_layout(title = {'text' : "Summe an gestohlenen Daten!"})

    return fig



##############################################
################# KPI Year ###################
##############################################
def getKPIYear(df):

    df_year_summe = df.groupby('year')['records_lost'].sum().reset_index(name = 'summe')
    df_year_summe2 = df_year_summe.sort_values(by = ['summe'])
    
    max_summe = df_year_summe2['summe'].iloc[-1]
    year = df_year_summe2['year'].iloc[-1]

    fig = go.Figure(go.Indicator(
                                    mode = "number+delta",
                                    value = max_summe,
                                    delta = {'position': "bottom", 'reference': df_year_summe2[df_year_summe2['year'] == 2022]['summe'].values[0],
                                        	 'increasing': {'color': 'red'}}
                                )
                    )

    fig.update_layout(title = {'text' : "Meisten gestohlenen Daten, Jahr {}!".format(str(year))})

    return fig



##############################################
############# Pie Anzahl Column ##############
##############################################
def getPie(df, column, title):

    df = df.groupby(column).size().reset_index(name = 'anzahl')
    # print(df)

    fig = px.pie(df, values = df.anzahl, names = df[column], hole = .7)

    fig.update_layout(legend = dict(orientation = "h"), title_text = "Verteilung der Anzahl an {} !".format(title), title_x = 0.5)
    
    return fig



##############################################
##### Barchart Anzahl und Summe pro Jahr #####
##############################################
def getBarTime(df, summe = False):

    if summe:

        df = df.groupby('year')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('year')['year'].size().reset_index(name = 'anzahl')

    fig = px.bar(df, x = "year", y = "anzahl", color = "year", text = df.anzahl)

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Jahr!"})

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Jahr!"})

    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig



##############################################
# Barchart Anzahl und Summe pro Unternehmen ##
##############################################
def getBarUnternehmen(df, summe = False):

    if summe:

        df = df.groupby('organisation')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('organisation').size().reset_index(name = 'anzahl')


    df = df.sort_values(by = ['anzahl'])

    df = df[-8:]

    # print(df)

    fig = px.bar(df, x = "organisation", y = "anzahl", color = "organisation", text = "anzahl")

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Unternehmen! (top 8)"})

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Unternehmen! (top 8)"})

    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Unternehmen')
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig



##############################################
# Barchart Anzahl und Summe pro Sektor ##
##############################################
def getBarSektor(df, summe = False):

    if summe:

        df = df.groupby('sector_1')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('sector_1')['sector_1'].size().reset_index(name = 'anzahl')


    df = df.sort_values(by = ['anzahl'])

    df = df[-8:]

    # print(df)

    fig = px.bar(df, x = "sector_1", y = "anzahl", color = "sector_1", text = "anzahl")

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Sektor! (top 8)"})

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Sektor! (top 8)"})

    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Sektor')
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig



##############################################
# Barchart Anzahl und Summe pro Sektor ##
##############################################
def getBarMethodeSensitive(df, column, title):
    
    df = df.groupby(column)['records_lost'].sum().reset_index(name = 'anzahl')

    df = df.sort_values(by = ['anzahl'])

    # print(df)

    fig = px.bar(df, x = df[column], y = "anzahl", color = df[column], text = "anzahl")
        
    fig.update_layout(title = {'text' : "Summe an gestohlenen Daten nach {}!".format(title)})
    fig.update_layout(legend = dict(orientation = "h"), title_x = 0.5, legend_title_text = title)
    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(title = None)
    
    return fig







