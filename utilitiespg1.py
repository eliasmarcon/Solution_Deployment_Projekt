import plotly.graph_objects as go
import plotly.express as px

kpi_height = 200
title_size = 15
number_size= 40

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
                                    number = {"font": {"size": number_size}},
                                    value = df_anzahl,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                                )
                    )

    if column == "":

        fig.update_layout(title = {'text' : "Count of Breaches"}, title_x = 0.5, title_font_size = title_size, height = kpi_height)

    else:

        fig.update_layout(title = {'text' : "Count of Organizations"}, title_x = 0.5, title_font_size = title_size, height = kpi_height)

    return fig

##############################################
############# KPI Records Summe ##############
##############################################
def getKPIRecords(df):

    summe = df['records_lost'].sum()

    fig = go.Figure(go.Indicator(
                                    mode = "number",
                                    number = {"font": {"size": number_size}},
                                    value = summe,
                                    domain = {'x': [0, 1], 'y': [0, 1]}
                                )
                    )

    fig.update_layout(title = {'text' : "Sum of stolen data"}, title_x = 0.5, title_font_size = title_size, height = kpi_height)

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
                                    number = {"font": {"size": number_size}},
                                    value = max_summe,
                                    delta = {'position': "bottom", 'reference': df_year_summe2[df_year_summe2['year'] == 2022]['summe'].values[0],
                                        	 'increasing': {'color': 'red'}}
                                )
                    )

    fig.update_layout(title = {'text' : "Max stolen data {}<br> vs. 2022".format(str(year))}, title_x = 0.5, title_font_size = title_size, height = kpi_height)

    return fig



##############################################
############# Pie Anzahl Column ##############
##############################################
def getPie(df, column, title):

    df = df.groupby(column).size().reset_index(name = 'anzahl')
    # print(df)

    fig = px.pie(df, values = df.anzahl, names = df[column], hole = .7)

    fig.update_layout(legend = dict(orientation = "h"), title_text = "Verteilung der Anzahl an {} !".format(title), title_x = 0.5, height=300)
    
    return fig



