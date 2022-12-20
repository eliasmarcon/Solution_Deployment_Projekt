import plotly.graph_objects as go
import plotly.express as px


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

        fig.update_layout(title = {'text' : "Anzahl an Vorfällen!"}, title_x = 0.5)

    else:

        fig.update_layout(title = {'text' : "Anzahl an Organisationen!"}, title_x = 0.5)


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

    fig.update_layout(title = {'text' : "Summe an gestohlenen Daten!"}, title_x = 0.5)

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

    fig.update_layout(title = {'text' : "Vergleich meisten gestohlenen Daten, <br> Jahr {}, im Vergleich zu 2022!".format(str(year))}, title_x = 0.5)

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
############# Bar Anzahl Column ##############
##############################################
def getBar(df, column, title, boolean = False):

    df = df.groupby(column).size().reset_index(name = 'anzahl')
    df['percentage'] = round((df.anzahl / df.anzahl.sum()) * 100, 2)
    df['dummy_variable'] = 'A'

    df = df.sort_values(by = ['percentage'], ascending = False)

    if boolean:

        fig = px.bar(df, x = "percentage", y = 'dummy_variable', color = column, orientation = 'h', barmode = 'stack', text = df['percentage'].apply(lambda x: '{0:1.2f}%'.format(x)))
        fig.update_yaxes(visible = False)
        fig.update_traces(insidetextanchor = "middle", width = 0.3)


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

    fig = px.bar(df, x = "year", y = "anzahl", color = "year", text = df.anzahl)

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Jahr!"})
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Jahr!"})
        fig.update_traces(texttemplate = '%{text:.0s}')

    fig.update_layout(yaxis_range = [0, max(df.anzahl) * 1.1])
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

    fig = px.line(df, x = "year", y = "anzahl", text = df.anzahl, markers = True)

    # print(df)

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Jahr!"})
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Jahr!"})

    fig.update_traces(textposition = "top center", textfont_size = 12)
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
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Unternehmen! (top 8)"})

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Unternehmen', yaxis_range = [0, max(df.anzahl) * 1.1])
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

    # print(df)

    fig = px.bar(df, x = "sector_1", y = "anzahl", color = "sector_1", text = "anzahl")

    if summe:
        
        fig.update_layout(title = {'text' : "Summe an gestohlenen Daten im jeweiligen Sektor! (top 8)"})
        fig.update_traces(texttemplate = '%{text:.2s}')

    else:

        fig.update_layout(title = {'text' : "Anzahl an Data breaches im jeweiligen Sektor! (top 8)"})

    fig.update_traces(textposition = 'outside', textfont_size = 12, textangle = 0)
    fig.update_layout(legend_title_text = 'Sektor', yaxis_range = [0, max(df.anzahl) * 1.1])
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

    fig = px.bar(df, x = df[column], y = "anzahl", color = df[column], text = "anzahl")
        
    fig.update_layout(title = {'text' : "Summe an gestohlenen Daten nach {}!".format(title)})
    fig.update_layout(legend = dict(orientation = "h"), title_x = 0.5, legend_title_text = title, yaxis_range = [0, max(df.anzahl) * 1.1])
    fig.update_traces(texttemplate = '%{text:.2s}', textposition = 'outside', textfont_size = 12, textangle = 0, cliponaxis = False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(title = None)
    
    return fig