##############################################
############# Bar Anzahl Column ##############
##############################################
def getBar(df, column, title, boolean = False):

    df = df.groupby(column).size().reset_index(name = 'anzahl')
    df['percentage'] = round((df.anzahl / df.anzahl.sum()) * 100, 2)
    df['dummy_variable'] = 'A'

    df = df.sort_values(by = ['percentage'], ascending = False)

    if boolean:

        fig = px.bar(df, x = "percentage", y = 'dummy_variable', color = column, orientation = 'h', barmode = 'stack', text = df['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), height=300)
        fig.update_yaxes(visible = False)
        fig.update_xaxes(visible = False)
        fig.update_traces(insidetextanchor = "middle", width = 0.3)
        fig.update_layout(title_text = '{} distribution'.format(title), title_x = 0.5, legend_title_text='', legend_orientation="h")


    else:

        fig = px.bar(df, x = "percentage", y = df[column], color = column, orientation = 'h', text = df['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)))

    fig.update_traces(textposition = 'inside', textfont_size = 12, textangle = 0)
    # fig.update_layout(legend_title_text = 'Unternehmen')
    
    return fig



##############################################
##### Barchart Anzahl und Summe pro Jahr #####
##############################################
def getBarTime(df, summe = False):

    if summe:

        df = df.groupby('year')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('year')['year'].size().reset_index(name = 'anzahl')

    fig = px.bar(df, x = "year", y = "anzahl", text = df.anzahl, height = 300)

    if summe:
        
        fig.update_layout(title = {'text' : "Sum of stolen data by year"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Count of breaches by year"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.0s}')

    fig.update_layout(yaxis_range = [0, max(df.anzahl)*1.2])
    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig



##############################################
##### Linechart Anzahl und Summe pro Jahr ####
##############################################
def getLineTime(df, summe = False):

    if summe:

        df = df.groupby('year')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('year')['year'].size().reset_index(name = 'anzahl')

    fig = px.line(df, x = "year", y = "anzahl", text = df.anzahl, markers = True, height = 300)

    # print(df)

    if summe:
        
        fig.update_layout(title = {'text' : "Sum of stolen data by year"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Count of breaches by year!"}, title_x = 0.5)

    fig.update_traces(textposition = "top center", textfont_size = 12)
    fig.update_layout(title_x = 0.5, yaxis_range = [0, max(df.anzahl) * 1.3])
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

    fig = px.bar(df, x = "organisation", y = "anzahl", color = "organisation", text = "anzahl", orientation = 'h')

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Unternehmen! (top 8)"}, height = 250)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Unternehmen! (top 8)"}, height = 250)

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Unternehmen', yaxis_range = [0, max(df.anzahl) * 1.1])
    fig.update_layout(legend = dict(orientation = "h"), title_x = 0.5, legend_title_text = '', yaxis_range = [0, max(df.anzahl) * 1.1])
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig

##############################################
#### Barchart Anzahl und Summe pro Sektor ####
##############################################
def getBarSektor(df, summe = False):

    if summe:

        df = df.groupby('sector_1')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('sector_1')['sector_1'].size().reset_index(name = 'anzahl')


    df = df.sort_values(by = ['anzahl'])

    df = df[-8:]

    df = df.sort_values(by = ['anzahl'], ascending = False)

    # print(df)

    fig = px.bar(df, x = "sector_1", y = "anzahl", color = "sector_1", text = "anzahl", height = 300)

    if summe:
        
        fig.update_layout(title = {'text' : "Sum of stolen data by sector (top 8)"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Count of breaches by sector (top 8)"}, title_x = 0.5)

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Sektor', yaxis_range = [0, max(df.anzahl) * 1.1], showlegend=False)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig

##############################################
#### Barchart Anzahl und Summe pro Methode ###
##############################################
def getBarMethod(df, summe = False):

    if summe:

        df = df.groupby('method')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('method')['method'].size().reset_index(name = 'anzahl')


    df = df.sort_values(by = ['anzahl'])

    df = df[-8:]
 
    df = df.sort_values(by = ['anzahl'], ascending = False)

    fig = px.bar(df, x = "anzahl", y = "method", color = "method", text = "anzahl", height = 300, orientation = "h")

    if summe:
        
        fig.update_layout(title = {'text' : "Sum of stolen data by method"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Count of breaches by method"}, title_x = 0.5)

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'method', xaxis_range = [0, max(df.anzahl)*1.2], showlegend=False)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig

#######################################################
#### Barchart Anzahl und Summe pro Data Sensitivity ###
#######################################################
def getBarDataSensitivity(df, summe = False):

    if summe:

        df = df.groupby('data_sensitivity_text')['records_lost'].sum().reset_index(name = 'anzahl')

    else:
    
        df = df.groupby('data_sensitivity_text')['data_sensitivity_text'].size().reset_index(name = 'anzahl')


    df = df.sort_values(by = ['anzahl'])

    df = df[-8:]

    df = df.sort_values(by = ['anzahl'], ascending = False)

    fig = px.bar(df, x = "anzahl", y = "data_sensitivity_text", color = "data_sensitivity_text", text = "anzahl", height = 300, orientation = "h")

    if summe:
        
        fig.update_layout(title = {'text' : "Sum of stolen data by data sensitivity"}, title_x = 0.5)
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Count of breaches by data sensitivity"}, title_x = 0.5)

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'data sensivity', xaxis_range = [0, max(df.anzahl)*1.2], showlegend=False)
    fig.update_xaxes(title = None)
    fig.update_yaxes(title = None)
    
    return fig

##############################################
#### Barchart Anzahl und Summe pro Sektor ####
##############################################
def getBarMethodeSensitive(df, column, title):
    
    df = df.groupby(column)['records_lost'].sum().reset_index(name = 'anzahl')

    df = df.sort_values(by = ['anzahl'])

    # print(df)

    fig = px.bar(df, x = df[column], y = "anzahl", color = df[column], text = "anzahl", height = 300)
        
    fig.update_layout(title = {'text' : "Summe an gestohlenen Daten nach {}!".format(title)})
    fig.update_layout(legend = dict(orientation = "h"), title_x = 0.5, legend_title_text = title, yaxis_range = [0, max(df.anzahl) * 1.1])
    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0, cliponaxis = False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(title = None)
    
    return fig







